import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from logic import (
    compute_compound_interest,
    extract_numbers,
    is_abstention,
    value_in_answer,
)


def test_compound_interest_basic():
    final, gain = compute_compound_interest(1000, 7, 10)
    assert round(final, 2) == 1967.15
    assert round(gain, 2) == 967.15


def test_compound_interest_zero_rate():
    final, gain = compute_compound_interest(500, 0, 5)
    assert final == 500
    assert gain == 0


def test_is_abstention_true():
    assert is_abstention("ABSTAIN: out of scope")
    assert is_abstention("  abstain: not covered  ")


def test_is_abstention_false():
    assert not is_abstention("Bonds are debt securities issued by companies.")
    assert not is_abstention("The final value is 1967.15.")


def test_extract_numbers_with_separators():
    assert extract_numbers("grows to 1,967.15 (gain 967.15)") == [1967.15, 967.15]


def test_value_in_answer_within_tolerance():
    answer = "the investment grows to 1967.15 (a gain of 967.15)."
    assert value_in_answer(answer, 1967.15, tolerance=1.0)
    assert not value_in_answer(answer, 2500.0, tolerance=1.0)
