"""Offline demo — grade a batch of model answers with verifiable rewards.

    python -m rlvr
"""
from __future__ import annotations

from .runner import Sample, grade
from .verifiers import MathVerifier


def main() -> None:
    samples = [
        Sample("We add the fractions: 1/2 + 1/3 = \\boxed{5/6}.", "5/6"),
        Sample("Total cost is \\boxed{1,000} dollars.", "1000"),
        Sample("Reasoning...\n#### 18", "18"),
        Sample("I think it's about \\boxed{41}.", "42"),        # wrong but formatted
        Sample("The answer is 7", "7"),                          # correct, no box
    ]
    report = grade(samples, MathVerifier(), format_weight=0.1)

    print(f"pass rate : {report.pass_rate:.0%}   mean reward : {report.mean_reward:.3f}\n")
    for s, row in zip(samples, report.rows):
        mark = "✅" if row["correct"] else "❌"
        print(f"  {mark} reward={row['reward']:.2f}  extracted={row['extracted']!r:>8}  "
              f"gold={s.gold!r}  ({row['reason']})")


if __name__ == "__main__":
    main()
