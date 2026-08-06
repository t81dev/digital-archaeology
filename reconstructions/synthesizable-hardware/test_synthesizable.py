# test_synthesizable.py
# Python-based golden-model verification & RTL validation for Synthesizable Soft-Cores

import os
import pytest

# ==========================================
# 1. SystemVerilog RTL Code Validation
# ==========================================

def test_rtl_files_exist_and_are_valid():
    """Verify that SystemVerilog files are present and contain essential synthesizable RTL structures."""
    hardware_dir = os.path.dirname(__file__)
    alu_path = os.path.join(hardware_dir, "ternary_alu.sv")
    checker_path = os.path.join(hardware_dir, "capability_bounds_checker.sv")

    assert os.path.exists(alu_path), "ternary_alu.sv does not exist!"
    assert os.path.exists(checker_path), "capability_bounds_checker.sv does not exist!"

    # Verify Ternary ALU contains expected modules and synthesizable syntax
    with open(alu_path, 'r', encoding='utf-8') as f:
        alu_content = f.read()
        assert "module ternary_alu" in alu_content
        assert "always_comb" in alu_content
        assert "always_ff @(posedge clk or negedge rst_n)" in alu_content
        assert "function automatic" in alu_content
        assert "endmodule" in alu_content

    # Verify Capability Bounds Checker contains sequential blocks, active-low reset, and outputs
    with open(checker_path, 'r', encoding='utf-8') as f:
        checker_content = f.read()
        assert "module capability_bounds_checker" in checker_content
        assert "always_ff @(posedge clk or negedge rst_n)" in checker_content
        assert "resp_violation_flag" in checker_content
        assert "resp_violation_code" in checker_content
        assert "endmodule" in checker_content


# ==========================================
# 2. Golden-Model Verification: Ternary ALU
# ==========================================

def pn_to_int(trit_binary):
    """Mimics the pn_to_int SV function."""
    if trit_binary == 0b01:
        return 1
    elif trit_binary == 0b10:
        return -1
    else:
        return 0

def int_to_pn(val):
    """Mimics the int_to_pn SV function."""
    if val == 1:
        return 0b01
    elif val == -1:
        return 0b10
    else:
        return 0b00

def get_trits(value_6bit):
    """Splits a 6-bit input into 3 separate 2-bit PN trits (T0, T1, T2)."""
    t0 = value_6bit & 0b11
    t1 = (value_6bit >> 2) & 0b11
    t2 = (value_6bit >> 4) & 0b11
    return t0, t1, t2

def make_6bit(t0, t1, t2):
    """Assembles three 2-bit PN trits into a 6-bit value."""
    return t0 | (t1 << 2) | (t2 << 4)

def golden_ternary_full_adder(a, b, cin):
    val_a = pn_to_int(a)
    val_b = pn_to_int(b)
    val_cin = pn_to_int(cin)
    sum_val = val_a + val_b + val_cin

    # Map sum_val [-3, 3] to s and cout
    mapping = {
        -3: (0b00, 0b10), # Sum = 0, Carry = -1
        -2: (0b01, 0b10), # Sum = 1, Carry = -1
        -1: (0b10, 0b00), # Sum = -1, Carry = 0
         0: (0b00, 0b00), # Sum = 0, Carry = 0
         1: (0b01, 0b00), # Sum = 1, Carry = 0
         2: (0b10, 0b01), # Sum = -1, Carry = 1
         3: (0b00, 0b01), # Sum = 0, Carry = 1
    }
    return mapping.get(sum_val, (0b00, 0b00))

def golden_ternary_neg(trit):
    # Swap positive and negative rails
    pos = trit & 1
    neg = (trit >> 1) & 1
    return (pos << 1) | neg

def golden_ternary_mul_trit(a, b):
    val_a = pn_to_int(a)
    val_b = pn_to_int(b)
    return int_to_pn(val_a * val_b)

def golden_ternary_min(a, b):
    val_a = pn_to_int(a)
    val_b = pn_to_int(b)
    return int_to_pn(min(val_a, val_b))

def golden_ternary_max(a, b):
    val_a = pn_to_int(a)
    val_b = pn_to_int(b)
    return int_to_pn(max(val_a, val_b))

def golden_ternary_alu(A, B, Op):
    """
    Python-based emulator of the SV `ternary_alu` logic.
    """
    a0, a1, a2 = get_trits(A)
    b0, b1, b2 = get_trits(B)

    if Op == 0: # ADD
        s0, c0 = golden_ternary_full_adder(a0, b0, 0b00)
        s1, c1 = golden_ternary_full_adder(a1, b1, c0)
        s2, c2 = golden_ternary_full_adder(a2, b2, c1)
        return make_6bit(s0, s1, s2), c2

    elif Op == 1: # SUB
        nb0 = golden_ternary_neg(b0)
        nb1 = golden_ternary_neg(b1)
        nb2 = golden_ternary_neg(b2)
        s0, c0 = golden_ternary_full_adder(a0, nb0, 0b00)
        s1, c1 = golden_ternary_full_adder(a1, nb1, c0)
        s2, c2 = golden_ternary_full_adder(a2, nb2, c1)
        return make_6bit(s0, s1, s2), c2

    elif Op == 2: # NEG (-A)
        return make_6bit(golden_ternary_neg(a0), golden_ternary_neg(a1), golden_ternary_neg(a2)), 0b00

    elif Op == 3: # MUL (3-trit multiplication with partial products)
        # Shifted multiplication mimicking SV structure
        pp0_t0 = golden_ternary_mul_trit(a0, b0)
        pp0_t1 = golden_ternary_mul_trit(a1, b0)
        pp0_t2 = golden_ternary_mul_trit(a2, b0)

        pp1_t0 = 0b00
        pp1_t1 = golden_ternary_mul_trit(a0, b1)
        pp1_t2 = golden_ternary_mul_trit(a1, b1)

        pp2_t0 = 0b00
        pp2_t1 = 0b00
        pp2_t2 = golden_ternary_mul_trit(a0, b2)

        # sum_pp0_pp1
        s00, cp0 = golden_ternary_full_adder(pp0_t0, pp1_t0, 0b00)
        s01, cp1 = golden_ternary_full_adder(pp0_t1, pp1_t1, cp0)
        s02, cp2 = golden_ternary_full_adder(pp0_t2, pp1_t2, cp1)

        # final_mul_sum = sum_pp0_pp1 + pp2
        f0, cm0 = golden_ternary_full_adder(s00, pp2_t0, 0b00)
        f1, cm1 = golden_ternary_full_adder(s01, pp2_t1, cm0)
        f2, cm2 = golden_ternary_full_adder(s02, pp2_t2, cm1)

        return make_6bit(f0, f1, f2), cm2

    elif Op == 4: # MIN (tritwise minimum)
        return make_6bit(golden_ternary_min(a0, b0), golden_ternary_min(a1, b1), golden_ternary_min(a2, b2)), 0b00

    elif Op == 5: # MAX (tritwise maximum)
        return make_6bit(golden_ternary_max(a0, b0), golden_ternary_max(a1, b1), golden_ternary_max(a2, b2)), 0b00

    elif Op == 6: # LSH (Logical Shift Left: T0 <- 0, T1 <- T0, T2 <- T1, COUT <- T2)
        return make_6bit(0b00, a0, a1), a2

    elif Op == 7: # RSH (Logical Shift Right: T2 <- 0, T1 <- T2, T0 <- T1, COUT <- T0)
        return make_6bit(a1, a2, 0b00), a0

    return 0, 0


@pytest.mark.parametrize("a_val,b_val,op,expected_out,expected_cout", [
    # ADD: 1 + 1 = 2 (s0 = -1 (0b10), s1 = +1 (0b01), s2 = 0 (0b00)) -> 0b000110, CarryOut = 0
    (0b000001, 0b000001, 0, 0b000110, 0b00),

    # ADD: -1 + -1 = -2 (s0 = +1 (0b01), s1 = -1 (0b10), s2 = 0 (0b00)) -> 0b001001, CarryOut = 0
    (0b000010, 0b000010, 0, 0b001001, 0b00),

    # SUB: 1 - (-1) = 2 -> 0b000110, CarryOut = 0
    (0b000001, 0b000010, 1, 0b000110, 0b00),

    # NEG: -1 (0b10) -> +1 (0b01)
    (0b000010, 0b000000, 2, 0b000001, 0b00),

    # MUL: 1 * -1 = -1 (s = -1)
    (0b000001, 0b000010, 3, 0b000010, 0b00),

    # MIN: 1 (0b01) MIN -1 (0b10) = -1 (0b10)
    (0b000001, 0b000010, 4, 0b000010, 0b00),

    # MAX: 1 (0b01) MAX -1 (0b10) = 1 (0b01)
    (0b000001, 0b000010, 5, 0b000001, 0b00),

    # LSH: [1, -1, 0] (0b001001) shifted left -> [0, 1, -1] (0b100100), carry = T2 = 0
    (0b001001, 0b000000, 6, 0b100100, 0b00),

    # RSH: [1, -1, 0] (0b001001) shifted right -> [-1, 0, 0] (0b000010), carry = T0 = 1 (0b01)
    (0b001001, 0b000000, 7, 0b000010, 0b01),
])
def test_ternary_alu_golden_model(a_val, b_val, op, expected_out, expected_cout):
    out, cout = golden_ternary_alu(a_val, b_val, op)
    assert out == expected_out, f"Out mismatch! Got {bin(out)}, expected {bin(expected_out)}"
    assert cout == expected_cout, f"CarryOut mismatch! Got {bin(cout)}, expected {bin(expected_cout)}"


# ==========================================
# 3. Golden-Model Verification: Capability Bounds Checker
# ==========================================

class GoldenCapabilityChecker:
    def __init__(self):
        self.allowed = False
        self.violation_flag = False
        self.violation_code = 0

    def step(self, req_valid, req_addr, req_op, cap_base, cap_limit, cap_perms, cap_tag):
        if not req_valid:
            self.allowed = False
            self.violation_flag = False
            self.violation_code = 0
            return

        tag_fault = not cap_tag
        bounds_fault = req_addr < cap_base or req_addr >= cap_limit or cap_base > cap_limit
        perm_fault = False

        if not tag_fault and not bounds_fault:
            if req_op == 0 and not (cap_perms & 0b001): # Read
                perm_fault = True
            elif req_op == 1 and not (cap_perms & 0b010): # Write
                perm_fault = True
            elif req_op == 2 and not (cap_perms & 0b100): # Execute
                perm_fault = True
            elif req_op == 3: # Invalid Op
                perm_fault = True

        if tag_fault:
            self.allowed = False
            self.violation_flag = True
            self.violation_code = 1
        elif bounds_fault:
            self.allowed = False
            self.violation_flag = True
            self.violation_code = 2
        elif perm_fault:
            self.allowed = False
            self.violation_flag = True
            self.violation_code = 3
        else:
            self.allowed = True
            self.violation_flag = False
            self.violation_code = 0


def test_capability_bounds_checker_golden_model():
    checker = GoldenCapabilityChecker()

    # Scenario 1: Access allowed (Read, within bounds, tag high)
    checker.step(req_valid=True, req_addr=0x1000, req_op=0, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True)
    assert checker.allowed is True
    assert checker.violation_flag is False
    assert checker.violation_code == 0

    # Scenario 2: Tag fault (invalid capability)
    checker.step(req_valid=True, req_addr=0x1000, req_op=0, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=False)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.violation_code == 1 # INVALID_CAP

    # Scenario 3: Bounds fault (Address below base)
    checker.step(req_valid=True, req_addr=0x0FFF, req_op=0, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.violation_code == 2 # OUT_OF_BOUNDS

    # Scenario 4: Bounds fault (Address at limit)
    checker.step(req_valid=True, req_addr=0x2000, req_op=0, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.violation_code == 2 # OUT_OF_BOUNDS

    # Scenario 5: Permissions fault (Write denied)
    checker.step(req_valid=True, req_addr=0x1500, req_op=1, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x5, cap_tag=True) # perms=5 is Read+Execute
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.violation_code == 3 # PERMISSION_DENIED

    # Scenario 6: Tightened Bounds Fault (Malformed bounds: base > limit)
    checker.step(req_valid=True, req_addr=0x1500, req_op=0, cap_base=0x2000, cap_limit=0x1000, cap_perms=0x7, cap_tag=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.violation_code == 2 # OUT_OF_BOUNDS

    # Scenario 7: Tightened Permissions Fault (Invalid req_op == 3)
    checker.step(req_valid=True, req_addr=0x1500, req_op=3, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.violation_code == 3 # PERMISSION_DENIED
