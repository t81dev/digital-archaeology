import pytest
from ternary_sim import (
    decimal_to_ternary,
    ternary_to_decimal,
    ternary_not,
    ternary_and,
    ternary_or,
    trit_full_adder,
    ternary_add,
    ternary_negate,
    ternary_subtract,
    ternary_multiply,
)

def test_decimal_to_ternary():
    assert decimal_to_ternary(0) == "0"
    assert decimal_to_ternary(1) == "1"
    assert decimal_to_ternary(-1) == "T"
    assert decimal_to_ternary(2) == "1T"
    assert decimal_to_ternary(-2) == "T1"
    assert decimal_to_ternary(3) == "10"
    assert decimal_to_ternary(-3) == "T0"
    assert decimal_to_ternary(4) == "11"
    assert decimal_to_ternary(-4) == "TT"

def test_conversions_roundtrip():
    test_cases = [0, 1, -1, 2, -2, 4, -4, 5, -5, 13, -13, 121, -121, 2026, -2026]
    for n in test_cases:
        tern = decimal_to_ternary(n)
        assert ternary_to_decimal(tern) == n

def test_invalid_ternary_string():
    with pytest.raises(ValueError):
        ternary_to_decimal("102T")
    with pytest.raises(ValueError):
        ternary_to_decimal("ABC")

def test_ternary_logic_gates():
    assert ternary_not(1) == -1
    assert ternary_not(0) == 0
    assert ternary_not(-1) == 1

    assert ternary_and(1, 0) == 0
    assert ternary_and(-1, 1) == -1
    assert ternary_and(1, 1) == 1
    assert ternary_and(0, 0) == 0

    assert ternary_or(1, 0) == 1
    assert ternary_or(-1, -1) == -1
    assert ternary_or(0, -1) == 0
    assert ternary_or(1, 1) == 1

def test_trit_full_adder():
    # Sum/carry for a + b + c_in
    assert trit_full_adder(0, 0, 0) == (0, 0)
    assert trit_full_adder(1, 1, 1) == (0, 1)
    assert trit_full_adder(-1, -1, -1) == (0, -1)
    assert trit_full_adder(1, -1, 0) == (0, 0)
    assert trit_full_adder(1, 1, 0) == (-1, 1)
    assert trit_full_adder(-1, -1, 0) == (1, -1)

def test_ternary_arithmetic():
    # Addition
    assert ternary_to_decimal(ternary_add("1", "1")) == 2
    assert ternary_to_decimal(ternary_add("1", "T")) == 0
    assert ternary_to_decimal(ternary_add("10", "1")) == 4
    assert ternary_to_decimal(ternary_add("T0", "T")) == -4

    # Negation
    assert ternary_negate("10T") == "T01"
    assert ternary_negate("0") == "0"

    # Subtraction
    assert ternary_to_decimal(ternary_subtract("1", "1")) == 0
    assert ternary_to_decimal(ternary_subtract("1", "T")) == 2
    assert ternary_to_decimal(ternary_subtract("10", "1")) == 2  # 3 - 1 = 2

    # Multiplication
    assert ternary_to_decimal(ternary_multiply("1", "1")) == 1
    assert ternary_to_decimal(ternary_multiply("10", "10")) == 9
    assert ternary_to_decimal(ternary_multiply("1T", "1T")) == 4 # 2 * 2 = 4
    assert ternary_to_decimal(ternary_multiply("1T", "T1")) == -4 # 2 * -2 = -4
    assert ternary_to_decimal(ternary_multiply("0", "11")) == 0
    assert ternary_to_decimal(ternary_multiply("11", "0")) == 0
