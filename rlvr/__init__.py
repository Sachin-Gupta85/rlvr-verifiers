"""rlvr-verifiers — deterministic, verifiable reward functions for RLVR.

Pull the answer out of free-form model output and grade it with a pure,
reproducible verifier (math / exact-match / multiple-choice / regex), then shape
it into the reward signal an RL loop consumes. No model-in-the-loop, no SymPy —
exact arithmetic via a safe AST evaluator.
"""
from .answer import extract_answer, normalise, to_number
from .expr import ExprError, safe_eval
from .reward import Reward, combined_reward
from .runner import RunReport, Sample, grade
from .verifiers import (
    ExactMatchVerifier,
    MathVerifier,
    MultipleChoiceVerifier,
    RegexVerifier,
    VerificationResult,
)

__all__ = [
    "extract_answer", "normalise", "to_number",
    "ExprError", "safe_eval",
    "Reward", "combined_reward",
    "RunReport", "Sample", "grade",
    "ExactMatchVerifier", "MathVerifier", "MultipleChoiceVerifier",
    "RegexVerifier", "VerificationResult",
]
