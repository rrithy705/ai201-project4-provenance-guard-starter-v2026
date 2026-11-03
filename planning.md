# Planning — Provenance Guard

## Part A — The path a submission takes

1. A writer sends a piece of text and their `creator_id` to `POST /submit` as JSON.
2. The route in `app.py` checks the request. If `text` or `creator_id` is missing,
   empty, or not a string, it answers `400` and logs the rejection instead of crashing.
3. **Signal one** — `detector.model_signal(text)` runs gpt2 locally and measures how
   *predictable* the text is (perplexity), squashed onto 0–1 where higher = more AI-like.
4. **Signal two** — `stylometry.style_signal(text)` measures the *shape* of the text
   (sentence-length spread, vocabulary variety, punctuation variety) and turns it into
   a 0–1 score pointing the same way.
5. `scoring.combine_signals(model, style)` merges the two into one combined score.
6. `scoring.score_to_label(score)` maps the combined score to one of three labels:
   high-confidence human, unsure, or high-confidence AI — written in plain words.
7. `audit.log_decision(...)` appends the decision (timestamp, content_id, creator_id,
   guess, both signal scores, combined score, label, status=`decided`) to
   `logs/audit.jsonl`, and the route returns the result to the writer.
8. If the writer disagrees, they send the `content_id` and their reasoning to
   `POST /appeal`. The appeal is appended to the same log and the item's status
   becomes `under_review`. Nothing is overwritten.

## Part B — The two signals

| Signal | What it measures | Limitation (blind spot) |
|---|---|---|
| Model signal (`detector.py`) | How predictable the text is to gpt2 (perplexity) | Predictability is not authorship. Plain writing — second-language writers, younger writers, anyone writing simply on purpose — looks as predictable as machine text, so it gets falsely flagged. Ornate prose with rare words can hide AI text. |
| Style signal (`stylometry.py`) | Sentence-length variation, word variety, punctuation variety | It cannot read. Style doesn't prove authorship, and anything that changes the shape without changing the content (typos, chopped-up sentences, a pasted quote) moves it cheaply. |

**Who I'm most worried about:** a person writing plainly in a second language. Signal
one is structurally likely to accuse them, and they have the least room to argue back.
That means the system should lean toward "unsure" rather than "AI" when evidence is weak,
and the appeal path must always work.

## Part C — Endpoints

### `POST /submit`

Request:

```json
{"text": "This is my original writing.", "creator_id": "user123"}
```

Response (example shape, not a real result):

```json
{
  "content_id": "abc123",
  "guess": "human",
  "confidence": 0.85,
  "label": "We think this was probably written by a person.",
  "model_score": 0.12,
  "style_score": 0.30,
  "combined_score": 0.18
}
```

- `400` if `text` or `creator_id` is missing/empty/not a string; `400` if the text is
  too short for the model to score.
- `413` if the text is enormous (over 20,000 characters).

### `POST /appeal`

Request:

```json
{"content_id": "abc123", "reasoning": "I wrote this myself."}
```

- `404` if the `content_id` doesn't exist in the log.
- `400` if `reasoning` is missing.
- Otherwise logs the appeal with `audit.log_appeal(...)`, sets status to
  `under_review`, and returns a confirmation.
