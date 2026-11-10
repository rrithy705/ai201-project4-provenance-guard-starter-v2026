# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 02:23
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `8c9cd941-e14a-4fb3-bca5-6ffe95b82099` | unsure | 0.582 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `9bc328ec-66d3-4ad3-962b-bce7d606e417` | unsure | 0.551 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `fd8a2e0c-b64e-4e71-9e0a-7efa09041215` | unsure | 0.548 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `401b50df-84a7-43a1-b4a1-114364a36e43` | unsure | 0.687 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `bedb0a44-241f-4c28-b9ad-4ff006942b79` | unsure | 0.627 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `7444c1f3-9f22-4331-83e3-474f97b245fc` | unsure | 0.512 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `f2662b74-ffce-47d0-a03f-8f159ed2c19e` | unsure | 0.515 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `d1a1bbc8-3b23-47d9-9abc-1a967decb7c6` | unsure | 0.558 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `2a505c65-982e-4b69-bb42-06653248f933` | unsure | 0.599 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `a42fd4c7-42e9-4a92-9925-62544334b5ea` | ai | 0.929 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `3b88aab5-9863-4c19-9a24-c35394f4a547` | unsure | 0.659 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `a38c43a5-4ded-4e32-ac4d-5351be7919b1` | unsure | 0.811 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `99234b86-7742-45be-b2b4-367990280c33` | unsure | 0.805 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `4628f7c4-30ae-426f-acf3-6ef59dcfcc29` | unsure | 0.809 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `532b74da-be5a-428e-9555-5659fecf2968` | unsure | 0.857 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c77f98e2-28fe-4f5b-b850-ef794d92a2c8` | unsure | 0.819 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `737b5e41-fe83-4df2-9a0b-37246ceeb315` | unsure | 0.770 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `dde33754-8a16-47c9-b1d9-5b552ac918de` | unsure | 0.556 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `7ccb26d9-99d1-4755-9037-c2b8b81321e0` | unsure | 0.541 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f7488544-e7bd-4cab-9015-118a37164d2c` | human | 0.732 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `d89ef42e-f5b1-4c7a-b7ef-40d87250ab11` | unsure | 0.538 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `4fef23b3-082e-4ae8-8647-398c51d4aa66` | unsure | 0.552 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `46226d41-f4e5-491e-9615-1160ab5b5aa4` | unsure | 0.517 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `39629aaf-c648-4010-b6c5-8d189aa716be` | unsure | 0.624 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `a6cf8d43-9f57-43cd-b916-d059873ef1d4` | human | 0.770 |  |
| MF04 | malformed | text is only punctuation | 200 | `59a8bd79-c071-4f3d-ae1a-94dd8fbb55b9` | unsure | 0.593 |  |
| MF05 | malformed | text is a very long single word | 200 | `8a33daa8-2262-4891-a91f-f2c7eeae726b` | unsure | 0.829 |  |
| MF06 | malformed | text is emoji only | 200 | `75393758-b248-4f1b-8f5b-5339f4bad1e9` | ai | 0.908 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c036eca0-c7b1-451d-a8a8-de598a37800c` | unsure | 0.854 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c55ffa45-54fa-449f-9ba1-73f288047baa` | human | 0.753 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `53373266-bff4-4bb4-b353-a83401b10856` | human | 0.753 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fb7401e4-0593-4404-972a-104eb5573f20` | human | 0.753 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5858f4fc-87d0-468b-9626-ed964f9e7060` | human | 0.753 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1e1ff496-36b7-4445-af6a-fb14c978dcae` | human | 0.753 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "8c9cd941-e14a-4fb3-bca5-6ffe95b82099",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5819,
  "model_score": 0.1635,
  "style_score": 0.8,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "9bc328ec-66d3-4ad3-962b-bce7d606e417",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5508,
  "model_score": 0.5943,
  "style_score": 0.2315,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "fd8a2e0c-b64e-4e71-9e0a-7efa09041215",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5476,
  "model_score": 0.6662,
  "style_score": 0.3698,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "401b50df-84a7-43a1-b4a1-114364a36e43",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6868,
  "model_score": 0.6114,
  "style_score": 0.8,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "bedb0a44-241f-4c28-b9ad-4ff006942b79",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.627,
  "model_score": 0.3212,
  "style_score": 0.4508,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "7444c1f3-9f22-4331-83e3-474f97b245fc",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5121,
  "model_score": 0.5727,
  "style_score": 0.4212,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "f2662b74-ffce-47d0-a03f-8f159ed2c19e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5147,
  "model_score": 0.5862,
  "style_score": 0.3339,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "d1a1bbc8-3b23-47d9-9abc-1a967decb7c6",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5577,
  "model_score": 0.2452,
  "style_score": 0.7379,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "2a505c65-982e-4b69-bb42-06653248f933",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5992,
  "model_score": 0.7042,
  "style_score": 0.4417,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "a42fd4c7-42e9-4a92-9925-62544334b5ea",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9294,
  "model_score": 0.9792,
  "style_score": 0.8546,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "3b88aab5-9863-4c19-9a24-c35394f4a547",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6587,
  "model_score": 0.6175,
  "style_score": 0.7206,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "a38c43a5-4ded-4e32-ac4d-5351be7919b1",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.8113,
  "model_score": 0.7387,
  "style_score": 0.9201,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "99234b86-7742-45be-b2b4-367990280c33",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.8048,
  "model_score": 0.8051,
  "style_score": 0.8044,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "4628f7c4-30ae-426f-acf3-6ef59dcfcc29",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.8093,
  "model_score": 0.8329,
  "style_score": 0.7739,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "532b74da-be5a-428e-9555-5659fecf2968",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.8572,
  "model_score": 0.8005,
  "style_score": 0.9423,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c77f98e2-28fe-4f5b-b850-ef794d92a2c8",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.8187,
  "model_score": 0.8814,
  "style_score": 0.7246,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "737b5e41-fe83-4df2-9a0b-37246ceeb315",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7697,
  "model_score": 0.8816,
  "style_score": 0.6018,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "dde33754-8a16-47c9-b1d9-5b552ac918de",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.5565,
  "model_score": 0.3223,
  "style_score": 0.6252,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "7ccb26d9-99d1-4755-9037-c2b8b81321e0",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5413,
  "model_score": 0.4625,
  "style_score": 0.453,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "f7488544-e7bd-4cab-9015-118a37164d2c",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.7318,
  "model_score": 0.2044,
  "style_score": 0.3639,
  "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "d89ef42e-f5b1-4c7a-b7ef-40d87250ab11",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5382,
  "model_score": 0.5943,
  "style_score": 0.4541,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "4fef23b3-082e-4ae8-8647-398c51d4aa66",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5524,
  "model_score": 0.4998,
  "style_score": 0.3693,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "46226d41-f4e5-491e-9615-1160ab5b5aa4",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5174,
  "model_score": 0.6401,
  "style_score": 0.2464,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "39629aaf-c648-4010-b6c5-8d189aa716be",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.6243,
  "model_score": 0.5583,
  "style_score": 0.7234,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "a6cf8d43-9f57-43cd-b916-d059873ef1d4",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.77,
  "model_score": 0.0,
  "style_score": 0.575,
  "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "59a8bd79-c071-4f3d-ae1a-94dd8fbb55b9",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5933,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "8a33daa8-2262-4891-a91f-f2c7eeae726b",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.8286,
  "model_score": 0.9976,
  "style_score": 0.575,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "75393758-b248-4f1b-8f5b-5339f4bad1e9",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9081,
  "model_score": 0.9969,
  "style_score": 0.775,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c036eca0-c7b1-451d-a8a8-de598a37800c",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.8538,
  "model_score": 0.9064,
  "style_score": 0.775,
  "label": "We couldn't tell either way. Plenty of people write in a style our checks find hard to read, so this is not a judgement about you or your work. If you wrote it, you don't need to do anything \u2014 and you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c55ffa45-54fa-449f-9ba1-73f288047baa",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7528,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "53373266-bff4-4bb4-b353-a83401b10856",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7528,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "fb7401e4-0593-4404-972a-104eb5573f20",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7528,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "5858f4fc-87d0-468b-9626-ed964f9e7060",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7528,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "1e1ff496-36b7-4445-af6a-fb14c978dcae",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7528,
  "model_score": 0.0287,
  "style_score": 0.575,
  "label": "This reads like writing by a person. Our checks found nothing that suggests it was generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
