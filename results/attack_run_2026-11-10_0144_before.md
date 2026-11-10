# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 01:44
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `f21daea1-280f-4781-9861-fb0deae07df8` | unsure | 0.582 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c7a87d43-fd17-4e27-9560-2b3f17ab5f91` | unsure | 0.551 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d54ab105-340a-437b-8fe2-0e1b502a9b0b` | unsure | 0.548 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `4450c9f1-12db-4ea9-9f4d-191f1591b219` | unsure | 0.687 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `627fabef-87ec-44c1-a960-e0eda029be63` | unsure | 0.627 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `aa088004-30d5-4fce-9ae2-5c8f842915bb` | unsure | 0.512 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `94b1756d-2dfb-42eb-bd12-cf2c175faa48` | unsure | 0.515 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `0818d562-bc77-4fc1-b5e9-7ebdbda11618` | unsure | 0.558 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `743bcc08-919e-4234-aa70-b54342c0aaa3` | unsure | 0.599 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `3bee90b2-a353-4e06-bc3c-923680e692b8` | ai | 0.929 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f1f9e546-8fb9-453d-9512-582035ec8fc1` | unsure | 0.659 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `2e60bfdc-8345-455c-943a-5ae5b50810be` | ai | 0.811 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `1edbaa22-20ee-4e5e-829e-0f67c60beaac` | ai | 0.805 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `58c9f087-20de-43c1-a54d-39647722230c` | ai | 0.809 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `61e77c13-7798-4e24-af03-8daf78551a46` | ai | 0.857 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `1f75d2a7-0710-4abc-9e0b-3d8f151a065d` | ai | 0.819 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `a84f2fd8-b471-4677-bdbf-66f9d8d540be` | ai | 0.770 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `5da2a493-d1e4-495d-9e94-3bb31adae860` | unsure | 0.556 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `7e3ef4ad-5d57-49cd-a1b8-273f0447f923` | unsure | 0.541 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `2129a14a-556c-4ad8-9465-8ada43a0dd3a` | human | 0.732 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `b6c65a92-08e8-477c-a8e9-4a694c2e5f8e` | unsure | 0.538 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `697cb235-adc9-444d-be15-bbfb7f3678e6` | unsure | 0.552 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `6997b4db-7f85-416d-9f14-5a17302b4df6` | unsure | 0.517 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `2b454490-6a1a-4550-92ad-f89f9209a9a2` | unsure | 0.624 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `8fadec1f-de27-4797-a414-20d978c75913` | human | 0.770 |  |
| MF04 | malformed | text is only punctuation | 200 | `cbec0a49-f335-418b-8c2e-b1aa86b1ddf4` | unsure | 0.593 |  |
| MF05 | malformed | text is a very long single word | 200 | `ed66f01b-2a3a-4ab8-bed6-b7b35b095f06` | unsure | 0.690 |  |
| MF06 | malformed | text is emoji only | 200 | `4324bc8b-3f89-4e25-b995-d3c5668045cb` | ai | 0.908 |  |
| MF07 | malformed | text is right-to-left script | 200 | `ab163629-42ce-44f4-8087-11113497d28d` | ai | 0.854 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b4a275a4-bda7-489b-97bb-d1fc1ddcd7a9` | human | 0.753 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6223bf7b-e0da-4326-bd2a-ec79e6ed4aad` | human | 0.753 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `da5c2685-7720-4517-afb7-ba744bb4e776` | human | 0.753 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `47bf3699-df05-4b41-b6b6-dfa0cec99585` | human | 0.753 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `50106d47-a4ee-427e-8748-653ce6f1eb4b` | human | 0.753 |  |
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
  "content_id": "f21daea1-280f-4781-9861-fb0deae07df8",
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
  "content_id": "c7a87d43-fd17-4e27-9560-2b3f17ab5f91",
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
  "content_id": "d54ab105-340a-437b-8fe2-0e1b502a9b0b",
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
  "content_id": "4450c9f1-12db-4ea9-9f4d-191f1591b219",
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
  "content_id": "627fabef-87ec-44c1-a960-e0eda029be63",
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
  "content_id": "aa088004-30d5-4fce-9ae2-5c8f842915bb",
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
  "content_id": "94b1756d-2dfb-42eb-bd12-cf2c175faa48",
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
  "content_id": "0818d562-bc77-4fc1-b5e9-7ebdbda11618",
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
  "content_id": "743bcc08-919e-4234-aa70-b54342c0aaa3",
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
  "content_id": "3bee90b2-a353-4e06-bc3c-923680e692b8",
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
  "content_id": "f1f9e546-8fb9-453d-9512-582035ec8fc1",
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
  "content_id": "2e60bfdc-8345-455c-943a-5ae5b50810be",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8113,
  "model_score": 0.7387,
  "style_score": 0.9201,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
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
  "content_id": "1edbaa22-20ee-4e5e-829e-0f67c60beaac",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8048,
  "model_score": 0.8051,
  "style_score": 0.8044,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
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
  "content_id": "58c9f087-20de-43c1-a54d-39647722230c",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8093,
  "model_score": 0.8329,
  "style_score": 0.7739,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
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
  "content_id": "61e77c13-7798-4e24-af03-8daf78551a46",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8572,
  "model_score": 0.8005,
  "style_score": 0.9423,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
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
  "content_id": "1f75d2a7-0710-4abc-9e0b-3d8f151a065d",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.8187,
  "model_score": 0.8814,
  "style_score": 0.7246,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
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
  "content_id": "a84f2fd8-b471-4677-bdbf-66f9d8d540be",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7697,
  "model_score": 0.8816,
  "style_score": 0.6018,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
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
  "content_id": "5da2a493-d1e4-495d-9e94-3bb31adae860",
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
  "content_id": "7e3ef4ad-5d57-49cd-a1b8-273f0447f923",
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
  "content_id": "2129a14a-556c-4ad8-9465-8ada43a0dd3a",
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
  "content_id": "b6c65a92-08e8-477c-a8e9-4a694c2e5f8e",
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
  "content_id": "697cb235-adc9-444d-be15-bbfb7f3678e6",
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
  "content_id": "6997b4db-7f85-416d-9f14-5a17302b4df6",
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
  "content_id": "2b454490-6a1a-4550-92ad-f89f9209a9a2",
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
  "content_id": "8fadec1f-de27-4797-a414-20d978c75913",
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
  "content_id": "cbec0a49-f335-418b-8c2e-b1aa86b1ddf4",
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
  "content_id": "ed66f01b-2a3a-4ab8-bed6-b7b35b095f06",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.69,
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
  "content_id": "4324bc8b-3f89-4e25-b995-d3c5668045cb",
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
  "content_id": "ab163629-42ce-44f4-8087-11113497d28d",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8538,
  "model_score": 0.9064,
  "style_score": 0.775,
  "label": "Parts of this look a lot like AI-generated writing. This is an automated guess, not proof, and it can be wrong. If you wrote this yourself, please appeal and a person will review it.",
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
  "content_id": "b4a275a4-bda7-489b-97bb-d1fc1ddcd7a9",
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
  "content_id": "6223bf7b-e0da-4326-bd2a-ec79e6ed4aad",
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
  "content_id": "da5c2685-7720-4517-afb7-ba744bb4e776",
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
  "content_id": "47bf3699-df05-4b41-b6b6-dfa0cec99585",
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
  "content_id": "50106d47-a4ee-427e-8748-653ce6f1eb4b",
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
