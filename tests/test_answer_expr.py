from fractions import Fraction

import pytest

from rlvr.answer import extract_answer, normalise, to_number
from rlvr.expr import ExprError, safe_eval


def test_safe_eval_is_exact():
    assert safe_eval("1/2 + 1/3") == Fraction(5, 6)
    assert safe_eval("2**10") == Fraction(1024)
    assert safe_eval("-(3 - 5)") == Fraction(2)


def test_safe_eval_rejects_code():
    for bad in ["__import__('os')", "len([1])", "x + 1", "1;2"]:
        with pytest.raises(ExprError):
            safe_eval(bad)


def test_extract_boxed_beats_trailing_numbers():
    assert extract_answer("We compute 3 then 5, so \\boxed{42} is final.") == "42"


def test_extract_gsm8k_hash_and_answer_is():
    assert extract_answer("... reasoning ...\n#### 18") == "18"
    assert extract_answer("The final answer is 7.") == "7"


def test_extract_falls_back_to_last_number():
    assert extract_answer("3 apples plus 5 oranges makes 8 fruit") == "8"
    assert extract_answer("no digits here") is None


def test_normalise_strips_formatting_and_units():
    assert normalise("$1,000") == "1000"
    assert normalise("50%") == "50"
    assert normalise("42 dollars") == "42"


def test_to_number_handles_expressions_and_nonnumeric():
    assert to_number("1/2 + 1/3") == Fraction(5, 6)
    assert to_number("cat") is None
