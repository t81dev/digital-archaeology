#!/usr/bin/env python3
"""
Balanced Ternary & Mixed-Radix Simulator
Implements Base-3 ternary arithmetic, logic gates, and a multi-trit ALU.
"""

# Map characters to trit values
CHAR_TO_TRIT = {'1': 1, '0': 0, 'T': -1, 't': -1, '-': -1}
TRIT_TO_CHAR = {1: '1', 0: '0', -1: 'T'}

def decimal_to_ternary(n: int) -> str:
    """Convert a decimal integer to a Balanced Ternary string representation."""
    if n == 0:
        return "0"

    trits = []
    temp = n
    while temp != 0:
        remainder = temp % 3
        temp = temp // 3

        if remainder == 2:
            remainder = -1
            temp += 1
        elif remainder == -2:
            remainder = 1
            temp -= 1

        trits.append(TRIT_TO_CHAR[remainder])

    return "".join(reversed(trits))

def ternary_to_decimal(s: str) -> int:
    """Convert a Balanced Ternary string to a decimal integer."""
    s = s.strip().upper()
    if not s:
        return 0

    decimal_val = 0
    power = 0
    for char in reversed(s):
        if char not in CHAR_TO_TRIT:
            raise ValueError(f"Invalid trit character: '{char}'. Must be '1', '0', or 'T'.")
        trit = CHAR_TO_TRIT[char]
        decimal_val += trit * (3 ** power)
        power += 1
    return decimal_val

def ternary_not(t: int) -> int:
    """Ternary NOT gate (inversion)."""
    return -t

def ternary_and(t1: int, t2: int) -> int:
    """Ternary AND gate (minimum of two trits)."""
    return min(t1, t2)

def ternary_or(t1: int, t2: int) -> int:
    """Ternary OR gate (maximum of two trits)."""
    return max(t1, t2)

def trit_full_adder(a: int, b: int, c_in: int) -> tuple:
    """
    Single-trit full adder.
    Returns (sum_trit, carry_trit).
    """
    decimal_sum = a + b + c_in

    # Map decimal_sum (-3 to +3) to sum and carry trits
    # sum_val = (decimal_sum + 1) % 3 - 1, with carry logic
    if decimal_sum == 0:
        return 0, 0
    elif decimal_sum == 1:
        return 1, 0
    elif decimal_sum == 2:
        return -1, 1
    elif decimal_sum == 3:
        return 0, 1
    elif decimal_sum == -1:
        return -1, 0
    elif decimal_sum == -2:
        return 1, -1
    elif decimal_sum == -3:
        return 0, -1
    else:
        raise ValueError(f"Unexpected decimal sum in trit full adder: {decimal_sum}")

def pad_strings(s1: str, s2: str) -> tuple:
    """Pads two ternary strings with leading '0's to align lengths."""
    max_len = max(len(s1), len(s2))
    return s1.rjust(max_len, '0'), s2.rjust(max_len, '0')

def ternary_add(s1: str, s2: str, show_trace: bool = False) -> str:
    """
    Adds two Balanced Ternary strings.
    Optionally prints a step-by-step carry propagation trace.
    """
    s1_pad, s2_pad = pad_strings(s1.strip(), s2.strip())

    carry = 0
    result_trits = []

    if show_trace:
        print("\n--- Addition Trace ---")
        print(f"  A:  {s1_pad}")
        print(f"  B:  {s2_pad}")
        print("-" * (len(s1_pad) + 10))

    for a_char, b_char in zip(reversed(s1_pad), reversed(s2_pad)):
        a = CHAR_TO_TRIT[a_char]
        b = CHAR_TO_TRIT[b_char]

        s_trit, new_carry = trit_full_adder(a, b, carry)
        result_trits.append(TRIT_TO_CHAR[s_trit])

        if show_trace:
            print(f"  Trit addition: {a_char} + {b_char} (carry-in {TRIT_TO_CHAR[carry]}) -> sum {TRIT_TO_CHAR[s_trit]}, carry-out {TRIT_TO_CHAR[new_carry]}")

        carry = new_carry

    if carry != 0:
        result_trits.append(TRIT_TO_CHAR[carry])
        if show_trace:
            print(f"  Final remaining carry-out: {TRIT_TO_CHAR[carry]}")

    # Reverse to restore big-endian representation
    res = "".join(reversed(result_trits))
    # Strip leading zeros, preserving a single zero if result is 0
    res = res.lstrip('0')
    return res if res else "0"

def ternary_negate(s: str) -> str:
    """Negate a Balanced Ternary number by inverting all trits."""
    return "".join(TRIT_TO_CHAR[ternary_not(CHAR_TO_TRIT[c])] for c in s.strip())

def ternary_subtract(s1: str, s2: str, show_trace: bool = False) -> str:
    """
    Subtract s2 from s1 using addition with negation: s1 - s2 = s1 + (-s2).
    Demonstrates that subtraction requires zero additional logic in Balanced Ternary.
    """
    s2_neg = ternary_negate(s2)
    if show_trace:
        print(f"\nPerforming subtraction: {s1} - {s2}")
        print(f"Negating subtrahend: -({s2}) = {s2_neg}")
        print(f"Adding: {s1} + {s2_neg}")
    return ternary_add(s1, s2_neg, show_trace)

def ternary_multiply(s1: str, s2: str, show_trace: bool = False) -> str:
    """
    Multiply two Balanced Ternary numbers using shift-and-add.
    Because trits are {-1, 0, 1}, multiplication reduces to basic shifts,
    additions, and subtractions (via negation additions).
    """
    s1 = s1.strip().lstrip('0')
    s2 = s2.strip().lstrip('0')
    if not s1 or not s2 or s1 == "0" or s2 == "0":
        return "0"

    accum = "0"
    if show_trace:
        print(f"\n--- Multiplication Trace: {s1} * {s2} ---")

    for i, b_char in enumerate(reversed(s2)):
        b = CHAR_TO_TRIT[b_char]
        if b == 0:
            if show_trace:
                print(f"  Trit at 3^{i} is 0: adding nothing")
            continue

        # Shift s1 by i trits (append i zeros)
        shifted_s1 = s1 + ("0" * i)

        if b == 1:
            if show_trace:
                print(f"  Trit at 3^{i} is 1: adding shifted multiplicand {shifted_s1}")
            accum = ternary_add(accum, shifted_s1)
        elif b == -1:
            negated_shifted = ternary_negate(shifted_s1)
            if show_trace:
                print(f"  Trit at 3^{i} is T: adding negated shifted multiplicand {negated_shifted}")
            accum = ternary_add(accum, negated_shifted)

    accum = accum.lstrip('0')
    return accum if accum else "0"


class TernaryALU:
    """
    A simulated multi-trit Balanced Ternary ALU with supporting registers.
    """
    def __init__(self):
        # 3 registers holding Balanced Ternary strings.
        self.registers = {
            "R0": "0",
            "R1": "0",
            "R2": "0"
        }
        self.history = []

    def execute(self, instruction: str) -> str:
        """
        Executes a single assembly-like instruction.
        Format examples:
          "LOAD R0, 1T0"
          "ADD R2, R0, R1"
          "SUB R0, R1, R2"
          "MUL R1, R0, R2"
          "NEG R0, R1"
          "NOT R2, R0"
          "AND R1, R0, R2"
          "OR R0, R1, R2"
          "SHL R2, R1"
          "SHR R0, R2"
        """
        self.history.append(instruction)
        parts = [p.strip() for p in instruction.replace(",", " ").split() if p.strip()]
        if not parts:
            return "NOP"

        op = parts[0].upper()

        if op == "LOAD":
            reg, val = parts[1], parts[2]
            if reg not in self.registers:
                raise ValueError(f"Invalid register: {reg}")
            # Verify valid ternary string format
            for char in val.upper():
                if char not in CHAR_TO_TRIT:
                    raise ValueError(f"Invalid trit value: {char}")
            self.registers[reg] = val.upper()
            dest = reg

        elif op == "ADD":
            dest, src1, src2 = parts[1], parts[2], parts[3]
            v1 = self.registers[src1]
            v2 = self.registers[src2]
            self.registers[dest] = ternary_add(v1, v2)

        elif op == "SUB":
            dest, src1, src2 = parts[1], parts[2], parts[3]
            v1 = self.registers[src1]
            v2 = self.registers[src2]
            self.registers[dest] = ternary_subtract(v1, v2)

        elif op == "MUL":
            dest, src1, src2 = parts[1], parts[2], parts[3]
            v1 = self.registers[src1]
            v2 = self.registers[src2]
            self.registers[dest] = ternary_multiply(v1, v2)

        elif op == "NEG":
            dest, src = parts[1], parts[2]
            v = self.registers[src]
            self.registers[dest] = ternary_negate(v)

        elif op == "NOT":
            dest, src = parts[1], parts[2]
            v = self.registers[src]
            self.registers[dest] = "".join(TRIT_TO_CHAR[ternary_not(CHAR_TO_TRIT[c])] for c in v)

        elif op == "AND":
            dest, src1, src2 = parts[1], parts[2], parts[3]
            v1 = self.registers[src1]
            v2 = self.registers[src2]
            p1, p2 = pad_strings(v1, v2)
            res_trits = []
            for c1, c2 in zip(p1, p2):
                t1 = CHAR_TO_TRIT[c1]
                t2 = CHAR_TO_TRIT[c2]
                res_trits.append(TRIT_TO_CHAR[ternary_and(t1, t2)])
            self.registers[dest] = "".join(res_trits).lstrip('0') or "0"

        elif op == "OR":
            dest, src1, src2 = parts[1], parts[2], parts[3]
            v1 = self.registers[src1]
            v2 = self.registers[src2]
            p1, p2 = pad_strings(v1, v2)
            res_trits = []
            for c1, c2 in zip(p1, p2):
                t1 = CHAR_TO_TRIT[c1]
                t2 = CHAR_TO_TRIT[c2]
                res_trits.append(TRIT_TO_CHAR[ternary_or(t1, t2)])
            self.registers[dest] = "".join(res_trits).lstrip('0') or "0"

        elif op == "SHL":
            dest, src = parts[1], parts[2]
            v = self.registers[src]
            self.registers[dest] = (v + "0").lstrip('0') or "0"

        elif op == "SHR":
            dest, src = parts[1], parts[2]
            v = self.registers[src]
            # Right shift is truncating the last trit, naturally rounding to nearest integer!
            if len(v) <= 1:
                self.registers[dest] = "0"
            else:
                self.registers[dest] = v[:-1].lstrip('0') or "0"

        else:
            raise ValueError(f"Unknown operation: {op}")

        return self.registers[dest]


def run_self_test():
    """Run verification self-tests."""
    print("=== Balanced Ternary Self-Test ===")

    # Test conversions
    test_cases = [0, 1, -1, 2, -2, 5, -5, 13, -13, 121, -121, 2026, -2026]
    print("\nVerifying decimal <-> ternary conversions:")
    for num in test_cases:
        tern = decimal_to_ternary(num)
        back = ternary_to_decimal(tern)
        print(f"  {num:6d}  ==>  {tern:8s}  ==>  {back:6d}  [ {'OK' if num == back else 'FAIL'} ]")
        assert num == back, f"Conversion failed for {num}"

    # Test logic gates
    assert ternary_not(1) == -1
    assert ternary_not(0) == 0
    assert ternary_not(-1) == 1

    assert ternary_and(1, 0) == 0
    assert ternary_and(-1, 1) == -1
    assert ternary_and(1, 1) == 1

    assert ternary_or(1, 0) == 1
    assert ternary_or(-1, -1) == -1
    assert ternary_or(0, -1) == 0
    print("\nLogic gates: OK")

    # Test addition & subtraction
    print("\nVerifying basic arithmetic operations:")
    arithmetic_pairs = [
        (5, 8),      # positive + positive
        (13, -5),    # positive + negative (results in positive)
        (-15, -20),  # negative + negative
        (121, -121), # addition yielding zero
        (45, 12),    # subtraction
        (7, 9)       # subtraction yielding negative
    ]
    for x, y in arithmetic_pairs:
        s_x = decimal_to_ternary(x)
        s_y = decimal_to_ternary(y)

        # Add
        sum_tern = ternary_add(s_x, s_y)
        sum_dec = ternary_to_decimal(sum_tern)
        expected_sum = x + y
        print(f"  Add: {x} + {y} = {sum_dec} ({sum_tern}) [ {'OK' if sum_dec == expected_sum else 'FAIL'} ]")
        assert sum_dec == expected_sum

        # Subtract
        sub_tern = ternary_subtract(s_x, s_y)
        sub_dec = ternary_to_decimal(sub_tern)
        expected_sub = x - y
        print(f"  Sub: {x} - {y} = {sub_dec} ({sub_tern}) [ {'OK' if sub_dec == expected_sub else 'FAIL'} ]")
        assert sub_dec == expected_sub

    # Test multiplication
    mult_pairs = [
        (5, 5),
        (12, -3),
        (-9, -9),
        (0, 45),
        (15, 0),
        (2026, -3)
    ]
    for x, y in mult_pairs:
        s_x = decimal_to_ternary(x)
        s_y = decimal_to_ternary(y)
        mult_tern = ternary_multiply(s_x, s_y)
        mult_dec = ternary_to_decimal(mult_tern)
        expected_mult = x * y
        print(f"  Mult: {x} * {y} = {mult_dec} ({mult_tern}) [ {'OK' if mult_dec == expected_mult else 'FAIL'} ]")
        assert mult_dec == expected_mult

    print("\nAll self-tests passed successfully!\n")

def main():
    """Interactive CLI menu."""
    run_self_test()

    print("=" * 60)
    print("Welcome to the Interactive Balanced Ternary Simulator!")
    print("=" * 60)

    while True:
        print("\nChoose an option:")
        print("1. Convert Decimal to Balanced Ternary")
        print("2. Convert Balanced Ternary to Decimal")
        print("3. Add two numbers (with step-by-step trace)")
        print("4. Subtract two numbers (with step-by-step trace)")
        print("5. Multiply two numbers (with step-by-step trace)")
        print("6. Run Multi-Trit ALU Instruction Set Demo")
        print("7. Exit")

        try:
            choice = input("Enter choice (1-7): ").strip()
            if choice == '1':
                val = int(input("Enter decimal integer: ").strip())
                tern = decimal_to_ternary(val)
                print(f"Decimal {val} in Balanced Ternary: {tern}")
            elif choice == '2':
                tern = input("Enter Balanced Ternary string (using 1, 0, T): ").strip().upper()
                val = ternary_to_decimal(tern)
                print(f"Balanced Ternary {tern} in Decimal: {val}")
            elif choice == '3':
                x = int(input("Enter first decimal: ").strip())
                y = int(input("Enter second decimal: ").strip())
                s_x = decimal_to_ternary(x)
                s_y = decimal_to_ternary(y)
                print(f"Adding: {x} ({s_x}) + {y} ({s_y})")
                res = ternary_add(s_x, s_y, show_trace=True)
                print(f"\nResult Ternary: {res}")
                print(f"Result Decimal: {ternary_to_decimal(res)}")
            elif choice == '4':
                x = int(input("Enter first decimal: ").strip())
                y = int(input("Enter second decimal: ").strip())
                s_x = decimal_to_ternary(x)
                s_y = decimal_to_ternary(y)
                print(f"Subtracting: {x} ({s_x}) - {y} ({s_y})")
                res = ternary_subtract(s_x, s_y, show_trace=True)
                print(f"\nResult Ternary: {res}")
                print(f"Result Decimal: {ternary_to_decimal(res)}")
            elif choice == '5':
                x = int(input("Enter first decimal: ").strip())
                y = int(input("Enter second decimal: ").strip())
                s_x = decimal_to_ternary(x)
                s_y = decimal_to_ternary(y)
                print(f"Multiplying: {x} ({s_x}) * {y} ({s_y})")
                res = ternary_multiply(s_x, s_y, show_trace=True)
                print(f"\nResult Ternary: {res}")
                print(f"Result Decimal: {ternary_to_decimal(res)}")
            elif choice == '6':
                print("\nRunning Ternary ALU Demo:")
                alu = TernaryALU()
                # Demo instructions
                insts = [
                    "LOAD R0, 11",  # 4
                    "LOAD R1, 1T",  # 2
                    "ADD R2, R0, R1", # 4 + 2 = 6 (Ternary: 1T0)
                    "SUB R0, R2, R1", # 6 - 2 = 4 (Ternary: 11)
                    "MUL R1, R2, R0", # 6 * 4 = 24 (Ternary: 10T0)
                    "SHR R2, R1",     # 24 // 3 = 8 (Ternary: 10T)
                    "SHL R0, R2"      # 8 * 3 = 24 (Ternary: 10T0)
                ]
                for inst in insts:
                    res = alu.execute(inst)
                    print(f"  Executed: '{inst:<15}' ==> Registers: R0={alu.registers['R0']} ({ternary_to_decimal(alu.registers['R0'])}), R1={alu.registers['R1']} ({ternary_to_decimal(alu.registers['R1'])}), R2={alu.registers['R2']} ({ternary_to_decimal(alu.registers['R2'])})")
            elif choice == '7':
                print("Exiting Balanced Ternary Simulator. Goodbye!")
                break
            else:
                print("Invalid choice, please select between 1 and 7.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
