"""Verifiers — the deterministic graders that turn a response into a 0/1 reward.

Each verifier implements ``verify(response, gold) -> VerificationResult``. They
are pure and deterministic (the "verifiable" in RLVR): the same inputs always
yield the same reward, with no model-in-the-loop and no randomness.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .answer import extract_answer, normalise, to_number


@dataclass(frozen=True)
class VerificationResult:
    reward: float            # 1.0 correct, 0.0 incorrect
    correct: bool
    extracted: str | None
    reason: str


class MathVerifier:
    """Numeric/symbolic equality with an exact-fraction fast path.

    Handles ``\\boxed{}``, commas, units and expression golds ("1/2 + 1/3").
    Falls back to normalised string equality for non-numeric answers.
    """

    def __init__(self, tol: float = 1e-6) -> None:
        self.tol = tol

    def verify(self, response: str, gold: str) -> VerificationResult:
        pred_span = extract_answer(response)
        if pred_span is None:
            return VerificationResult(0.0, False, None, "no answer found in response")

        pg = to_number(pred_span)
        gg = to_number(gold)
        if pg is not None and gg is not None:
            if pg == gg or abs(float(pg) - float(gg)) <= self.tol:
                return VerificationResult(1.0, True, pred_span, "numeric match")
            return VerificationResult(0.0, False, pred_span, f"numeric mismatch {pg} != {gg}")

        if normalise(pred_span) == normalise(gold):
            return VerificationResult(1.0, True, pred_span, "string match")
        return VerificationResult(0.0, False, pred_span, "mismatch")


class ExactMatchVerifier:
    def __init__(self, case_sensitive: bool = False) -> None:
        self.case_sensitive = case_sensitive

    def verify(self, response: str, gold: str) -> VerificationResult:
        a, b = response.strip(), gold.strip()
        if not self.case_sensitive:
            a, b = a.lower(), b.lower()
        ok = a == b
        return VerificationResult(float(ok), ok, response.strip(),
                                  "exact match" if ok else "no exact match")


class MultipleChoiceVerifier:
    """Grade a single-letter choice (A/B/C/D), tolerant of '(B)', 'Answer: B'."""

    _LETTER = re.compile(r"\b([A-E])\b")

    def verify(self, response: str, gold: str) -> VerificationResult:
        span = extract_answer(response) or response
        m = self._LETTER.search(span.upper()) or self._LETTER.search(response.upper())
        pred = m.group(1) if m else None
        ok = pred is not None and pred == gold.strip().upper()
        return VerificationResult(float(ok), ok, pred, "choice match" if ok else "choice mismatch")


class RegexVerifier:
    """Reward 1.0 iff the response matches a required pattern (format reward)."""

    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern, re.S)

    def verify(self, response: str, gold: str = "") -> VerificationResult:
        ok = self.pattern.search(response) is not None
        return VerificationResult(float(ok), ok, None,
                                  "pattern matched" if ok else "pattern not matched")
