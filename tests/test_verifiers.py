from rlvr.verifiers import (
    ExactMatchVerifier,
    MathVerifier,
    MultipleChoiceVerifier,
    RegexVerifier,
)


def test_math_matches_fraction_and_decimal_forms():
    v = MathVerifier()
    assert v.verify("The answer is \\boxed{0.5}", "1/2").correct
    assert v.verify("so we get \\boxed{1,000} dollars", "1000").correct


def test_math_rejects_wrong_value():
    v = MathVerifier()
    r = v.verify("\\boxed{3}", "4")
    assert not r.correct and r.reward == 0.0


def test_math_reports_no_answer():
    r = MathVerifier().verify("I am not sure.", "5")
    assert r.extracted is None and not r.correct


def test_math_string_fallback_for_nonnumeric():
    assert MathVerifier().verify("The answer is Paris.", "paris").correct


def test_exact_match_case_insensitive_by_default():
    assert ExactMatchVerifier().verify("Hello", "hello").correct
    assert not ExactMatchVerifier(case_sensitive=True).verify("Hello", "hello").correct


def test_multiple_choice_tolerates_formatting():
    v = MultipleChoiceVerifier()
    assert v.verify("The answer is (B).", "B").correct
    assert v.verify("B", "B").correct
    assert not v.verify("I pick C", "B").correct


def test_regex_format_verifier():
    v = RegexVerifier(r"\\boxed\{[^{}]*\}")
    assert v.verify("final \\boxed{7}").correct
    assert not v.verify("the answer is 7").correct
