# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

1. A writer sends `{"text": ..., "creator_id": ...}` to `POST /submit`.
2. The route (`app.py::submit`) checks the input. Missing or empty `text` or
   `creator_id` gets a `400`, text over 20,000 characters gets a `413`, and text
   too short to score gets a `400`. Every refusal is written to the audit log with
   `audit.log_rejection`, so it leaves a trace.
3. **Signal one** — `detector.model_signal(text)` runs gpt2 on my own machine and
   measures how predictable the text is (perplexity), turned into a 0–1 score.
4. **Signal two** — `stylometry.style_signal(text)` measures the shape of the text:
   how much sentence length varies, how varied the vocabulary is, and how much
   expressive punctuation it uses. That also becomes a 0–1 score.
5. `scoring.combine_signals` merges them into one combined score (higher = more AI-like).
6. `scoring.score_to_label` turns that score into a guess (`human` / `unsure` / `ai`)
   and a plain-language sentence the writer reads.
7. `audit.log_decision` appends the decision — timestamp, content_id, creator_id,
   guess, both signal scores, combined score, label, status `decided` — to
   `logs/audit.jsonl`, and the response goes back with all of those fields.
8. If the writer disagrees, `POST /appeal` with the `content_id` and their reasoning
   appends an appeal entry and moves the item to `under_review`. The original
   decision is never overwritten.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (gpt2), as
perplexity. Low perplexity = "I could have guessed every word" = higher score. It's
squashed onto 0–1 with a logistic curve centred on perplexity 45 (the starter's
midpoint, which I left unchanged).

**Why that might differ between human and AI writing:** A language model writes by
repeatedly choosing a likely next word, so its output is text a model finds easy to
predict. People make odder, more specific choices.

**What it can't see:** Who actually wrote it. Predictability is not authorship. Plain
writing — short sentences and common words, the way a second-language writer or a
younger writer often writes — is just as predictable as machine text. My plain
human calibration paragraph scored **0.823**, higher than one of my AI samples
(0.754). The reverse also happens: lightly edited AI text with a few casual words
dropped to **0.332**.

### Signal two — the style signal

**What it measures:** Three measures of the text's shape, each flipped and scaled to
0–1 "AI-likeness" and then weighted:

| Measure | How | AI end → 1.0 | Human end → 0.0 | Weight |
|---|---|---|---|---|
| Sentence-length spread | stdev ÷ mean of sentence lengths | 0.20 | 0.80 | 0.45 |
| Expressive punctuation | `; : — – ( ) ? !` and quotes, per word | 0.00 | 0.08 | 0.35 |
| Vocabulary variety | type-token ratio averaged over 50-word windows | 0.72 | 0.92 | 0.20 |

I picked the anchor points from the raw values on my calibration texts. Vocabulary
gets the smallest weight because it barely separated the groups: one AI sample had
more varied vocabulary (0.91) than my clearly human sample (0.85). A one-sentence
text has no spread to measure, so that part counts as neutral (0.5).

**Why that might differ between human and AI writing:** Generated prose tends to march
in even, mid-length sentences and lean on full stops and commas. Human writing is
lumpier: a three-word sentence next to a forty-word one, a dash, a question.

**What it can't see:** Meaning. It can't read at all. Adding typos, chopping up
sentences, or throwing in a few dashes and questions moves it without changing who
wrote the text. Simple, even human writing also looks "machine-like" to it: my
plain human paragraph scored **0.901**.

### The combining rule

**The rule:** A weighted average that leans on the model signal, with one guard: **if
the two signals disagree by more than 0.40, the system won't accuse anyone.** The
combined score is then capped just below the AI threshold, so the worst result is
"unsure". Two methods disagreeing is itself uncertainty.

**The numbers:** `combined = 0.6 × model_score + 0.4 × style_score`. If
`|model_score − style_score| > 0.40`, `combined = min(combined, 0.69)`. Weights,
gap and thresholds all live in `config.py` (`WEIGHT_MODEL_SIGNAL`,
`WEIGHT_STYLE_SIGNAL`, `DISAGREEMENT_GAP`, `HUMAN_THRESHOLD`, `AI_THRESHOLD`).

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

My clearly human paragraph (about my grandmother's button jar — dashes, a question,
a semicolon, one four-word sentence next to a thirty-word one) scored
**model 0.483 / style 0.069**. The model found it fairly predictable, but its shape
is very human. That's a gap of 0.41, so the guard kicks in. The weighted average
was already low (0.318), so the cap didn't change anything, and it's labelled
**human**. If the split ran the other way (model 0.95, style 0.30, average 0.69), the
guard would hold it at "unsure" instead of letting one signal accuse the writer
alone.

**Calibration results** (all real runs):

| Input | model | style | combined | label |
|---|---|---|---|---|
| Clearly AI (time-management essay) | 0.754 | 0.598 | 0.692 | unsure |
| Clearly AI (social-media essay) | 0.900 | 0.842 | 0.877 | **AI** |
| Clearly human (button jar) | 0.483 | 0.069 | 0.318 | **human** |
| Plain human (soccer, second-language style) | 0.823 | 0.901 | 0.854 | **AI — false positive** |
| Formal human (committee/plasterwork) | 0.237 | 0.236 | 0.236 | **human** |
| Lightly edited AI | 0.332 | 0.524 | 0.409 | unsure |

The plain human paragraph is the failure this project is about: **both** signals
read plain writing as machine-like, so the disagreement guard can't catch it. The
only protection it gets is the wording of the AI label and the appeal path. That's
the first thing unit 8 should go after.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | This reads like writing by a person. Our checks found nothing that suggests it was generated by AI. |
| unsure | above 0.35, below 0.70 | We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything — and you can ask for a person to review it. |
| high-confidence AI | 0.70 – 1.00 | Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it. |

The ranges cover every score from 0 to 1 with no gaps (`scoring.py::score_to_label`
checks `>= 0.70` first, then `<= 0.35`, and everything else is unsure). The unsure band is
wider on the AI side (0.35–0.70) than on the human side, because a wrong "AI" label
costs a writer much more than a wrong "human" label costs the site. `confidence` in
the response is the distance from the middle: `0.5 + |score − 0.5|`.

**Why I worded the "unsure" one this way:**

The person reading it may well have written every word. So it says what happened
("we couldn't tell"), puts the limitation on *our checks* rather than their
writing, says outright that it isn't a judgement about them, and tells them they
don't have to do anything. It mentions review as an option, not a demand. It never
says "AI", so a writer skimming it doesn't come away feeling accused.

---

## Sample Run

This is the plain-language paragraph from the calibration table: a human-written
piece that my system wrongly labels AI, followed by the appeal against it.

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I like to play soccer with my friends after school. We play in the park near my house. My best friend is Ahmed. He is very fast and he scores many goals. I am not so fast but I am good at defense. Sometimes we play until it is dark. Then my mother calls me to come home for dinner. I think soccer is the best sport.", "creator_id": "student_42"}'
```

```json
{
  "combined_score": 0.8543,
  "confidence": 0.8543,
  "content_id": "195763d0-c13e-4da3-89cc-d0cdb28d709c",
  "guess": "ai",
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "model_score": 0.823,
  "status": "decided",
  "style_score": 0.9013
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "195763d0-c13e-4da3-89cc-d0cdb28d709c", "reasoning": "I wrote this myself for my English class. I write in simple sentences because English is my second language."}'
```

```json
{
  "appealed_at": "2026-11-03T04:52:52+00:00",
  "content_id": "195763d0-c13e-4da3-89cc-d0cdb28d709c",
  "message": "Thanks — your appeal is recorded and a person will review this decision.",
  "original_label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "missing_creator_id",
      "status": "rejected",
      "timestamp": "2026-11-03T04:52:46+00:00"
    },
    {
      "combined_score": 0.8543,
      "content_id": "195763d0-c13e-4da3-89cc-d0cdb28d709c",
      "creator_id": "student_42",
      "guess": "ai",
      "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
      "model_score": 0.823,
      "status": "decided",
      "style_score": 0.9013,
      "timestamp": "2026-11-03T04:52:52+00:00"
    },
    {
      "content_id": "195763d0-c13e-4da3-89cc-d0cdb28d709c",
      "creator_id": "student_42",
      "event": "appeal",
      "reasoning": "I wrote this myself for my English class. I write in simple sentences because English is my second language.",
      "status": "under_review",
      "timestamp": "2026-11-03T04:52:52+00:00"
    }
  ]
}
```

The first entry is a request with no `creator_id` that the route refused. It was
logged as a rejection instead of disappearing. The decision and the appeal sit one
after the other: the original "ai" decision is still there, and the appeal
after it moves the item to `under_review`.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked Claude Code to help me set up the project environment and get python test.py to pass.
- *What came back:* Claude Code found that my virtual environments were using Python 3.14, which was not supported by the project. It helped set up Python 3.12, install the required libraries, and download the GPT-2 model.
- *What I changed:* I switched to a compatible Python environment and used the updated setup to run my project. I also checked that the required packages were installed and that the tests could run successfully. This helped me understand why using the correct Python version is important.

**Moment 2**

- *What I asked for:* I asked Claude Code to help me build the style signal and combine it with the AI detector score.
- *What came back:* Claude Code analyzed six sample texts and compared their writing patterns. It found that vocabulary variety was not very useful for separating AI and human writing. It suggested using 60% for the model signal and 40% for the style signal, along with a rule for handling disagreement.
- *What I changed:* I used the calibration results to evaluate the suggested weights and scoring rules. I kept the 60/40 combination and the disagreement rule to reduce the risk of incorrectly labeling human writing as AI. I also reviewed the test results and noticed that simple human writing could still be incorrectly classified. This showed me why the system needs an unsure label and an appeal option.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 60 per day (`config.py`: `RATE_LIMIT_PER_MINUTE`,
`RATE_LIMIT_PER_DAY`), on `POST /submit` only.

**Why those numbers and not others:**

- **A real writer** submits a finished piece, reads the label, maybe edits and
  resubmits. Even someone pasting several chapters back to back doesn't need more
  than 5 in one minute, and 60 in a day is more than a full day of real work. A
  limit of 1–2 per minute would trip on an honest writer resubmitting after a fix.
- **A script mapping my thresholds** needs hundreds of variations to find where
  "unsure" turns into "AI" (0.70) or where the disagreement guard (0.40 gap)
  kicks in. At 60 a day per creator it gets 60 data points before it's cut off,
  so mapping the bands takes days instead of a minute. The per-minute limit
  stops the burst; the per-day limit stops the slow drip that stays under 5/min.
- Each submission also runs gpt2 inline (a second or two of CPU), so a flood is a
  cost problem as well as a probing problem. 5/min per caller keeps one caller
  from hogging the model.

**What a caller counts as:** the `creator_id` in the request body, falling back to
the IP address when the body has no usable `creator_id` (`app.py::rate_limit_key`).
That's the weak point: a script that invents a new `creator_id` for every request
is a "new caller" every time and is never limited. The attack set does exactly
this — every row in `attacks.csv` has its own `creator_id` — which is why only the
`flood_same_creator` rows can trip it. Per-address limiting would catch that
script but would also lump a whole classroom or household behind one IP together.
A real deployment would need both, plus accounts so `creator_id` can't be made up.

**Every refusal is logged.** The starter's 429 handler writes `rate_limited`
rejections. I also log every refusal my own routes make with `audit.log_rejection`
— `missing_text`, `missing_creator_id`, `text_too_long`, `text_too_short` on
`/submit`, and (new this unit) the 400/404 refusals on `/appeal` — each with its
`status_code`.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15` (full output in `results/flood_2026-11-10_0138.md`):

```
  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  ...
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================

10 of 15 were rate limited.
```

`GET /health` afterwards: `{"detector_loaded":true,"detector_model":"gpt2","log_entries":30,"ok":true,"rate_limiting":true}`

One of the ten rejection entries it left in `logs/audit.jsonl`:

```json
{"timestamp": "2026-11-10T06:38:56+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

---

## Attack Run — Before

`python run_attacks.py --set attack_set --label before`. Rate limiting on (5/min, 60/day),
nothing else changed since unit 7. Raw output: `results/attack_run_2026-11-10_0144_before.md`;
the audit-log slice for the run: `results/audit_attack_run_before.jsonl`; my held/broke
calls: `results/verdicts_before.json`.

The runner's "Score" column is `confidence`, not the combined score, so I pulled
`model`, `style` and `combined` for every row from the audit log by `content_id`.

**How I judged held/broke.** An attack *broke* if it got where its `targets` column
said it was going:

- **evasion** — the AI paragraph every evasion is built on scores **0.722 → ai**
  unmodified (I scored it directly: model 0.669, style 0.800). An evasion broke if it
  moved that text out of the AI band (below 0.70). Landing in "unsure" counts, because
  "unsure" is exactly what stops the system from flagging it.
- **false_positive** — broke if real human writing got the **ai** label. "Unsure" is
  not an accusation, so it held.
- **prompt_injection** — broke if the text got what the injection asked for (a
  **human** label, or hostile content in the label or log).
- **malformed** — broke on a 5xx, *or* on a 200 that hands down a verdict about
  something that isn't writing in a language my model reads.
- **flood** — held if the limiter cut it off and every rejection was logged.

| ID | Family | Targeting | HTTP | model | style | combined | Label | Held/Broke | Note |
|---|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | 0.164 | 0.800 | 0.418 | unsure | **BROKE** | AI text left the AI band (base paragraph scores 0.722 → ai) |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | 0.594 | 0.232 | 0.449 | unsure | **BROKE** | left the AI band |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | 0.666 | 0.370 | 0.548 | unsure | **BROKE** | left the AI band |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | 0.611 | 0.800 | 0.687 | unsure | **BROKE** | left the AI band, but only just (0.687) |
| EV05 | evasion | both signals: heavy human editing pass | 200 | 0.321 | 0.451 | 0.373 | unsure | **BROKE** | left the AI band |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | 0.573 | 0.421 | 0.512 | unsure | **BROKE** | left the AI band |
| EV07 | evasion | signal two: padding with punctuation | 200 | 0.586 | 0.334 | 0.485 | unsure | **BROKE** | left the AI band |
| EV08 | evasion | signal one: text below the token window | 200 | 0.245 | 0.738 | 0.442 | unsure | **BROKE** | two sentences, still scored instead of refused |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | 0.704 | 0.442 | 0.599 | unsure | **BROKE** | left the AI band |
| EV10 | evasion | signal two: repeated stanza structure | 200 | 0.979 | 0.855 | 0.929 | ai | **HELD** | still labelled ai |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | 0.618 | 0.721 | 0.659 | unsure | **HELD** | unsure, not accused |
| FP02 | false_positive | human writing in a formal register | 200 | 0.739 | 0.920 | 0.811 | ai | **BROKE** | human writing labelled ai |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | 0.805 | 0.804 | 0.805 | ai | **BROKE** | non-native writer labelled ai |
| FP04 | false_positive | a student essay written to a rubric | 200 | 0.833 | 0.774 | 0.809 | ai | **BROKE** | human writing labelled ai |
| FP05 | false_positive | technical documentation written by a person | 200 | 0.800 | 0.942 | 0.857 | ai | **BROKE** | human writing labelled ai |
| FP06 | false_positive | a person imitating a formal template | 200 | 0.881 | 0.725 | 0.819 | ai | **BROKE** | human writing labelled ai |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | 0.882 | 0.602 | 0.770 | ai | **BROKE** | human writing labelled ai |
| FP08 | false_positive | very short genuine human submission | 200 | 0.322 | 0.625 | 0.444 | unsure | **HELD** | unsure, not accused |
| PI01 | prompt_injection | instruction to ignore the check | 200 | 0.463 | 0.453 | 0.459 | unsure | **HELD** | not labelled human |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | 0.204 | 0.364 | 0.268 | human | **BROKE** | labelled human |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | 0.594 | 0.454 | 0.538 | unsure | **HELD** | not labelled human |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | 0.500 | 0.369 | 0.448 | unsure | **HELD** | label is a fixed string; the script is never echoed back |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | 0.640 | 0.246 | 0.483 | unsure | **HELD** | log line stays one valid JSON object; guess is unsure, not the injected human |
| PI06 | prompt_injection | instruction plus real human text | 200 | 0.558 | 0.723 | 0.624 | unsure | **HELD** | not treated as verified; unsure |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | **HELD** | 400 missing_text |
| MF02 | malformed | text is a single character | 400 | — | — | — | — | **HELD** | 400 text_too_short |
| MF03 | malformed | text is control characters | 200 | 0.000 | 0.575 | 0.230 | human | **BROKE** | control codes scored and labelled human |
| MF04 | malformed | text is only punctuation | 200 | 0.011 | 1.000 | 0.407 | unsure | **BROKE** | punctuation-only scored as writing |
| MF05 | malformed | text is a very long single word | 200 | 0.998 | 0.575 | 0.690 | unsure | **BROKE** | one 'word' scored as writing |
| MF06 | malformed | text is emoji only | 200 | 0.997 | 0.775 | 0.908 | ai | **BROKE** | emoji labelled ai |
| MF07 | malformed | text is right-to-left script | 200 | 0.906 | 0.775 | 0.854 | ai | **BROKE** | a real Arabic sentence labelled ai |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | — | — | **HELD** | 413 text_too_long |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | **HELD** | 400 |
| RQ02 | malformed | no creator_id | 400 | — | — | — | — | **HELD** | 400 |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | **HELD** | 400 |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | **HELD** | 400 |
| RQ05 | malformed | text is null | 400 | — | — | — | — | **HELD** | 400 |
| RQ06 | malformed | creator_id is an object | 400 | — | — | — | — | **HELD** | 400 |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | **HELD** | 400 |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | **HELD** | 400 |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | **HELD** | 400 |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | — | — | **HELD** | refused with no crash, but by the limiter (429), not the route — see note |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | — | — | **HELD** | same as RQ10 |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | **HELD** | 400 |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | 0.029 | 0.575 | 0.247 | human | **HELD** | under the limit |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | 0.029 | 0.575 | 0.247 | human | **HELD** | under the limit |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | 0.029 | 0.575 | 0.247 | human | **HELD** | under the limit |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | 0.029 | 0.575 | 0.247 | human | **HELD** | under the limit |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | 0.029 | 0.575 | 0.247 | human | **HELD** | under the limit |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429, logged |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429, logged |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429, logged |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429, logged |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429, logged |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429, logged |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429, logged |

**Count: 35 held, 21 broke, 0 crashes.**

| Family | Held | Broke |
|---|---|---|
| evasion | 1 / 10 | 9 |
| false_positive | 2 / 8 | 6 |
| prompt_injection | 5 / 6 | 1 |
| malformed (MF text + RQ requests) | 15 / 20 | 5 |
| flood_same_creator | 12 / 12 | 0 |

Notes on rows that need one:

- **RQ10 and RQ11 got a 429, not a 400.** Neither body parses as JSON (form-encoded,
  and JSON sent as `text/plain`), so `rate_limit_key` had no `creator_id` and fell back
  to my IP address — the same bucket RQ02 and RQ06–RQ09 had already used up 5 of.
  They were refused and logged, so nothing crashed, but they never reached my route,
  and the log records them as `rate_limited` from `unknown` instead of what they
  actually were. One person with several bad requests can lock their own IP out.
- **The flood text itself was labelled human** (model 0.029). The limiter, not the
  detector, is what stopped that attack.
- **PI04 and PI05 held for structural reasons, not clever ones.** The label a writer
  sees is one of three fixed strings in `scoring.py`, so submitted text is never
  echoed into it; and `audit._append` writes with `json.dumps`, so the quote marks in
  PI05 are escaped and the line stays one valid object with `guess: "unsure"`.

**Ten audit log entries from the run** (plus two more), copied verbatim from
`logs/audit.jsonl`. Nine decisions chosen for the failures, three rejections — a
`400` from my route, a `400` for a body that's a JSON array, and a `429` from the
flood rows:

```json
{"timestamp": "2026-11-10T06:44:03+00:00", "content_id": "f21daea1-280f-4781-9861-fb0deae07df8", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.8, "combined_score": 0.4181, "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything — and you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:03+00:00", "content_id": "627fabef-87ec-44c1-a960-e0eda029be63", "creator_id": "attacker_EV05", "guess": "unsure", "model_score": 0.3212, "style_score": 0.4508, "combined_score": 0.373, "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything — and you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:03+00:00", "content_id": "1edbaa22-20ee-4e5e-829e-0f67c60beaac", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.8044, "combined_score": 0.8048, "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:03+00:00", "content_id": "61e77c13-7798-4e24-af03-8daf78551a46", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.9423, "combined_score": 0.8572, "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:04+00:00", "content_id": "2129a14a-556c-4ad8-9465-8ada43a0dd3a", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3639, "combined_score": 0.2682, "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:04+00:00", "content_id": "6997b4db-7f85-416d-9f14-5a17302b4df6", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.2464, "combined_score": 0.4826, "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything — and you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:04+00:00", "content_id": "8fadec1f-de27-4797-a414-20d978c75913", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.575, "combined_score": 0.23, "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:04+00:00", "content_id": "4324bc8b-3f89-4e25-b995-d3c5668045cb", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 0.775, "combined_score": 0.9081, "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:04+00:00", "content_id": "ab163629-42ce-44f4-8087-11113497d28d", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 0.775, "combined_score": 0.8538, "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-10T06:44:04+00:00", "creator_id": "attacker_RQ01", "event": "rejected", "status": "rejected", "reason": "missing_text", "status_code": 400}
{"timestamp": "2026-11-10T06:44:04+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "missing_creator_id", "status_code": 400}
{"timestamp": "2026-11-10T06:44:04+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

What they show, in order: **EV01** typos crashed the model signal to 0.164 while style
still said 0.80 — the opposite of what the attack targeted. **EV05** heavy human editing
pulled both signals down. **FP03** (non-native writer) and **FP05** (technical docs):
both signals *agree* the human writing is AI, so the disagreement guard never fires.
**PI02** got a human label. **PI05**'s injected `"guess": "human"` is inside the escaped
note text, not a field. **MF03** control codes were scored 0.000 by the model and labelled
human. **MF06** emoji and **MF07** Arabic were both labelled AI. Then the three rejections.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03 — a non-native English speaker writing carefully**, labelled **high-confidence AI**
(model 0.805, style 0.804, combined 0.805):

> I want to describe my experience of the first month in this country. The weather was
> very different from my home. I did not expect the rain to continue for so many days. ...

It's the same failure my unit 7 sample run found with my own plain soccer paragraph,
and now it's confirmed by text I didn't write. The person most likely to write like this
is the one least able to argue back, and both of my signals fail on them in the same
direction at once. MF07 is a close second: someone writing in Arabic gets accused of
using AI by a model that has never really read Arabic.

---

## Run Log and Verdicts

`python run_eval.py --label before`, run once, three trials per scenario, nothing changed
in between. Raw output: `results/run_2026-11-10_0221_before.md`. Scenarios: `scenarios.py`
(criterion 1 is ten short pieces I wrote myself; the AI texts were generated by Claude).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10 | 5/10 | 5/10 | 5/10 | **MISSED** |
| 2. Mean score gap, 5 clearly-AI vs 5 clearly-human | ≥ 0.30 | 0.086 (0.812 vs 0.726) | 0.086 | 0.086 | **MISSED** |
| 3. All three labels reachable across 6 spread inputs | 3 of 3 | 2/3 (no human) | 2/3 | 2/3 | **MISSED** |
| 4. Valid appeals → 200 + logged + `under_review`; unknown id → 404 | 5/5 and 404 | 5/5, 404 | 5/5, 404 | 5/5, 404 | **MET** |
| 5. Malformed requests → 4xx JSON, no 500 | 4/4, 0 × 500 | 4/4 (400,400,400,413) | 4/4 | 4/4 | **MET** |

**How I decided each verdict.** The target has to hold in *every* trial.
1. Counted `guess == "ai"` among the ten. 5 in every trial, against a target of at most 1.
2. `run_eval` doesn't return `combined_score`, so I recomputed it from each row's
   `model_score` and `style_score` with the same rule as `scoring.combine_signals`
   (the guesses it gives match the returned guesses on every row). AI mean 0.812, human
   mean 0.726: a gap of 0.086, well short of 0.30.
3. The six inputs gave `ai, unsure, unsure, ai, ai, ai`. "human" never appeared.
4. All five appeals returned `200` with status `under_review`, the log for each
   `content_id` read `["decided", "appeal"]`, and the unknown id got `404`, in all three trials.
5. Missing text `400`, empty text `400`, missing creator_id `400`, 25,000 chars `413`.
   All JSON, no `500`.

All three trials were identical, as expected: neither signal has anything random in it.

**Real output from one trial**, pasted as text. Produced by `run_eval.py::main` (and
`run_eval.py::run_appeals` for criterion 4) calling `app.py::submit` / `app.py::appeal`:

**Criterion 1 — `my own writing`, trial 1** (3 of 10 results shown; label text shortened with …):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8533,
    "model_score": 0.9013,
    "style_score": 0.7812,
    "label": "Parts of this look a lot like AI-generated writing. This is …",
    "sent": "I wake up at 6:30 am to get ready for college. I take the train, then "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.9,
    "model_score": 0.8333,
    "style_score": 1.0,
    "label": "Parts of this look a lot like AI-generated writing. This is …",
    "sent": "Life is too short to complain, and so we have to try our best to compl"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5202,
    "model_score": 0.5457,
    "style_score": 0.4819,
    "label": "We couldn't tell either way. Plenty of people write in a sty…",
    "sent": "Watching a movie with the family feels relaxing, with a warm bowl of s"
  }
]
```

**Criterion 2 — `AI side of spread`, trial 1** (1 of 5 results shown; label text shortened with …):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8744,
    "model_score": 0.9302,
    "style_score": 0.7907,
    "label": "Parts of this look a lot like AI-generated writing. This is …",
    "sent": "Renewable energy has become an increasingly important part of the glob"
  }
]
```

**Criterion 2 — `human side of spread`, trial 1** (1 of 5 results shown; label text shortened with …):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7532,
    "model_score": 0.6826,
    "style_score": 0.859,
    "label": "Parts of this look a lot like AI-generated writing. This is …",
    "sent": "I travel by train, and during my trip I read my class notes. If I get "
  }
]
```

**Criterion 3 — `label coverage`, trial 1** (2 of 6 results shown; label text shortened with …):

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6034,
    "model_score": 0.4331,
    "style_score": 0.8588,
    "label": "We couldn't tell either way. Plenty of people write in a sty…",
    "sent": "I tried to make pumpkin bread for the first time, but I forgot to add "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5254,
    "model_score": 0.6947,
    "style_score": 0.2715,
    "label": "We couldn't tell either way. Plenty of people write in a sty…",
    "sent": "Remote work has changed how a lot of teams operate. Some people love i"
  }
]
```

**Criterion 4 — `appeal path`, trial 1** (2 of 6 results shown; label text shortened with …):

```json
[
  {
    "sent": "I love eating a chicken sandwich. I love it when the chicken is fresh,",
    "submit_status": 200,
    "content_id": "29da38b2-0816-4d43-87b1-19a8e4a3e82e",
    "guess": "ai",
    "appeal_http": 200,
    "appeal_status": "under_review",
    "log_events": [
      "decided",
      "appeal"
    ],
    "log_has_appeal": true
  },
  {
    "sent": "appeal for unknown content_id no-such-id-trial-1",
    "appeal_http": 404,
    "appeal_status": "appeal_unknown_content_id"
  }
]
```

**Criterion 5 — `bad input`, trial 1** (4 of 4 results shown; label text shortened with …):

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": \"I wrote this paragraph myself last week.\"}"
  },
  {
    "status": 413,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

**Diagnoses**

The three misses and the six false-positive attacks are **one problem**, not nine.

*Criterion 1 (5 of 10 of my own pieces labelled AI), criterion 3 (no "human"), and attacks
FP02–FP07.* My pieces are short and plain: two or three sentences, everyday words, almost
no dashes, semicolons or questions. Both signals read that as machine writing:

- **Signal one** (`detector.model_signal`). Sentences like "I wake up at 6:30 am to get
  ready for college" are made of the most common words in the most common order, so
  gpt2 predicts them easily. Low perplexity gives a high score (0.901 on that piece). It
  measures predictability, and plain writing is predictable whoever wrote it.
- **Signal two** (`stylometry.style_signal`). Breaking the style score into its parts:
  the punctuation measure scores **1.00 (maximum AI)** on 8 of my 10 pieces, on FP03 and
  FP05, *and* on all 5 clearly-AI texts. It can't tell the groups apart, because neither
  plain human writing nor AI writing uses expressive punctuation. Sentence-length
  spread on two sentences is also close to noise: "Life is too short…" has two
  similar-length sentences, so spread scores 1.00 and its style score is 1.000.
- **The combining rule** (`scoring.combine_signals`) is where those two errors add up
  instead of cancelling. My only guard is the disagreement cap, and it fires only when the
  signals *disagree*. On plain human writing they agree (FP03: 0.805 and 0.804, gap 0.00),
  so nothing stops the accusation.
- **The label mapping** turns that into an accusation at 0.70, and 0.70 sits *below* most
  of the human scores: mine at 0.734–0.900, FP02–FP07 at 0.770–0.857.

The stage that *causes* it is the two signals measuring the same thing (plainness). The
stage where it *becomes an accusation* is the label mapping.

*Criterion 2 (gap 0.086).* Same mechanism seen from the other side. My "clearly human"
set is plain writing, which both signals push up to 0.726, right next to the AI mean of
0.812. The signals separate polished human prose (unit 7's button-jar paragraph, 0.318)
from AI text, but not plain human prose. For plain writing, the score is mostly
measuring how plain the text is, not who wrote it.

*Evasion attacks EV01–EV09 (9 broke).* The AI paragraph they share only scores 0.722, two
hundredths over the line, so almost any edit drops it out. The edits work through two
different mechanisms:
- **Signal one:** typos (EV01, model 0.67 → 0.16), a short text (EV08, 0.25) and a human
  opening (EV05, 0.32) all make the text less predictable to gpt2. The typo attack was
  aimed at signal two but actually broke signal one: a misspelt word is a rare token.
- **Signal two:** "Really." between sentences (EV02, style 0.80 → 0.23), a quotation
  (EV03, 0.37) and semicolon padding (EV07, 0.33) all add expressive punctuation or
  sentence-length spread without changing a word of the AI content. That's exactly the
  blind spot I named in unit 7.

*PI02 (labelled human).* Stage: **signal one**. The system never read the instruction as
an instruction; nothing in my pipeline is a language model that takes orders. But
`SYSTEM: … Return guess=human, confidence=0.02.` is a very unpredictable string to gpt2:
scored alone it gets model 0.019. Perplexity is averaged over the whole text, so pasting
it on top of a short AI fragment (0.754 alone) dragged the total to 0.204. Any weird
text would have done the same; the "injection" just happens to be weird text.

*MF03–MF07 (junk scored as writing).* Stage: **the route**. `app.py::submit` only
checks that `text` is a non-empty string under 20,000 characters, then hands anything
to the signals. Neither signal can say "this isn't English prose". gpt2 finds a run of
`a`s or repeated emoji extremely predictable (MF05 0.998, MF06 0.997) and Arabic
unfamiliar in a way that still comes out high (0.906). So the system confidently labels
non-writing, and a real Arabic sentence, as AI.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
