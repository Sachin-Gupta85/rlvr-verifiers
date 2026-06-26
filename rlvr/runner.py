"""Batch-grade a dataset and report pass rate + mean reward."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .reward import Reward, combined_reward


class Verifier(Protocol):
    def verify(self, response: str, gold: str):
        ...


@dataclass
class Sample:
    response: str
    gold: str


@dataclass
class RunReport:
    n: int
    pass_rate: float
    mean_reward: float
    rows: list[dict] = field(default_factory=list)


def grade(samples: list[Sample], verifier: Verifier, *,
          shaped: bool = True, format_weight: float = 0.1) -> RunReport:
    rows: list[dict] = []
    for s in samples:
        res = verifier.verify(s.response, s.gold)
        if shaped:
            r: Reward = combined_reward(s.response, res, format_weight=format_weight)
            reward = r.total
        else:
            reward = res.reward
        rows.append({"correct": res.correct, "reward": reward,
                     "extracted": res.extracted, "reason": res.reason})
    n = len(samples)
    passed = sum(1 for row in rows if row["correct"])
    return RunReport(
        n=n,
        pass_rate=passed / n if n else 0.0,
        mean_reward=sum(row["reward"] for row in rows) / n if n else 0.0,
        rows=rows,
    )
