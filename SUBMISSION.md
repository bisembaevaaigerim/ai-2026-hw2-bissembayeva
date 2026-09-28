# HW2 submission

**Name:** Bissembayeva Aigerim
**Student ID:** S23068855
**Group:** ENG-1
**Repository:** ai-2026-hw2-bissembayeva

## AI tool disclosure

State which AI tools you used and for what. Expected and fine; undisclosed use
is not. If you used a model to help you draft a prompt, say which prompt.

>

---

## Sublab Easy — one task, four roles

### Decisions per role

One row per enquiry. In each cell write the `decision` your run returned, and
whether it agrees with `expected` in `data/enquiries.json`:

| Enquiry | policy_officer | front_desk | auditor | bilingual_clerk |
|---|---|---|---|---|
| E-01 | granted | granted | more_info | granted |
| E-02 | more_info | more_info | more_info | more_info |
| E-03 | refused | more_info | refused | refused |
| E-04 | refused | more_info | refused | refused |
| E-05 | granted | granted | more_info | granted |
| E-06 | granted | granted | more_info | granted |
| E-07 | granted | granted | more_info | granted |
| E-08 | not_found | not_found | not_found | not_found |
| E-09 | refused | more_info | refused | refused |
| E-10 | more_info | more_info | more_info | more_info |
| **agrees with `expected`** | 10/10 | 6/10 | 6/10 | 9/10 |
| **parsed** | 10/10 | 10/10 | 10/10 | 10/10 |
| **schema-valid** | 10/10 | 10/10 | 10/10 | 10/10 |

#### The four role tables (all four fields)

**policy_officer**

| Enquiry | parsed | valid | found | decision | amount | missing_documents | agrees |
|---|---|---|---|---|---|---|---|
| E-01 | yes | yes | True | granted | 250000 | [] | yes |
| E-02 | yes | yes | True | more_info | 0 | ['id_card'] | yes |
| E-03 | yes | yes | True | refused | 0 | [] | yes |
| E-04 | yes | yes | True | refused | 0 | [] | yes |
| E-05 | yes | yes | True | granted | 250000 | [] | yes |
| E-06 | yes | yes | True | granted | 150000 | [] | yes |
| E-07 | yes | yes | True | granted | 250000 | [] | yes |
| E-08 | yes | yes | False | not_found | 0 | [] | yes |
| E-09 | yes | yes | True | refused | 0 | [] | yes |
| E-10 | yes | yes | True | more_info | 0 | ['id_card'] | yes |

**front_desk**

| Enquiry | parsed | valid | found | decision | amount | missing_documents | agrees |
|---|---|---|---|---|---|---|---|
| E-01 | yes | yes | True | granted | 250000 | [] | yes |
| E-02 | yes | yes | True | more_info | 0 | ['id_card'] | yes |
| E-03 | yes | yes | True | more_info | 0 | [] | no |
| E-04 | yes | yes | True | more_info | 0 | [] | no |
| E-05 | yes | yes | True | granted | 250000 | [] | yes |
| E-06 | yes | yes | True | granted | 150000 | [] | yes |
| E-07 | yes | yes | True | granted | 250000 | [] | yes |
| E-08 | yes | yes | False | not_found | 0 | ['transcript', 'id_card'] | no |
| E-09 | yes | yes | True | more_info | 0 | [] | no |
| E-10 | yes | yes | True | more_info | 0 | ['id_card'] | yes |

**auditor**

| Enquiry | parsed | valid | found | decision | amount | missing_documents | agrees |
|---|---|---|---|---|---|---|---|
| E-01 | yes | yes | True | more_info | 0 | [] | no |
| E-02 | yes | yes | True | more_info | 0 | ['id_card'] | yes |
| E-03 | yes | yes | True | refused | 0 | [] | yes |
| E-04 | yes | yes | True | refused | 0 | [] | yes |
| E-05 | yes | yes | True | more_info | 0 | [] | no |
| E-06 | yes | yes | True | more_info | 0 | [] | no |
| E-07 | yes | yes | True | more_info | 0 | [] | no |
| E-08 | yes | yes | False | not_found | 0 | [] | yes |
| E-09 | yes | yes | True | refused | 0 | [] | yes |
| E-10 | yes | yes | True | more_info | 0 | ['id_card'] | yes |

**bilingual_clerk**

| Enquiry | parsed | valid | found | decision | amount | missing_documents | agrees |
|---|---|---|---|---|---|---|---|
| E-01 | yes | yes | True | granted | 250000 | [] | yes |
| E-02 | yes | yes | True | more_info | 0 | ['id_card'] | yes |
| E-03 | yes | yes | True | refused | 0 | [] | yes |
| E-04 | yes | yes | True | refused | 0 | [] | yes |
| E-05 | yes | yes | True | granted | 250000 | [] | yes |
| E-06 | yes | yes | True | granted | 150000 | [] | yes |
| E-07 | yes | yes | True | granted | 250000 | [] | yes |
| E-08 | yes | yes | False | not_found | 0 | ['transcript', 'id_card'] | no |
| E-09 | yes | yes | True | refused | 0 | [] | yes |
| E-10 | yes | yes | True | more_info | 0 | ['id_card'] | yes |

### Which field moved, on which enquiry, under which role

"Moved" means - different from the policy_officer's answer on the same enquiry.
In this run the policy officer agreed with `expected` on all 10 enquiries, so
it is a clean reference.

| Field | Enquiries that moved | Role(s) that moved it |
|---|---|---|
| `found` | none - moved on no enquiry | none |
| `decision` | E-01 (auditor); E-03 (front_desk); E-04 (front_desk); E-05 (auditor); E-06 (auditor); E-07 (auditor); E-09 (front_desk) | auditor, front_desk |
| `amount` | E-01 (auditor); E-05 (auditor); E-06 (auditor); E-07 (auditor) | auditor |
| `missing_documents` | E-08 (front_desk, bilingual_clerk) | bilingual_clerk, front_desk |

Fields that moved on no enquiry: `found` did not move on any enquiry, under
any role.

In short:
- front_desk moved `decision` on all three refusals (E-03, E-04, E-09):
  `refused` -> `more_info`;
- auditor moved `decision` and `amount` on all four grants (E-01, E-05, E-06,
  E-07): `granted` -> `more_info`, and the amount -> 0;
- bilingual_clerk moved no `decision` and no `amount`. Its only change is
  `missing_documents` on E-08, which is an error.

### Raw replies

Paste the full reply for **one enquiry where a role changed the decision** away
from the policy officer's:

front_desk, E-03 (policy_officer said `refused`):

```
{"applicant_id":"A-203","found":true,"decision":"more_info","amount":0,"missing_documents":[],"reason":"The GPA is 2.4, below the required 2.67. Please raise the GPA to at least 2.67 before applying again."}
```

Paste the full reply for **E-07 (the Kazakh enquiry)** from the bilingual
clerk, so the `reason` language is visible:

```
{"applicant_id":"A-201","found":true,"decision":"granted","amount":250000,"missing_documents":[],"reason":"Сіз грант талаптарына сайсыз: GPA көрсеткіші 3.4, табыс санатыңыз 1 және қажетті құжаттарыңыз толық. Грант мөлшері — 250 000 теңге."}
```

For comparison, the policy officer answered the same Kazakh enquiry in English:
`"reason":"GPA 3.4, income band 1, and both required documents are on file."`

### Written answers

**1. Which fields are role-sensitive and which are not?** Point at rows in your
tables.

> *The decision field is the most role-sensitive field.*
> The front_desk changed `refused` to `more_info` in E-03, E-04 and E-09 because it cannot refuse applications. 
> The auditor changed `granted` to `more_info` in E-01, E-05, E-06 and E-07 because it cannot grant applications.
>
> *The amount field changed only with the decision.*
> In E-01, E-05, E-06 and E-07, the amount became 0.
>
> *The found field was not role-sensitive.*
> It did not change because it depends on the records, not the role.
>
> *The missing_documents field changed only in E-08.*
> The front_desk and bilingual_clerk listed `transcript` and `id_card` for a person not found in the records. This may be related to the front_desk role, while for the bilingual_clerk it was an error.
>
> The bilingual_clerk also changed the `reason` field and used Kazakh in E-07. However, language was not fully controlled by the role, since the front_desk and auditor also used Kazakh.

**2. Which enquiries are most sensitive to the role, and why those?** Say what
E-03, E-04, E-07 and E-10 are each testing.

> *The most role-sensitive enquiries were the clear refusal and grant cases.*
> These are E-03, E-04, E-09 and E-01, E-05, E-06, E-07, because the front_desk and auditor changed the `decision` field. 
> E-02 and E-10 did not change because `more_info` was already the expected answer.

> **E-03** tests a refusal because of a low GPA (2.4 instead of 2.67). 
> The front_desk changed it to `more_info`, even though the problem cannot be fixed by providing a document.

> **E-04** tests a refusal because of income band 3. 
> The front_desk again changed it to `more_info`, although the applicant does not meet the required income band.

> **E-07** tests a Kazakh-language enquiry. 
> All roles found the correct person, so the language did not affect the lookup. 
> The auditor changed the `decision`, not because of the language.

> **E-10** tests a claim that an ID card was already uploaded. 
> All roles kept `more_info` because the record did not show the upload.


**3. Where does discretion belong — the role paragraph, or code that reads
`decision` afterwards?** Say what a downstream program can and cannot tell
about which role produced a record.

> *I think discretion should be handled in code.*
> A program can see only the output fields, not the role that produced them.
> For example, E-01 and E-03 both returned `found: true`, `decision: more_info`, `amount: 0` and `missing_documents: []`, 
> even though one case should be granted and the other refused. Only the `reason` was different.

> Therefore, a downstream program cannot know the real decision or which role produced the record.
> A better design is to keep the actual decision in the data and let code apply role-specific behaviour. 
> If the role is needed later, it should also be stored in the record.


**4. Is a role a boundary?** Say in Week 2 terms what the role paragraph is
made of, and what you would put in code — not in the prompt — if a wrong
`decision` were expensive.

> No. The role paragraph is just tokens at the start of the context. 
> The model reads them together with the records and the applicant's message, and it continues the text.
> It does not follow them like a program follows code.
> My run shows this. The bilingual clerk was told to decide exactly like a strict policy officer, 
> but on E-08 it listed `transcript` and `id_card` as missing documents for a person who is not in the records, while the policy officer returned `[]`. 
> So the same instruction did not give the same answer.
> Also, on E-07 the front desk and the auditor wrote the reason in Kazakh, although nobody told them to do this. 

> A role makes some answers more likely, it does not make other answers impossible.

> If a wrong `decision` were expensive, I would put these checks in code:
> 1. compute the rule myself from `records.json` (GPA > 2.67, band 1 or 2, both documents) and compare it with the model's `decision`;
> 2. take `amount` and `missing_documents` from the records, not from the model;
> 3. maybe send every case where the code and the model disagree to a human.

---

## Sublab Medium — memory you choose

### Tokens per call

| Call | A — never compressed | B — compressed at the `compress` turn |
|---|---|---|
| 1 | 802 | 802 |
| 2 | 913 | 882 |
| 3 | 1029 | 962 |
| 4 | 1134 | 1047 |
| 5 | 1230 | 1138 |
| 6 | 1343 | 1224 |
| 7 | 1457 | 1314 |
| 8 | 1569 | 1405 |
| 9 | 1696 | 1499 |
| 10 | — (compress skipped) | 2098 (the compress call) |
| 11 | 1806 | 1189 |
| 12 | 1897 | 1265 |
| **peak** | 1897 | 2098 |
| **total for the run** | 14876 | 14825 |

### Probes after the conversation

Each probe is asked separately, from the memory at the end of the run. It is
not added to the history, so one probe cannot help another. A probe is
"retrieved" if the reply contains one of the `expect_contains` strings.

| Probe | Tests | A retrieved? | A answer | B retrieved? | B answer |
|---|---|---|---|---|---|
| Q-1 identity | turn 1 | yes | Сіз — Daniyar Qoshan, өтініш нөміріңіз A-202. | yes | You are Daniyar Qoshan, applicant A-202. Your id card is still missing from the file. |
| Q-2 missing document | turn 5 | yes | Файлыңызда жеке куәлік құжаты әлі жетіспейді. | yes | Your id card is still missing from your file; your transcript is already on record. |
| Q-3 band and amount | turns 3–4 | yes | Сіздің табыс санатыңыз — 2. Барлық талап орындалса, осы санат үшін грант мөлшері 150000 теңге болады; қазір жеке куәлік құжаты жетіспейді. | yes | Your income band is 2. If you provide the missing id card and meet all requirements, the grant amount would be 150,000 tenge. |
| Q-4 the constraint | turn 6 | **no** | Кеңсеге келетін апта күні туралы ақпарат жазбада көрсетілмеген. Сіздің файлыңызда жеке куәлік әлі жетіспейді. | **no** | The records do not specify which day the office accepts documents. Your id card is still missing from the file. |
| Q-5 the open question | turn 7 | yes | You asked whether a scanned letter from your employer would count or whether the original was required. | yes | You asked whether a scanned letter from your employer would be accepted or whether the original is required. The record does not specify this. |
| **retrieved** | | 4/5 | | 4/5 | |

### The state my compression produced

```json
{
  "applicant_id": "A-202",
  "topic": "Study grant eligibility and application requirements",
  "facts": [
    "The applicant's name is Daniyar Qoshan.",
    "The applicant stated applicant ID A-202.",
    "The applicant stated that they sent their transcript last week.",
    "The applicant stated that their income band is 2 and that their family's certificate says so.",
    "The applicant could not upload their id card because the scanner at home broke.",
    "The applicant can only come to the office on Thursdays because they have lab all week otherwise.",
    "The applicant has a sister named Aruzhan who applied last year and is on file."
  ],
  "decisions": [
    "The office said the applicant's record was found.",
    "The office said the transcript is on file and the id card is missing.",
    "The office said the applicant otherwise meets the GPA and income requirements.",
    "The office said the conditional grant amount for income band 2 would be 150,000 tenge.",
    "The office said the record does not specify whether a scanned employer letter is accepted.",
    "The office said the record does not specify whether a decision is made the same day.",
    "The office said Aruzhan Nurlan is on file but the family relationship is not verified."
  ],
  "constraints": [
    "The id card must be on file before the application can be reviewed for approval.",
    "The applicant can bring the id card on Thursday."
  ],
  "open_questions": [
    "Does a scanned letter from the applicant's employer count, or must it be the original?",
    "If the applicant brings the id card on Thursday, will the decision be made the same day?"
  ],
  "language": "English and Kazakh"
}
```

### What happened in `--interactive` mode

```
you> hi, i am Aigerim Serik, A-201
office> You qualify for the grant. The awarded amount is 250,000 tenge.
   [sent 794 tokens; memory now holds 2 turn messages]

you> I can only come to the office on Mondays after 3 pm.
office> Noted: you can come to the office on Mondays after 3 pm.
   [sent 865 tokens; memory now holds 4 turn messages]

you> Can my mother bring the documents instead of me?
office> The record does not specify whether your mother may submit the documents on your behalf. Please confirm this with the grant office.
   [sent 931 tokens; memory now holds 6 turn messages]

you> tokens
Last call: sent 931 tokens, got back 190, total 1121

you> compress
!! Compression FAILED - the history is kept. Reason: 'topic' is a required property
(compress call sent 1513 tokens)

you> When can I come to the office?
office> The record does not specify office hours. Please contact the grant office to confirm when you can visit.
   [sent 1002 tokens; memory now holds 8 turn messages]

you> What did I ask about my mother?
office> You asked whether your mother can bring the documents to the office instead of you.
   [sent 1069 tokens; memory now holds 10 turn messages]

you> token
office> Please clarify what you mean by “token”.
   [sent 1125 tokens; memory now holds 12 turn messages]

you> tokens
Last call: sent 1125 tokens, got back 104, total 1229

you> exit
```


**Compression failed.** I forgot the `topic` field, so my program
   did not accept the state. The history was kept: 6 messages before
   `compress` and 8 after the next turn. I think the reason is my prompt:
   `topic` is in the schema, but I did not write a rule for it like for the
   other fields. In the scripted run the model added `topic` by itself, so it
   makes this mistake only sometimes. This is why the check is important.
 **Same problem as Q-4, but without compression.** In turn 2 the model
   said "Noted: you can come to the office on Mondays after 3 pm". But later,
   when I asked "When can I come to the office?", it said "The record does
   not specify office hours". The whole chat was still in memory, so the
   model had the answer but did not use it. I think it only looked at the
   records, because my prompt says they are "the only source of truth". So
   Q-4 was lost because of my prompt, not because of compression.

### Written answers

**1. What did compression buy?** Peak tokens both ways, probes retrieved both
ways, and — if a probe was lost — which one and which turn it came from.

> *Compression made the later calls shorter, but it did not save many tokens in total.*
> In Run A, the maximum was 1897 tokens. After compression, the calls were 1189 and 1265 tokens instead of 1806 and 1897. 
> So, the later calls used about 34% fewer tokens. 
> However, the total was almost the same: 14876 tokens in A and 14825 in B, because the compression call itself used 2098 tokens.

> *Compression did not cause any probe loss.*
> Both runs got 4/5 probes. Both lost **Q-4** (Thursday, turn 6). 
> The fact was still in the memory after compression, so the problem was probably the prompt, not compression. 
> The model treated the records as the only source of truth.
> 
> Q-2 and Q-3 worked in both runs because the needed information was still available in the records.


**2. ****Why must the state be structured rather than a paragraph?** You could have
asked for "a summary". Say what changes when the summary is an object with
named fields.

> *The state should be structured because it is easier to check and use.*
> First, code can check a structured state. My program checks that it is valid JSON and has all seven required fields.
> If the check fails, the old history is kept. This happened in my test when `topic` was missing. 
> A normal paragraph cannot be checked as easily.

> Second, field names show the model what information is important. 
> For example, `open_questions` helped keep the unanswered questions from turns 7 and 8, so Q-5 was retrieved after compression.

> Third, code can directly read a field such as `applicant_id` without asking the model again.


**3. What is missing from your state that you would add?** Name what you would
add and what you would drop to pay for it.

> *I would add two fields to the state.*
> First, I would add a `source` for each fact, such as "said by the applicant" or "from the record". 
> This could help with cases like Q-4, where the model ignored the Thursday information because it trusted only the records.

> I would also add `people_mentioned` to keep people like Aruzhan separate from the other facts.

> I would also remove `topic` because the topic is always the grant in this task.


**4. When is compression the wrong choice?** Name a conversation where it would
lose something that cannot be recovered, and say whether your program would
notice.

> Compression is a bad choice when the exact words are important. 
> For example, the applicant said, "I can only come on Thursdays", but the compressed state says the applicant "can" come on Thursday. 
> The word only is lost, so the meaning changes. After compression, the original message is deleted, so this information cannot be recovered. 

> The same problem can happen with an appeal, complaint or letter. A summary may keep only the main idea and lose the exact text. 
> Compression is also not very useful for a short chat. In my run, the total number of tokens was almost the same with and without compression. 
> My program would not notice these problems. It only checks the JSON structure and field types. 
> It does not check if the information is complete or correct, so the lost word only would pass the validation.

---

## Sublab Hard — stories in, CVs out, the best candidate by code

### Part 1 — extraction

| Story | Parsed? | Valid? | Fields that came back `null` | Traps hit |
|---|---|---|---|---|
| story-01 | yes | yes | none | none (normal case: GPA 3.8/4.0, 2 published papers, 8 months) |
| story-02 | yes | yes | graduation_year, gpa_4_scale, gpa_original, gpa_original_scale | **no GPA stated** → gpa null (not guessed from "diploma with distinction"). graduation_year is null because the story says only "last year", not a year |
| story-03 | yes | yes | none | **GPA on another scale** (4.6/5.0 → 3.68/4.0, original scale recorded); **paper not published** ("under review" not counted) |
| story-04 | yes | yes | none | **papers not published**: 1 published counted; 1 "under review" and 2 "in preparation" not counted |
| story-05 | yes | yes | none | story in Kazakh; 1 paper "being written, not submitted" not counted |
| story-06 | yes | yes | graduation_year, gpa_4_scale, gpa_original, gpa_original_scale | **story contradicts itself**: GPA 3.2 vs 3.5, and graduated 2024 vs graduating 2026 → both fields null, both contradictions in `ambiguities`; the poster is not counted as a publication |

All six replies parsed and all six were valid against my CV schema.

Paste the extraction for **story-06**, the one that contradicts itself:

```json
{
  "candidate_id": "story-06",
  "full_name": "Nurzhan Abilov",
  "degree": "BSc in Statistics",
  "graduation_year": null,
  "gpa_4_scale": null,
  "gpa_original": null,
  "gpa_original_scale": null,
  "languages": ["Kazakh", "Russian", "English"],
  "published_count": 1,
  "published_papers": ["Paper on survey weighting in a peer-reviewed proceedings"],
  "unpublished_papers": ["Poster at a local event"],
  "experience_months": 40,
  "experience_not_countable": [],
  "ambiguities": [
    "The GPA is stated as both 3.2 and 3.5.",
    "The story says the candidate graduated in 2024 but is also a final-year student graduating in 2026."
  ],
  "evidence": {
    "candidate_id": "candidate_id: story-06",
    "full_name": "# Nurzhan Abilov",
    "degree": "I graduated in 2024 with a BSc in Statistics.",
    "graduation_year": "I graduated in 2024 with a BSc in Statistics. ... I am currently a final-year student graduating in 2026",
    "gpa_4_scale": "My GPA was 3.2. Actually I should double-check that, I think it was 3.5",
    "gpa_original": "My GPA was 3.2. Actually I should double-check that, I think it was 3.5",
    "gpa_original_scale": "My GPA was 3.2. Actually I should double-check that, I think it was 3.5",
    "languages": "Languages: Kazakh, Russian, English.",
    "published_count": "one paper published, in a peer-reviewed proceedings, on survey weighting",
    "published_papers": "one paper published, in a peer-reviewed proceedings, on survey weighting",
    "unpublished_papers": "One poster at a local event, which I do not think counts.",
    "experience_months": "I have been at an insurance analytics team since February 2023, which is about forty months.",
    "experience_not_countable": "",
    "ambiguities": "My GPA was 3.2. Actually I should double-check that, I think it was 3.5 ... I graduated in 2024 ... I am currently a final-year student graduating in 2026",
    "evidence": "I know the application asks for one number for grades and one for months."
  }
}
```

### Part 2 — scores and the winner

The model returned only the three scores (as JSON fields). My code computed
the total: `0.5 * academic + 0.3 * research + 0.2 * experience`, rounded to
two decimals (`weighted_total()` in `cv_extract_and_rank.py`), and sorted the
candidates.

| Candidate | academic (0–5) | research (0–5) | experience (0–5) | weighted total (code) |
|---|---|---|---|---|
| story-01 (Aziza Bekova) | 5 | 5 | 2 | 4.4 |
| story-02 (Dias Yerzhanov) | 1 | 2.5 | 5 | 2.25 |
| story-03 (Lyazzat Omarova) | 4.9 | 2.5 | 2.9 | 3.78 |
| story-04 (Tamerlan Saparov) | 4 | 3 | 5 | 3.9 |
| story-05 (Aisha Nurlankyzy) | 5 | 2.5 | 1.25 | 3.5 |
| story-06 (Nurzhan Abilov) | 2 | 2.5 | 5 | 2.75 |

Ranking computed by my code:
1. story-01 (Aziza Bekova) = 4.4
2. story-04 (Tamerlan Saparov) = 3.9
3. story-03 (Lyazzat Omarova) = 3.78
4. story-05 (Aisha Nurlankyzy) = 3.5
5. story-06 (Nurzhan Abilov) = 2.75
6. story-02 (Dias Yerzhanov) = 2.25

**Winner, computed by my code:** story-01 (Aziza Bekova), total 4.4

**The model's prose answer, asked separately ("who should win?"):**

```
Scores: Aziza Bekova—academic 5, research 5, experience 2; Dias Yerzhanov—academic 0, research 2.5, experience 5; Lyazzat Omarova—academic 4, research 2.5, experience 5; Tamerlan Saparov—academic 4, research 2.5, experience 5; Aisha Nurlankyzy—academic 5, research 2.5, experience 1; Nurzhan Abilov—academic null because of contradictory grade and enrollment information, research 2.5, experience 5. The weighted total and winner should be computed by the specified code.
```

The model did not name a winner in prose. In the prose call I sent the whole
`candidate_rubric.json`, including `rule_for_the_ranking` ("the winner is
computed in code"), and the model followed that rule

### Part 3 — written answers

### Part 3 — written answers

**1. Which rule did you have to add, and what broke without it?** Name the
story that forced it.

> I added two rules before my first run. They are in `EXTRA_RULES` in my code.
> - Rule 7: write all fields in English, but keep the quotes in the original
>   language. I added it because of **story-05**, which is in Kazakh. Without
>   this rule the fields could be in Kazakh, and I could not compare them with
>   the other CVs. In my run the fields came back in English and the quotes
>   stayed in Kazakh.
> - Rule 8: part-time months count as full months. I added it because of
>   **story-02**, where two of the three years were part-time. In my run the
>   model counted all 36 months.
>
> I also found a rule that is still missing. The rubric says "no GPA = 0 on
> academic", and this was in my scoring prompt. But **story-02** (no GPA) got
> academic = 1. So the model broke the rule even though it was in the prompt.
> I think this rule should be checked in code: if `gpa_4_scale` is null and
> there is no contradiction, academic = 0.

**2. Where did the model guess, and where did your code have to decide?** One
example of each, from your run.

> **The model guessed** in the scores. Five candidates (story-02 to story-06)
> have one published paper each, so they should get the same research score.
> Four of them got 2.5, but **story-04 (Tamerlan) got 3**. I think the model
> was influenced by his three unpublished papers, but they should not count.
> This small guess (+0.15 to the total) decided second place: Tamerlan got 3.9
> and Lyazzat got 3.78. With 2.5, Tamerlan would have 3.75 and be third.
>
> **My code decided** the total and the winner. The model only gave three
> numbers. My function `weighted_total()` calculated the total with the
> weights 0.5, 0.3 and 0.2, and `sorted()` made the ranking. The model did not
> calculate any total and could not change the weights.

**3. Did your prose ranking and your computed ranking agree?** Say which one
you trust and why — and if they agreed, what you would need to see before
trusting the prose one alone.

> The model did not name a winner in prose. It only gave its own scores and
> wrote that the winner "should be computed by the specified code". This was
> my mistake: I sent the whole rubric, and the rubric says the winner is
> computed in code. Next time I would send only the criteria.
>
> But the prose answer was still interesting, because the scores were
> different from the scoring calls, with the same model:
> - Lyazzat: experience 5 in prose, 2.9 in scoring. She has only 14 months,
>   and 5 needs two years, so 5 is wrong.
> - Dias: academic 0 in prose (correct), 1 in scoring.
> - Tamerlan: research 2.5 in prose, 3 in scoring.
>
> If I use the prose scores, Aziza is still first (4.4). But Lyazzat and
> Tamerlan are tied (3.75), and Nurzhan cannot be ranked (academic null).
>
> I trust my computed ranking more. Each score is a field, the formula is in
> my code, and I can check every step. The same model gave different numbers
> for the same person in two calls, so I cannot trust a number inside a
> sentence. To trust the prose answer, I would need to see the same winner
> and the same scores in several runs, and the scores should match the CVs.

**4. The rubric has no anchor for a contradicted field.** The stories say 3.2
and then 3.5; the rubric defines a 0 and a 5 and nothing in between for this
case. Say what you did and what the rule should be.

> What I did: the extraction followed the rule. For story-06 the GPA is null,
> and the contradiction (3.2 vs 3.5) is written in `ambiguities`. I did not add
> a special rule for scoring, so the model decided by itself and gave
> **academic = 2**. This is not 0 (like "no GPA"), and it is not what 3.2 or
> 3.5 would get (about 4, like Tamerlan with 3.6). The model just picked a
> number. In the prose call it wrote "academic null" instead.
>
> What the rule should be: a contradicted GPA is not the same as no GPA, so it
> should not get 0. I think the fair rule is to use the lower number (3.2),
> mark the candidate as "needs checking", and ask for the transcript if it can
> change the winner. This rule should be in code, so it gives the same result
> every time. In my run it does not change the winner: Nurzhan is fifth
> anyway.

**5. How close were your top two candidates?** If they were within 0.05, say
what you would tell the committee and what you would change in the extraction
to make that call defensible.

> My top two were story-01 (Aziza, 4.4) and story-04 (Tamerlan, 3.9). The gap
> is 0.5, so it is not within 0.05 and the winner is clear. The difference is
> research: Aziza is the only one with two published papers, so she got 5.
>
> But second and third place were close: Tamerlan 3.9 and Lyazzat 3.78, a gap
> of 0.12. This gap comes from the guessed research score (3 instead of 2.5).
> If the committee needed a second place, I would tell them this order is not
> reliable. To make it better, I would calculate the research and experience
> scores in code from `published_count` and `experience_months`, with fixed
> rules, and let the model decide only what really needs judgement.

---