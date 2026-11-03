"""Pure, dependency-free core logic.

The deterministic heart of the assistant: the compound-interest maths
and the checks used by the evaluation. Imports nothing heavy, so it can
be unit-tested quickly and for free, without loading the ML model or
calling any API.
"""
import math
import re


def compute_compound_interest(principal: float, annual_rate: float, years: float):
    """Return (final_amount, gain). annual_rate is a percentage, e.g. 7 = 7%."""
    rate = annual_rate / 100
    final_amount = principal * (1 + rate) ** years
    gain = final_amount - principal
    return final_amount, gain


def is_abstention(answer: str) -> bool:
    """True if the answer is an explicit out-of-scope abstention."""
    return answer.strip().lower().startswith("abstain:")


def extract_numbers(text: str):
    """Extract all numbers from text (handles thousands separators)."""
    matches = re.findall(r"[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?", text)
    return [float(m.replace(",", "")) for m in matches]


def value_in_answer(answer: str, expected_value: float, tolerance: float = 1.0) -> bool:
    """True if expected_value appears in the answer within tolerance."""
    return any(
        math.isclose(v, expected_value, rel_tol=0, abs_tol=tolerance)
        for v in extract_numbers(answer)
    )
