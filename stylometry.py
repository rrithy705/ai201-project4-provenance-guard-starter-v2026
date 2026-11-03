"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────

# Punctuation that varies a lot between writers. Full stops and commas are left
# out on purpose: everyone uses them, so they say little about who wrote it.
EXPRESSIVE_PUNCTUATION = set(";:—–()?!\"'")

# Window for the moving type-token ratio. Plain TTR falls as text gets longer;
# averaging over fixed 50-word windows keeps short and long texts comparable.
TTR_WINDOW = 50


def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation of sentence length (stdev / mean, in words).

    Returns:
        0.0 and up. Typically 0.2–0.9. **Higher means more human** — human
        writing mixes three-word sentences with forty-word ones.

        Fewer than two sentences has no spread to measure and returns 0.0;
        `style_signal` treats that case as neutral rather than as evidence.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Moving-average type-token ratio over 50-word windows.

    Returns:
        A float between 0 and 1. **Higher means more varied vocabulary**, which
        leans human. Texts under 50 words fall back to plain TTR.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if len(tokens) < TTR_WINDOW:
        return len(set(tokens)) / len(tokens)
    windows = [
        len(set(tokens[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(tokens) - TTR_WINDOW + 1)
    ]
    return statistics.mean(windows)


def punctuation_density(text: str) -> float:
    """
    Expressive punctuation marks (; : — – ( ) ? ! quotes) per word.

    Returns:
        0.0 and up. Typically 0.0–0.12. **Higher means more human** — generated
        prose leans on full stops and commas and rarely uses dashes, semicolons
        or questions.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    marks = sum(1 for ch in text if ch in EXPRESSIVE_PUNCTUATION)
    return marks / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

def _scale(value: float, ai_end: float, human_end: float) -> float:
    """Map a raw measure onto 0–1 AI-likeness: ai_end -> 1.0, human_end -> 0.0."""
    score = (value - human_end) / (ai_end - human_end)
    return min(max(score, 0.0), 1.0)


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    All three measures point the "more human" way when raw, so each is flipped
    by `_scale`, which maps it to 0–1 AI-likeness between two anchor points
    chosen from the Milestone 4 calibration texts:

        spread       0.20 -> 1.0 (AI)     0.80 -> 0.0 (human)
        vocabulary   0.72 -> 1.0          0.92 -> 0.0
        punctuation  0.00 -> 1.0          0.08 -> 0.0

    Weights: spread 0.45, punctuation 0.35, vocabulary 0.20. Vocabulary gets the
    least because on the calibration set it barely separated AI from human.
    """
    if len(sentences(text)) < 2:
        spread_ai = 0.5  # one sentence: no evidence either way
    else:
        spread_ai = _scale(sentence_length_spread(text), ai_end=0.20, human_end=0.80)
    vocab_ai = _scale(type_token_ratio(text), ai_end=0.72, human_end=0.92)
    punct_ai = _scale(punctuation_density(text), ai_end=0.0, human_end=0.08)

    score = 0.45 * spread_ai + 0.35 * punct_ai + 0.20 * vocab_ai
    return round(score, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
