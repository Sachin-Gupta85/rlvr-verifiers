"""Extract and normalise the final answer from free-form model output.

RLVR rewards hinge on pulling *one* answer out of a chatty response and
comparing it fairly. These helpers mirror what GSM8K / MATH-style graders do:
honour ``\\boxed{...}`` and "the answer is ...", strip formatting noise
(commas, $, %, units), and parse to an exact number when possible.
"""
from __future__ import annotations

import re
from fractions import Fraction

from .expr import ExprError, safe_eval

_BOXED = re.compile(r"\\boxed\{([^{}]*)\}")
_ANSWER_IS = re.compile(r"(?:the\s+)?(?:final\s+)?answer\s*(?:is|:|=)\s*(.+?)(?:[.\n]|$)", re.I)
_HASH = re.compile(r"####\s*(.+?)(?:\n|$)")          # GSM8K gold format
_NUMBER = re.compile(r"-?\$?\d[\d,]*\.?\d*%?")


def extract_answer(text: str) -> str | None:
    """Return the best-guess answer span from ``text`` (not yet normalised)."""
    if not text:
        return None
    for pattern in (_BOXED, _HASH, _ANSWER_IS):
        m = pattern.search(text)
        if m:
            return m.group(1).strip()
    # fall back to the last number-looking token in the text
    numbers = _NUMBER.findall(text)
    return numbers[-1].strip() if numbers else None


def normalise(answer: str) -> str:
    """Canonicalise a textual answer: strip $,%, commas, units and whitespace."""
    s = answer.strip().strip(".").strip()
    s = s.replace(",", "").replace("$", "").replace("\\%", "").replace("%", "")
    s = re.sub(r"\b(dollars?|cents?|units?|years?|days?|hours?|km|cm|mm|kg|g)\b", "", s, flags=re.I)
    return s.strip().lower()


def to_number(answer: str) -> Fraction | None:
    """Parse a normalised answer to an exact Fraction, or None if non-numeric."""
    s = normalise(answer)
    if not s:
        return None
    try:
        return safe_eval(s)
    except ExprError:
        return None
