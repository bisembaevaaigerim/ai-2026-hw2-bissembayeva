import json
import os
import sys

from dotenv import load_dotenv
from jsonschema import ValidationError, validate
from openai import OpenAI

load_dotenv()
client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


records = load_json("data/records.json")
policy = load_json("data/policy.json")
script = load_json("data/chat_script.json")
STATE_SCHEMA = load_json("data/memory_state.schema.json")

SYSTEM = f"""
You are the assistant of a grant office, chatting with an applicant.

RECORDS (the only source of truth):
{json.dumps(records, ensure_ascii=False, indent=2)}

RULE:
{policy["rule_human"]}

Reply to every message with one json object and nothing else, with these fields:
"applicant_id" (string or null), "found" (true/false),
"decision" ("granted", "refused", "more_info" or "not_found"),
"amount" (whole number in tenge, 0 unless granted),
"missing_documents" (list of "transcript"/"id_card" not in the record),
"reason" (your short, friendly answer to the applicant's message).
"""

COMPRESS_INSTRUCTION = f"""
PROGRAM COMMAND (not from the applicant): compress.
Summarise the whole conversation above into one json object and nothing else.
It must follow this JSON schema exactly:
{json.dumps(STATE_SCHEMA, indent=2)}

Rules:
- applicant_id: the id the applicant gave or null if they never gave one.
- facts: every fact the APPLICANT stated, even if said only once (who they are,
  documents sent or missing, income band, family members on file, ...).
- decisions: what the office has told the applicant (decision, amount, what is missing).
- constraints: conditions on how or when something can happen (a day, a deadline, ...).
- open_questions: every question the applicant asked that was not answered yet.
- language: the language the applicant used.
- Never invent anything that was not said.
"""


class Session:
    def __init__(self):
        self.turns = []
        self.state = None
        self.last_usage = None

    def build_messages(self):
        """The exact list of messages sent to the model on the next call."""
        messages = [{"role": "system", "content": SYSTEM}]
        if self.state is not None:
            messages.append({
                "role": "system",
                "content": "Conversation state so far (earlier turns were "
                           "compressed into this object):\n"
                           + json.dumps(self.state, ensure_ascii=False, indent=2),
            })
        return messages + self.turns

    def call_model(self, messages):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"},
        )
        self.last_usage = response.usage
        return response.choices[0].message.content, response.usage.prompt_tokens

    def send(self, user_text):
        """A normal chat turn: it is kept in the history."""
        self.turns.append({"role": "user", "content": user_text})
        answer, tokens_sent = self.call_model(self.build_messages())
        self.turns.append({"role": "assistant", "content": answer})
        return answer, tokens_sent

    def ask_once(self, question):
        """A probe: asked from the current memory, but NOT kept in the history."""
        messages = self.build_messages() + [{"role": "user", "content": question}]
        return self.call_model(messages)

    def compress(self):
        """Replace the turns with one validated state object.
        If the summary is broken, keep the history and say so."""
        messages = self.build_messages() + [
            {"role": "user", "content": COMPRESS_INSTRUCTION}]
        raw, tokens_sent = self.call_model(messages)
        try:
            new_state = json.loads(raw)
            validate(new_state, STATE_SCHEMA)
        except (json.JSONDecodeError, ValidationError) as error:
            print("!! Compression FAILED - the history is kept. Reason:",
                  str(error).splitlines()[0])
            return False, tokens_sent
        self.state = new_state
        self.turns = []
        return True, tokens_sent


def reason_of(raw):
    """Take the human answer out of a JSON reply (or the raw text if broken)."""
    try:
        return json.loads(raw).get("reason", raw)
    except (json.JSONDecodeError, AttributeError):
        return raw


def run_script(use_compress):
    session = Session()
    calls = []
    for number, turn in enumerate(script["conversation"], start=1):
        if turn == "<compress>":
            if use_compress:
                ok, tokens = session.compress()
                calls.append({"call": number, "turn": "compress", "tokens": tokens,
                              "ok": ok})
            else:
                calls.append({"call": number, "turn": "(skipped)", "tokens": None})
            continue
        _, tokens = session.send(turn)
        calls.append({"call": number, "turn": turn, "tokens": tokens})
        print(f"  call {number}: sent {tokens} tokens")

    probes = []
    for probe in script["probes"]:
        answer, _ = session.ask_once(probe["question"])
        retrieved = any(word.lower() in answer.lower()
                        for word in probe["expect_contains"])
        probes.append({"id": probe["id"], "tests": probe["tests"],
                       "retrieved": retrieved, "answer": reason_of(answer),
                       "raw": answer})
    return calls, probes, session.state


def scripted():
    print("Run A - never compressed ...")
    calls_a, probes_a, _ = run_script(use_compress=False)
    print("Run B - compressed at the `compress` turn ...")
    calls_b, probes_b, state_b = run_script(use_compress=True)

    print("\n### Tokens per call\n")
    print("| Call | A - never compressed | B - compressed at the `compress` turn |")
    print("|---|---|---|")
    for a, b in zip(calls_a, calls_b):
        a_cell = a["tokens"] if a["tokens"] is not None else "- (compress skipped)"
        b_cell = b["tokens"]
        if b["turn"] == "compress":
            b_cell = f"{b['tokens']} (the compress call)"
        print(f"| {a['call']} | {a_cell} | {b_cell} |")
    a_tokens = [c["tokens"] for c in calls_a if c["tokens"] is not None]
    b_tokens = [c["tokens"] for c in calls_b if c["tokens"] is not None]
    b_chat = [c["tokens"] for c in calls_b
              if c["tokens"] is not None and c["turn"] != "compress"]
    print(f"| **peak** | {max(a_tokens)} | {max(b_tokens)} |")
    print(f"| **peak of chat calls (without the compress call)** | "
          f"{max(a_tokens)} | {max(b_chat)} |")
    print(f"| **total for the run** | {sum(a_tokens)} | {sum(b_tokens)} |")

    print("\n### Probes after the conversation\n")
    print("| Probe | Tests | A retrieved? | A answer | B retrieved? | B answer |")
    print("|---|---|---|---|---|---|")
    for pa, pb in zip(probes_a, probes_b):
        print(f"| {pa['id']} | {pa['tests']} | {yes(pa['retrieved'])} | "
              f"{short(pa['answer'])} | {yes(pb['retrieved'])} | {short(pb['answer'])} |")
    print(f"| **retrieved** | | {sum(p['retrieved'] for p in probes_a)}/5 | | "
          f"{sum(p['retrieved'] for p in probes_b)}/5 | |")

    print("\n### The state my compression produced\n")
    if state_b is None:
        print("(compression failed - no state; see the message above)")
    else:
        print(json.dumps(state_b, ensure_ascii=False, indent=2))

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/medium_results.json", "w", encoding="utf-8") as f:
        json.dump({"A": {"calls": calls_a, "probes": probes_a},
                   "B": {"calls": calls_b, "probes": probes_b, "state": state_b}},
                  f, ensure_ascii=False, indent=2)
    print("\nFull results are saved in outputs/medium_results.json")


def yes(flag):
    return "yes" if flag else "no"


def short(text):
    """One line, no table-breaking characters, for the markdown table."""
    return str(text).replace("\n", " ").replace("|", "/")


def interactive():
    session = Session()
    print("Interactive chat. Commands: compress, tokens, quit")
    while True:
        text = input("\nyou> ").strip()
        if text in ("quit", "exit"):
            break
        if text == "":
            continue
        if text == "tokens":
            u = session.last_usage
            if u is None:
                print("No call yet.")
            else:
                print(f"Last call: sent {u.prompt_tokens} tokens, "
                      f"got back {u.completion_tokens}, total {u.total_tokens}")
            continue
        if text == "compress":
            ok, tokens = session.compress()
            print(f"(compress call sent {tokens} tokens)")
            if ok:
                print("New state - this is now what is sent instead of the turns:")
                print(json.dumps(session.state, ensure_ascii=False, indent=2))
            continue
        answer, tokens = session.send(text)
        print("office>", reason_of(answer))
        print(f"   [sent {tokens} tokens; memory now holds "
              f"{len(session.turns)} turn messages"
              f"{' + a state object' if session.state else ''}]")


if __name__ == "__main__":
    if "--interactive" in sys.argv:
        interactive()
    else:
        scripted()