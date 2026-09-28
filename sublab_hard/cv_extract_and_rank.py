
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


rubric = load_json("data/candidate_rubric.json")
STORY_IDS = ["story-01", "story-02", "story-03", "story-04", "story-05", "story-06"]


def read_story(story_id):
    with open(f"data/candidates/{story_id}.md", encoding="utf-8") as f:
        return f.read()


CV_SCHEMA = {
    "type": "object",
    "properties": {
        "candidate_id": {"type": "string"},
        "full_name": {"type": ["string", "null"]},
        "degree": {"type": ["string", "null"]},
        "graduation_year": {"type": ["integer", "null"]},
        "gpa_4_scale": {"type": ["number", "null"], "minimum": 0, "maximum": 4},
        "gpa_original": {"type": ["number", "null"]},
        "gpa_original_scale": {"type": ["number", "null"]},
        "languages": {"type": "array", "items": {"type": "string"}},
        "published_count": {"type": "integer", "minimum": 0},
        "published_papers": {"type": "array", "items": {"type": "string"}},
        "unpublished_papers": {"type": "array", "items": {"type": "string"}},
        "experience_months": {"type": ["integer", "null"], "minimum": 0},
        "experience_not_countable": {"type": "array", "items": {"type": "string"}},
        "ambiguities": {"type": "array", "items": {"type": "string"}},
        "evidence": {"type": "object", "additionalProperties": {"type": "string"}},
    },
    "required": ["candidate_id", "full_name", "degree", "graduation_year",
                 "gpa_4_scale", "gpa_original", "gpa_original_scale", "languages",
                 "published_count", "published_papers", "unpublished_papers",
                 "experience_months", "experience_not_countable", "ambiguities",
                 "evidence"],
    "additionalProperties": False,
}

EXTRACT_RULES = """
RULES (follow all of them):
1. A fact the story does not state is null. Never estimate it. No GPA in the
   story means gpa_4_scale = null - never guess it from the degree, the
   university or the impression the story gives.
2. A GPA on another scale is converted to the 4.0 scale
   (gpa_4_scale = gpa_original / gpa_original_scale * 4, rounded to 2 decimals),
   and the original number and scale are recorded in gpa_original and
   gpa_original_scale.
3. A paper is published only when the story says "published" or "accepted".
   "Submitted", "under review", "in preparation", "planned" and "in press" are
   NOT published: put them in unpublished_papers and do not count them in
   published_count. A poster is not a peer-reviewed publication.
4. Contradictions are not resolved and not averaged: if the story gives two
   different values for a field, that field is null and the contradiction is
   written in ambiguities.
5. Experience: count months, not jobs. Overlapping periods count once. A period
   with no dates or no month count is not countable: write it in
   experience_not_countable and do not add it to experience_months.
6. evidence: for every field you fill, give a short exact quote from the story
   as {"field_name": "quote"}.
"""

EXTRA_RULES = """
7. Some stories are not in English (for example Kazakh). Write every field in
   English, but keep the evidence quotes in the original language.
8. Part-time months count as full months; do not reduce them.
"""

EXTRACT_FORMAT = f"""
Reply with one json object and nothing else, following this JSON schema:
{json.dumps(CV_SCHEMA, indent=2)}
"""


def extract_cv(story_id, story_text):
    """Ask the model for a CV. Returns (cv_dict or None, parsed?, valid?, raw)."""
    system_text = ("You extract a structured CV from a scholarship application story.\n"
                   + EXTRACT_RULES + EXTRA_RULES + EXTRACT_FORMAT)
    user_text = f"candidate_id: {story_id}\n\nSTORY:\n{story_text}"
    raw = ask_json(system_text, user_text)
    return check(raw, CV_SCHEMA)


SCORE_SCHEMA = {
    "type": "object",
    "properties": {
        "academic": {"type": "number", "minimum": 0, "maximum": 5},
        "research": {"type": "number", "minimum": 0, "maximum": 5},
        "experience": {"type": "number", "minimum": 0, "maximum": 5},
    },
    "required": ["academic", "research", "experience"],
    "additionalProperties": False,
}


def score_cv(cv):
    """Ask the model for three 0-5 scores. Returns (scores or None, parsed?, valid?, raw)."""
    system_text = f"""
You score one scholarship candidate against this rubric.

CRITERIA:
{json.dumps(rubric["criteria"], indent=2)}

COUNTING RULES:
{json.dumps(rubric["counting_rules"], indent=2)}

Reply with ONE JSON object and nothing else, exactly like:
{{"academic": <0-5>, "research": <0-5>, "experience": <0-5>}}
Do NOT compute a total, a weighted score or a ranking.
"""
    user_text = "CANDIDATE CV:\n" + json.dumps(cv, ensure_ascii=False, indent=2)
    raw = ask_json(system_text, user_text)
    return check(raw, SCORE_SCHEMA)


WEIGHTS = {c["id"]: c["weight"] for c in rubric["criteria"]}


def weighted_total(scores):
    total = sum(WEIGHTS[name] * scores[name] for name in WEIGHTS)
    return round(total, 2)


def ask_prose_winner():
    stories = "\n\n".join(f"=== {sid} ===\n{read_story(sid)}" for sid in STORY_IDS)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content":
                "You help a scholarship committee. Rubric:\n"
                + json.dumps(rubric, ensure_ascii=False, indent=2)},
            {"role": "user", "content":
                stories + "\n\nIn one short paragraph: which candidate should "
                "win the one funded place, and why?"},
        ],
    )
    return response.choices[0].message.content


def ask_json(system_text, user_text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_text},
                  {"role": "user", "content": user_text}],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def check(raw, schema):
    """Parse the reply and validate it against a schema."""
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None, False, False, raw
    try:
        validate(data, schema)
        return data, True, True, raw
    except ValidationError as error:
        print("   schema problem:", error.message)
        return data, True, False, raw


def traps_seen(cv):
    """Describe which of the four traps show up in this extraction."""
    traps = []
    if cv.get("gpa_4_scale") is None and not cv.get("ambiguities"):
        traps.append("no GPA stated (gpa null)")
    scale = cv.get("gpa_original_scale")
    if scale not in (None, 4, 4.0):
        traps.append(f"GPA on another scale ({cv.get('gpa_original')}/{scale} "
                     f"-> {cv.get('gpa_4_scale')}/4)")
    if cv.get("unpublished_papers"):
        traps.append(f"{len(cv['unpublished_papers'])} unpublished paper(s) not counted")
    if cv.get("ambiguities"):
        traps.append("contradiction recorded: " + "; ".join(cv["ambiguities"]))
    return traps or ["none"]


def main():
    results = {}
    for sid in STORY_IDS:
        print(f"{sid}: extracting ...")
        cv, parsed, valid, raw = extract_cv(sid, read_story(sid))
        row = {"parsed": parsed, "valid": valid, "cv": cv, "raw_cv": raw,
               "scores": None, "total": None}
        if valid:
            print(f"{sid}: scoring ...")
            scores, s_parsed, s_valid, s_raw = score_cv(cv)
            row["raw_scores"] = s_raw
            if s_valid:
                row["scores"] = scores
                row["total"] = weighted_total(scores)
        results[sid] = row

    print("asking the model in prose ...")
    prose = ask_prose_winner()

    # ---- Part 1 table ----
    print("\n### Part 1 - extraction\n")
    print("| Story | Parsed? | Valid? | Fields that came back `null` | Traps hit |")
    print("|---|---|---|---|---|")
    for sid, row in results.items():
        cv = row["cv"] or {}
        nulls = [k for k, v in cv.items() if v is None]
        print(f"| {sid} | {yes(row['parsed'])} | {yes(row['valid'])} | "
              f"{', '.join(nulls) or 'none'} | {'; '.join(traps_seen(cv))} |")

    print("\nExtraction for story-06:\n")
    print(json.dumps(results["story-06"]["cv"], ensure_ascii=False, indent=2))

    print("\n### Part 2 - scores and the winner\n")
    print("| Candidate | academic (0-5) | research (0-5) | experience (0-5) | weighted total (code) |")
    print("|---|---|---|---|---|")
    for sid, row in results.items():
        s = row["scores"] or {}
        print(f"| {sid} | {s.get('academic')} | {s.get('research')} | "
              f"{s.get('experience')} | {row['total']} |")

    ranked = sorted([sid for sid in results if results[sid]["total"] is not None],
                    key=lambda sid: results[sid]["total"], reverse=True)
    print("\nRanking computed by code:")
    for place, sid in enumerate(ranked, start=1):
        name = (results[sid]["cv"] or {}).get("full_name")
        print(f"  {place}. {sid} ({name}) - {results[sid]['total']}")
    if len(ranked) >= 2:
        winner, second = ranked[0], ranked[1]
        gap = round(results[winner]["total"] - results[second]["total"], 2)
        print(f"\n**Winner, computed by my code:** {winner} "
              f"({results[winner]['cv'].get('full_name')}), total {results[winner]['total']}")
        print(f"Gap to second place ({second}): {gap}")
        if gap <= 0.05:
            print("WARNING: the top two are within 0.05 of each other.")

    print("\n**The model's prose answer:**\n")
    print(prose)

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/hard_results.json", "w", encoding="utf-8") as f:
        json.dump({"results": results, "ranking": ranked, "prose": prose},
                  f, ensure_ascii=False, indent=2)
    print("\nFull results are saved in outputs/hard_results.json")


def yes(flag):
    return "yes" if flag else "no"


if __name__ == "__main__":
    main()