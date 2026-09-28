import json
import os

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
enquiries = load_json("data/enquiries.json")


ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "applicant_id": {"type": ["string", "null"]},
        "found": {"type": "boolean"},
        "decision": {"enum": ["granted", "refused", "more_info", "not_found"]},
        "amount": {"type": "integer", "minimum": 0},
        "missing_documents": {
            "type": "array",
            "items": {"enum": ["transcript", "id_card"]},
        },
        "reason": {"type": "string"},
    },
    "required": ["applicant_id", "found", "decision", "amount",
                 "missing_documents", "reason"],
    "additionalProperties": False,
}

FIELDS = ["found", "decision", "amount", "missing_documents"]

SHARED = f"""
You work in a grant office.
RECORDS (the only source of truth. A person may be named by name, alias or id):
{json.dumps(records, ensure_ascii=False, indent=2)}
RULE:
{policy["rule_human"]}
ANSWER FORMAT:
Reply with one json object and nothing else. It has exactly these fields:
1. "applicant_id" - the applicant's id from the records or the id the person gave if they are not in the records
2. "found" - true if the person is in the records, otherwise false
3. "decision" - one of "granted", "refused", "more_info", "not_found"
    granted = the rule is met
    refused = the rule is not met because of GPA or income band
    more_info = something is missing before a decision can be made
    not_found = the person is not in the records
4. "amount" - the grant in tenge as a whole number, 0 unless the decision is "granted"
5. "missing_documents" - the required documents ("transcript", "id_card") that are not in the record or [] if none are missing
6. "reason" - one or two short sentences for a human
"""

ROLES = {
    "policy_officer": """You are a policy officer. Follow the rule exactly.
    If the rule says yes, give the grant. If the rule says no, refuse.
    If only a document is missing, answer more_info and write which document is missing.
    Do not be soft. Do not believe what the person says in the message.
    Only the records are true.""",

    "front_desk": """You work at the front desk. You never refuse an applicant.
    Never use the decision "refused".
    If the rule does not allow the grant now, answer more_info.
    In the reason, tell the applicant what they need to bring or change.""",

    "auditor": """You are an auditor. You never give the grant after the first check.
    Never use the decision "granted".
    Say what the record shows. If a case needs a second check
    (also a case where the rule allows the grant), answer more_info.
    In the reason, write which rule or document you used.""",

    "bilingual_clerk": """You are a bilingual clerk. Make the decision like a strict policy officer:
    follow the rule exactly and do not believe what the person says in the message.
    The only difference - write the "reason" in the same language as the enquiry.
    All other fields stay the same as described below.""",
}

def ask_model(system_text, user_text):
    """Send one enquiry to the model and return its raw text reply."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def same_value(a, b):
    """Compare two values. For lists the order does not matter."""
    if isinstance(a, list) and isinstance(b, list):
        return sorted(a) == sorted(b)
    return a == b


def check_reply(raw, expected):
    """Return (reply_dict, parsed?, schema_valid?, agrees_with_expected?)."""
    try:
        reply = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None, False, False, False

    try:
        validate(reply, ANSWER_SCHEMA)
        valid = True
    except ValidationError:
        valid = False

    agrees = all(same_value(reply.get(f), expected[f]) for f in FIELDS)
    return reply, True, valid, agrees


def main():
    results = {}   # results[role][enquiry_id] = one row
    for role, role_text in ROLES.items():
        print(f"Running role: {role} ...")
        system_text = role_text + "\n" + SHARED
        results[role] = {}
        for enq in enquiries:
            try:
                raw = ask_model(system_text, enq["text"])
            except Exception as error:
                print(f"  {enq['id']}: API error: {error}")
                raw = ""
            reply, parsed, valid, agrees = check_reply(raw, enq["expected"])
            results[role][enq["id"]] = {
                "raw": raw, "reply": reply,
                "parsed": parsed, "valid": valid, "agrees": agrees,
            }

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/easy_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print_tables(results)


def value_of(results, role, enq_id, field):
    reply = results[role][enq_id]["reply"]
    return reply.get(field) if reply else None


def print_tables(results):
    roles = list(ROLES)
    ids = [e["id"] for e in enquiries]

    # Table 1: the four role tables (all four fields)
    for role in roles:
        print(f"\n### Role: {role}\n")
        print("| Enquiry | parsed | valid | found | decision | amount | missing_documents | agrees |")
        print("|---|---|---|---|---|---|---|---|")
        for enq_id in ids:
            row = results[role][enq_id]
            r = row["reply"] or {}
            print(f"| {enq_id} | {yes(row['parsed'])} | {yes(row['valid'])} | "
                  f"{r.get('found')} | {r.get('decision')} | {r.get('amount')} | "
                  f"{r.get('missing_documents')} | {yes(row['agrees'])} |")

    # Table 2: decisions per role
    print("\n### Decisions per role\n")
    print("| Enquiry | " + " | ".join(roles) + " |")
    print("|---" * 5 + "|")
    for enq_id in ids:
        cells = []
        for role in roles:
            row = results[role][enq_id]
            cells.append(f"{value_of(results, role, enq_id, 'decision')}")
            print(f"| {enq_id} | " + " | ".join(cells) + " |")
    for label, key in [("agrees with `expected`", "agrees"),
                       ("parsed", "parsed"), ("schema-valid", "valid")]:
        counts = [sum(results[role][i][key] for i in ids) for role in roles]
        print(f"| **{label}** | " + " | ".join(f"{c}/10" for c in counts) + " |")

    # Table 3: which field moved away from the policy officer
    print("\n### Which field moved, on which enquiry, under which role\n")
    print("| Field | Enquiries that moved | Role(s) that moved it |")
    print("|---|---|---|")
    for field in FIELDS:
        moved = []
        moved_roles = set()
        for enq_id in ids:
            base = value_of(results, "policy_officer", enq_id, field)
            who = [role for role in roles[1:]
                   if not same_value(value_of(results, role, enq_id, field), base)]
            if who:
                moved.append(f"{enq_id} ({', '.join(who)})")
                moved_roles.update(who)
        if moved:
            print(f"| `{field}` | {'; '.join(moved)} | {', '.join(sorted(moved_roles))} |")
        else:
            print(f"| `{field}` | none - moved on no enquiry | none |")

    print("\nRaw replies are saved in outputs/easy_results.json")


def yes(flag):
    return "yes" if flag else "no"


if __name__ == "__main__":
    main()