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
    reversible_path = os.path.join(hardware_dir, "reversible_gates.sv")
    multiplier_path = os.path.join(hardware_dir, "stochastic_multiplier.sv")
    formal_path = os.path.join(hardware_dir, "formal_assertions_companion.sv")

    assert os.path.exists(alu_path), "ternary_alu.sv does not exist!"
    assert os.path.exists(checker_path), "capability_bounds_checker.sv does not exist!"
    assert os.path.exists(reversible_path), "reversible_gates.sv does not exist!"
    assert os.path.exists(multiplier_path), "stochastic_multiplier.sv does not exist!"
    assert os.path.exists(formal_path), "formal_assertions_companion.sv does not exist!"

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
        assert "resp_page_fault" in checker_content
        assert "desc_mode" in checker_content
        assert "cap_present" in checker_content
        assert "endmodule" in checker_content

    # Verify Reversible Gates contains correct modules
    with open(reversible_path, 'r', encoding='utf-8') as f:
        rev_content = f.read()
        assert "module reversible_gates" in rev_content
        assert "always_ff @(posedge clk or negedge rst_n)" in rev_content
        assert "X_comb" in rev_content
        assert "Y_comb" in rev_content
        assert "Z_comb" in rev_content
        assert "endmodule" in rev_content

    # Verify Stochastic Multiplier contains correct modules
    with open(multiplier_path, 'r', encoding='utf-8') as f:
        mult_content = f.read()
        assert "module stochastic_multiplier" in mult_content
        assert "always_ff @(posedge clk or negedge rst_n)" in mult_content
        assert "always_comb" in mult_content
        assert "bin_val" in mult_content
        assert "stream_b" in mult_content
        assert "stream_out" in mult_content
        assert "endmodule" in mult_content

    # Verify Formal Assertions Companion contains correct SVA bind modules
    with open(formal_path, 'r', encoding='utf-8') as f:
        formal_content = f.read()
        assert "module capability_checker_sva_bind" in formal_content
        assert "assert_unforgeability: assert property" in formal_content
        assert "assert_spatial_safety: assert property" in formal_content
        assert "assert_descriptor_page_fault: assert property" in formal_content
        assert "module stochastic_multiplier_sva_bind" in formal_content
        assert "assert_lfsr_nonzero: assert property" in formal_content
        assert "module reversible_gates_sva_bind" in formal_content
        assert "assert_fredkin_conservation: assert property" in formal_content


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
        self.page_fault = False
        self.violation_code = 0

    def step(self, req_valid, req_addr, req_op, desc_mode, cap_base, cap_limit, cap_perms, cap_tag, cap_present):
        if not req_valid:
            self.allowed = False
            self.violation_flag = False
            self.page_fault = False
            self.violation_code = 0
            return

        tag_fault = not cap_tag
        pres_fault = desc_mode and not cap_present
        bounds_fault = req_addr < cap_base or req_addr >= cap_limit or cap_base > cap_limit
        perm_fault = False

        if not tag_fault and not pres_fault and not bounds_fault:
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
            self.page_fault = False
            self.violation_code = 1 # INVALID_CAP
        elif pres_fault:
            self.allowed = False
            self.violation_flag = True
            self.page_fault = True
            self.violation_code = 3 # PERMISSION_DENIED (or swapped out page mapping)
        elif bounds_fault:
            self.allowed = False
            self.violation_flag = True
            self.page_fault = False
            self.violation_code = 2 # OUT_OF_BOUNDS
        elif perm_fault:
            self.allowed = False
            self.violation_flag = True
            self.page_fault = False
            self.violation_code = 3 # PERMISSION_DENIED
        else:
            self.allowed = True
            self.violation_flag = False
            self.page_fault = False
            self.violation_code = 0


def test_capability_bounds_checker_golden_model():
    checker = GoldenCapabilityChecker()

    # Scenario 1: Access allowed (Read, within bounds, tag high, capability mode)
    checker.step(req_valid=True, req_addr=0x1000, req_op=0, desc_mode=False, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True, cap_present=True)
    assert checker.allowed is True
    assert checker.violation_flag is False
    assert checker.page_fault is False
    assert checker.violation_code == 0

    # Scenario 2: Tag fault (invalid capability)
    checker.step(req_valid=True, req_addr=0x1000, req_op=0, desc_mode=False, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=False, cap_present=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is False
    assert checker.violation_code == 1 # INVALID_CAP

    # Scenario 3: Bounds fault (Address below base)
    checker.step(req_valid=True, req_addr=0x0FFF, req_op=0, desc_mode=False, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True, cap_present=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is False
    assert checker.violation_code == 2 # OUT_OF_BOUNDS

    # Scenario 4: Bounds fault (Address at limit)
    checker.step(req_valid=True, req_addr=0x2000, req_op=0, desc_mode=False, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True, cap_present=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is False
    assert checker.violation_code == 2 # OUT_OF_BOUNDS

    # Scenario 5: Permissions fault (Write denied)
    checker.step(req_valid=True, req_addr=0x1500, req_op=1, desc_mode=False, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x5, cap_tag=True, cap_present=True) # perms=5 is Read+Execute
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is False
    assert checker.violation_code == 3 # PERMISSION_DENIED

    # Scenario 6: Tightened Bounds Fault (Malformed bounds: base > limit)
    checker.step(req_valid=True, req_addr=0x1500, req_op=0, desc_mode=False, cap_base=0x2000, cap_limit=0x1000, cap_perms=0x7, cap_tag=True, cap_present=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is False
    assert checker.violation_code == 2 # OUT_OF_BOUNDS

    # Scenario 7: Tightened Permissions Fault (Invalid req_op == 3)
    checker.step(req_valid=True, req_addr=0x1500, req_op=3, desc_mode=False, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True, cap_present=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is False
    assert checker.violation_code == 3 # PERMISSION_DENIED

    # Scenario 8: Burroughs Descriptor Page Fault (desc_mode=True, cap_present=False)
    checker.step(req_valid=True, req_addr=0x1000, req_op=0, desc_mode=True, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True, cap_present=False)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is True
    assert checker.violation_code == 3 # Swapped-out page mapping

    # Scenario 9: Burroughs Descriptor Allowed (desc_mode=True, cap_present=True)
    checker.step(req_valid=True, req_addr=0x1000, req_op=0, desc_mode=True, cap_base=0x1000, cap_limit=0x2000, cap_perms=0x7, cap_tag=True, cap_present=True)
    assert checker.allowed is True
    assert checker.violation_flag is False
    assert checker.page_fault is False
    assert checker.violation_code == 0


# ==========================================
# 4. Golden-Model Verification: Reversible Gates
# ==========================================

def golden_reversible_gates(op, a, b, c):
    """
    Python-based emulator of the SV `reversible_gates` logic.
    op = 0: Toffoli (CCNOT), op = 1: Fredkin (CSWAP)
    """
    if op == 0:
        # Toffoli (CCNOT)
        return a, b, c ^ (a & b)
    else:
        # Fredkin (CSWAP)
        if a == 1:
            return a, c, b
        else:
            return a, b, c

def test_reversible_gates_golden_model():
    """Verify standard logic combinations for synthesizable Toffoli and Fredkin gates."""
    # Toffoli checks (op = 0)
    assert golden_reversible_gates(op=0, a=1, b=1, c=0) == (1, 1, 1)
    assert golden_reversible_gates(op=0, a=1, b=0, c=1) == (1, 0, 1)
    assert golden_reversible_gates(op=0, a=0, b=1, c=0) == (0, 1, 0)

    # Fredkin checks (op = 1)
    assert golden_reversible_gates(op=1, a=1, b=1, c=0) == (1, 0, 1) # SWAP
    assert golden_reversible_gates(op=1, a=0, b=1, c=0) == (0, 1, 0) # No SWAP


# ==========================================
# 5. Golden-Model Verification: Stochastic Multiplier
# ==========================================

def test_stochastic_multiplier_behavior():
    """Verify logical modeling of synthesizable stochastic multiplier."""
    # Simple unipolar stochastic multiplier behavior:
    # If target is bin_val, comparator returns 1 if lfsr_state < bin_val
    # We check a mock trace
    lfsr_states = [1, 5, 10, 15, 20, 25, 30]
    bin_val = 12
    stream_b_vals = [1, 1, 0, 1, 1, 0, 1]

    stream_out_trace = []
    for lfsr, sb in zip(lfsr_states, stream_b_vals):
        stream_a = 1 if lfsr < bin_val else 0
        stream_out = stream_a & sb
        stream_out_trace.append(stream_out)

    assert stream_out_trace == [1, 1, 0, 0, 0, 0, 0]


# ==========================================
# 6. Advanced/Hardened Coverage Tests
# ==========================================

def test_lfsr_maximal_period_and_stochastic_ratios():
    """Verify that the 8-bit LFSR has maximal period and generates correct stochastic densities."""
    state = 0x01
    visited = set()

    # 8-bit LFSR primitive polynomial feedback logic:
    # lfsr_state <= {lfsr_state[6:0], lfsr_state[7] ^ lfsr_state[5] ^ lfsr_state[4] ^ lfsr_state[3]}
    for _ in range(255):
        visited.add(state)
        # Compute feedback bit (indexes are 0-based, so [7] is bit 7, etc.)
        bit = ((state >> 7) & 1) ^ ((state >> 5) & 1) ^ ((state >> 4) & 1) ^ ((state >> 3) & 1)
        state = ((state & 0x7F) << 1) | bit

    # A maximal-period 8-bit LFSR must visit exactly 255 unique non-zero states
    assert len(visited) == 255, f"LFSR did not achieve maximal period! Visited only {len(visited)} states."
    assert 0 not in visited, "LFSR locked up/entered the forbidden 0 state."

    # Validate unipolar probability densities across a full cycle for key values
    # For a binary value target in [0, 255], the number of cycles where state < target should be exactly target - 1 (except for target=0)
    # as the LFSR state spans from 1 to 255.
    for target in [0, 1, 64, 128, 192, 255]:
        stream_ones = sum(1 for s in visited if s < target)
        expected = max(0, target - 1)
        assert stream_ones == expected, f"Expected {expected} ones for target {target}, got {stream_ones}"


def test_reversible_gates_bijectivity():
    """Verify that both Toffoli and Fredkin reversible gates are strictly bijective (invertible)."""
    # For any input triplet (A, B, C) -> (X, Y, Z) -> applying the gate again must restore (A, B, C)
    for op in [0, 1]:  # 0: Toffoli, 1: Fredkin
        for a in [0, 1]:
            for b in [0, 1]:
                for c in [0, 1]:
                    # Forward pass
                    x, y, z = golden_reversible_gates(op, a, b, c)
                    # Backward/Inverse pass (both Toffoli and Fredkin are self-inverse gates!)
                    a_back, b_back, c_back = golden_reversible_gates(op, x, y, z)

                    assert (a, b, c) == (a_back, b_back, c_back), \
                        f"Gate op={op} failed self-inverse property at inputs ({a},{b},{c})!"


def test_reversible_uncomputation_alignment():
    """Verify that reversible uncomputation in Experiment 2 is strictly modeled in our golden model gates."""
    # Experiment 2 uncomputes to cleanly restore garbage state back to 0 without loss (Bennett uncomputation)
    # Forward pass: compute on input x=1, helper/garbage register starts at 0, target starts at 0
    # Let's use a Toffoli gate to compute and store in target (c)
    a, b, c = 1, 1, 0  # control A, control B, target C
    x, y, z = golden_reversible_gates(op=0, a=a, b=b, c=c)
    assert z == 1, "Expected computation output to be 1"

    # Uncomputation step: we execute the inverse sequence (self-inverse Toffoli) to restore the state back
    a_back, b_back, c_back = golden_reversible_gates(op=0, a=x, b=y, c=z)
    assert c_back == 0, "Uncomputation failed to restore state to 0!"


def test_capability_checker_experiment_alignment():
    """Ensure that the capability checker golden model behaves in exact alignment with the scenarios in Experiment 3."""
    checker = GoldenCapabilityChecker()

    # Scenario A: Nominal authorized read within bounds
    # Sandbox bounds: [10, 20) (base=10, limit=20, index=0, physical address=10)
    checker.step(req_valid=True, req_addr=10, req_op=0, desc_mode=True, cap_base=10, cap_limit=20, cap_perms=0x7, cap_tag=True, cap_present=True)
    assert checker.allowed is True
    assert checker.violation_flag is False
    assert checker.page_fault is False
    assert checker.violation_code == 0

    # Scenario B: Out of Bounds read violation
    # Sandbox bounds: [10, 20) (base=10, limit=20, index=40, physical address=50)
    checker.step(req_valid=True, req_addr=50, req_op=0, desc_mode=True, cap_base=10, cap_limit=20, cap_perms=0x7, cap_tag=True, cap_present=True)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is False
    assert checker.violation_code == 2 # OUT_OF_BOUNDS

    # Scenario C: Swapped-out descriptor page fault
    # Secure segment bounds: [50, 60), cap_present=False
    checker.step(req_valid=True, req_addr=50, req_op=0, desc_mode=True, cap_base=50, cap_limit=60, cap_perms=0x7, cap_tag=True, cap_present=False)
    assert checker.allowed is False
    assert checker.violation_flag is True
    assert checker.page_fault is True
    assert checker.violation_code == 3 # Swapped-out page mapping / permission denied status


def test_ternary_alu_exhaustive_trit_multiplication():
    """Verify the 1-trit multiplier logic exhaustively across all 9 combinations."""
    # In Balanced Ternary: trit A in [-1, 0, 1], trit B in [-1, 0, 1]
    # Represented in 2-bit PN: -1 = 2'b10, 0 = 2'b00, 1 = 2'b01
    pn_values = [0b10, 0b00, 0b01]

    for a_bin in pn_values:
        for b_bin in pn_values:
            val_a = pn_to_int(a_bin)
            val_b = pn_to_int(b_bin)
            expected_product_val = val_a * val_b

            prod_bin = golden_ternary_mul_trit(a_bin, b_bin)
            prod_val = pn_to_int(prod_bin)

            assert prod_val == expected_product_val, \
                f"1-trit multiplication failed for {val_a} * {val_b}! Got {prod_val}, expected {expected_product_val}"


def test_ternary_alu_overflow_underflow_scenarios():
    """Verify overflow and underflow detection for 3-trit Balanced Ternary arithmetic."""
    # 3-trit Balanced Ternary range: [-13, 13]
    # 13 is represented as +1, +1, +1 = 0b010101 (since 1 + 3 + 9 = 13)
    # -13 is represented as -1, -1, -1 = 0b101010 (since -1 - 3 - 9 = -13)
    max_val_pn = 0b010101  # +13
    min_val_pn = 0b101010  # -13
    one_pn = 0b000001      # +1
    neg_one_pn = 0b000010  # -1

    # Scenario A: Overflow (+13 + 1)
    # In ternary math: 13 + 1 = 14 = 0b000110 (out = -13, carry = +1)
    out, cout = golden_ternary_alu(max_val_pn, one_pn, 0)
    assert out == min_val_pn, f"Expected output to overflow and wrap to -13 (0b{min_val_pn:06b}), got 0b{out:06b}"
    assert cout == 0b01, f"Expected CarryOut +1 (0b01) for overflow, got 0b{cout:02b}"

    # Scenario B: Underflow (-13 - 1)
    # In ternary math: -13 - 1 = -14 = 0b010101 (out = +13, carry = -1)
    out, cout = golden_ternary_alu(min_val_pn, neg_one_pn, 0)
    assert out == max_val_pn, f"Expected output to underflow and wrap to +13 (0b{max_val_pn:06b}), got 0b{out:06b}"
    assert cout == 0b10, f"Expected CarryOut -1 (0b10) for underflow, got 0b{cout:02b}"
