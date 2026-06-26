"""Reward shaping for RLVR.

Policies are usually trained on more than raw correctness: a small **format**
reward teaches the model to put its answer where the grader can find it (e.g. in
``\\boxed{}``), and the correctness reward dominates. ``combined_reward`` mixes
the two with a tunable weight, which is exactly the signal an RL loop consumes.
"""
from __future__ import annotations

from dataclasses import dataclass

from .verifiers import RegexVerifier, VerificationResult

# A response is "well formatted" if it contains a boxed answer.
BOXED_FORMAT = RegexVerifier(r"\\boxed\{[^{}]*\}")


@dataclass(frozen=True)
class Reward:
    total: float
    correctness: float
    format: float


def combined_reward(response: str, result: VerificationResult, *,
                    format_weight: float = 0.1,
                    format_verifier: RegexVerifier = BOXED_FORMAT) -> Reward:
    """Correctness plus a bounded format bonus, total clamped to [0, 1]."""
    if not 0 <= format_weight < 1:
        raise ValueError("format_weight must be in [0, 1)")
    correctness = 1.0 if result.correct else 0.0
    fmt = format_verifier.verify(response).reward
    total = (1 - format_weight) * correctness + format_weight * fmt
    return Reward(total=round(total, 6), correctness=correctness, format=fmt)
