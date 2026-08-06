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
    TernaryALU,
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


# ==========================================
# New Ternary ALU & Instruction Tests
# ==========================================

def test_ternary_alu_load_validation():
    alu = TernaryALU()
    # Valid LOADs
    alu.execute("LOAD R0, 1T0")
    assert alu.registers["R0"] == "1T0"

    alu.execute("LOAD R1, T11")
    assert alu.registers["R1"] == "T11"

    # Invalid Register
    with pytest.raises(ValueError):
        alu.execute("LOAD R5, 1T0")

    # Invalid Trit values
    with pytest.raises(ValueError):
        alu.execute("LOAD R0, 120T")


def test_ternary_alu_arithmetic():
    alu = TernaryALU()
    # 4 (11) and 2 (1T)
    alu.execute("LOAD R0, 11")
    alu.execute("LOAD R1, 1T")

    # ADD R2, R0, R1 -> 4 + 2 = 6 (1T0)
    alu.execute("ADD R2, R0, R1")
    assert alu.registers["R2"] == "1T0"
    assert ternary_to_decimal(alu.registers["R2"]) == 6

    # SUB R2, R0, R1 -> 4 - 2 = 2 (1T)
    alu.execute("SUB R2, R0, R1")
    assert alu.registers["R2"] == "1T"
    assert ternary_to_decimal(alu.registers["R2"]) == 2

    # MUL R2, R0, R1 -> 4 * 2 = 8 (10T)
    alu.execute("MUL R2, R0, R1")
    assert alu.registers["R2"] == "10T"
    assert ternary_to_decimal(alu.registers["R2"]) == 8


def test_ternary_alu_bitwise_logic():
    alu = TernaryALU()
    # R0 = 1T0 (6), R1 = 11 (4)
    alu.execute("LOAD R0, 1T0")
    alu.execute("LOAD R1, 11")

    # NEG R2, R0 -> -6 (T10)
    alu.execute("NEG R2, R0")
    assert alu.registers["R2"] == "T10"
    assert ternary_to_decimal(alu.registers["R2"]) == -6

    # NOT R2, R0 -> -6 (T10) [bitwise NOT is identical to negation in balanced ternary!]
    alu.execute("NOT R2, R0")
    assert alu.registers["R2"] == "T10"

    # AND R2, R0, R1 -> bitwise AND of 1T0 and 011 -> 0T0 -> T0 (-3)
    # 1T0 and 011:
    # 1 AND 0 -> 0
    # T AND 1 -> T
    # 0 AND 1 -> 0
    # Result: 0T0 -> T0
    alu.execute("AND R2, R0, R1")
    assert alu.registers["R2"] == "T0"
    assert ternary_to_decimal(alu.registers["R2"]) == -3

    # OR R2, R0, R1 -> bitwise OR of 1T0 and 011 -> 111 (13)
    # 1 OR 0 -> 1
    # T OR 1 -> 1
    # 0 OR 1 -> 1
    # Result: 111
    alu.execute("OR R2, R0, R1")
    assert alu.registers["R2"] == "111"
    assert ternary_to_decimal(alu.registers["R2"]) == 13


def test_ternary_alu_shift_operations():
    alu = TernaryALU()
    # R0 = 11 (4)
    alu.execute("LOAD R0, 11")

    # SHL R1, R0 -> 4 * 3 = 12 (110)
    alu.execute("SHL R1, R0")
    assert alu.registers["R1"] == "110"
    assert ternary_to_decimal(alu.registers["R1"]) == 12

    # SHR R2, R1 -> 12 // 3 = 4 (11)
    alu.execute("SHR R2, R1")
    assert alu.registers["R2"] == "11"
    assert ternary_to_decimal(alu.registers["R2"]) == 4

    # SHR on a single trit -> should reduce to 0
    alu.execute("LOAD R0, T")
    alu.execute("SHR R1, R0")
    assert alu.registers["R1"] == "0"
