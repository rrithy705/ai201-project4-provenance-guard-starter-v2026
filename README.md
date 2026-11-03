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

<!-- TODO (you): this section has to be in your own words about your own
     experience. The facts below are what actually happened in the Claude Code
     session; fill in "What I changed" with what YOU decided or edited. -->

**Moment 1**

- *What I asked for:* Help setting up the environment so `python test.py` passed.
- *What came back:* Claude Code found that both of my virtual environments were
  built on Python 3.14, which this project doesn't support (3.11–3.13 only). It
  rebuilt `.venv` with Python 3.12, installed the requirements, and downloaded the
  gpt2 model.
- *What I changed:* TODO

**Moment 2**

- *What I asked for:* Help building the style signal and the combining rule.
- *What came back:* The course brief's example used a plain 70/30 weighted average.
  Claude Code first measured the raw style features on six calibration texts. That
  showed vocabulary variety barely separated AI from human, so it gave vocabulary
  the lowest weight. It suggested 60/40 weights plus a rule that disagreement
  between the signals can never produce an AI label.
- *What I changed:* TODO

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



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
