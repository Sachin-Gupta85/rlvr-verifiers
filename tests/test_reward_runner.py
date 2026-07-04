import pytest

from rlvr.reward import combined_reward
from rlvr.runner import Sample, grade
from rlvr.verifiers import MathVerifier


def test_combined_reward_rewards_format():
    v = MathVerifier()
    correct_boxed = combined_reward("\\boxed{42}", v.verify("\\boxed{42}", "42"))
    correct_plain = combined_reward("the answer is 42", v.verify("the answer is 42", "42"))
    wrong_boxed = combined_reward("\\boxed{41}", v.verify("\\boxed{41}", "42"))

    assert correct_boxed.total == pytest.approx(1.0)
    assert correct_plain.total == pytest.approx(0.9)      # correct, no box -> format bonus lost
    assert wrong_boxed.total == pytest.approx(0.1)        # wrong, but formatted
    assert correct_boxed.total > correct_plain.total > wrong_boxed.total


def test_grade_reports_pass_rate_and_mean_reward():
    samples = [
        Sample("\\boxed{2}", "2"),       # correct + formatted -> 1.0
        Sample("\\boxed{3}", "5"),       # wrong + formatted  -> 0.1
        Sample("answer is 4", "4"),      # correct, no box    -> 0.9
    ]
    report = grade(samples, MathVerifier())
    assert report.n == 3
    assert report.pass_rate == pytest.approx(2 / 3)
    assert report.mean_reward == pytest.approx((1.0 + 0.1 + 0.9) / 3)


def test_grade_unshaped_uses_raw_reward():
    samples = [Sample("answer is 4", "4")]
    report = grade(samples, MathVerifier(), shaped=False)
    assert report.mean_reward == 1.0                      # raw correctness, no format weighting
