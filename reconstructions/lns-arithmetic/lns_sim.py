#!/usr/bin/env python3
"""
Logarithmic Number System (LNS) Simulator
Demonstrates real-number encoding as sign and logarithm, simplifying multiplication/division
to fixed-point addition/subtraction, and executing addition/subtraction via lookup tables
and linear interpolation of the Jacobian Logarithm functions.
"""

import math

class LNS:
    """
    Simulates a Logarithmic Number System.
    Numbers are represented as a tuple: (sign, log_value)
    where:
      - sign is 1 for positive, -1 for negative, 0 for zero.
      - log_value is the log (base b) of the absolute value of the number.
      - b is the logarithm base (defaults to 2).
    """
    def __init__(self, base: float = 2.0, table_size: int = 100):
        self.base = base
        self.ln_base = math.log(base)
        self.table_size = table_size

        # Precompute lookup tables for addition/subtraction approximations:
        # F_p(d) = log_b(1 + b^-d) for addition
        # F_m(d) = log_b(1 - b^-d) for subtraction
        # We sample d in [0, 8.0]
        self.d_max = 8.0
        self.table_add = []
        self.table_sub = []

        for i in range(table_size):
            d = (i / (table_size - 1)) * self.d_max
            # Addition function
            f_p = math.log(1.0 + base ** (-d)) / self.ln_base
            self.table_add.append(f_p)

            # Subtraction function
            # Clamp to prevent division by zero or log of negative number when d=0
            if d == 0:
                # Theoretically -infinity, we use a placeholder or clamp d slightly
                f_m = -999.0
            else:
                f_m = math.log(abs(1.0 - base ** (-d))) / self.ln_base
            self.table_sub.append(f_m)

    def encode(self, val: float) -> tuple:
        """Encodes a standard float into LNS representation (sign, log_val)."""
        if val == 0.0:
            return (0, -999.0)  # -999.0 represents -infinity/underflow
        sign = 1 if val > 0 else -1
        log_val = math.log(abs(val)) / self.ln_base
        return (sign, log_val)

    def decode(self, lns_val: tuple) -> float:
        """Decodes an LNS representation back to a standard float."""
        sign, log_val = lns_val
        if sign == 0 or log_val <= -900.0:
            return 0.0
        return sign * (self.base ** log_val)

    def multiply(self, x: tuple, y: tuple) -> tuple:
        """
        LNS Multiplication: Sign is XORed, logs are added.
        """
        sign_x, log_x = x
        sign_y, log_y = y

        if sign_x == 0 or sign_y == 0:
            return (0, -999.0)

        sign_out = sign_x * sign_y
        log_out = log_x + log_y
        return (sign_out, log_out)

    def divide(self, x: tuple, y: tuple) -> tuple:
        """
        LNS Division: Sign is XORed, logs are subtracted.
        """
        sign_x, log_x = x
        sign_y, log_y = y

        if sign_x == 0:
            return (0, -999.0)
        if sign_y == 0:
            raise ZeroDivisionError("LNS Division by zero.")

        sign_out = sign_x * sign_y
        log_out = log_x - log_y
        return (sign_out, log_out)

    def _interpolate_table(self, d: float, table: list) -> float:
        """Interpolates lookup table to approximate Jacobian log functions."""
        if d >= self.d_max:
            return 0.0
        if d < 0:
            d = 0.0

        # Linear interpolation
        idx_f = (d / self.d_max) * (self.table_size - 1)
        idx_low = int(math.floor(idx_f))
        idx_high = min(idx_low + 1, self.table_size - 1)

        weight = idx_f - idx_low

        val_low = table[idx_low]
        val_high = table[idx_high]

        return val_low + weight * (val_high - val_low)

    def add(self, x: tuple, y: tuple) -> tuple:
        """
        LNS Addition using Jacobian Logarithm approximation:
        log_b(A + B) = log_b(A) + s_p(d) where d = |log_b(A) - log_b(B)|
        and s_p(d) = log_b(1 + b^-d).
        Handles sign differences by delegating to subtract.
        """
        sign_x, log_x = x
        sign_y, log_y = y

        # Identity cases
        if sign_x == 0:
            return y
        if sign_y == 0:
            return x

        # Handle signs
        if sign_x != sign_y:
            # Delegate to subtract: A + (-B) = A - B
            return self.subtract(x, (sign_x, log_y))

        # Core Jacobian addition
        max_log = max(log_x, log_y)
        min_log = min(log_x, log_y)
        d = max_log - min_log

        # Approximate F_p(d)
        f_p = self._interpolate_table(d, self.table_add)

        return (sign_x, max_log + f_p)

    def subtract(self, x: tuple, y: tuple) -> tuple:
        """
        LNS Subtraction using Jacobian Logarithm approximation:
        log_b(A - B) = log_b(A) + s_m(d) where d = |log_b(A) - log_b(B)|
        and s_m(d) = log_b(|1 - b^-d|).
        """
        sign_x, log_x = x
        sign_y, log_y = y

        # Identity cases
        if sign_y == 0:
            return x
        if sign_x == 0:
            return (-sign_y, log_y)

        # Handle signs: A - (-B) = A + B
        if sign_x != sign_y:
            return self.add(x, (sign_x, log_y))

        # Core subtraction: A - B
        if log_x == log_y:
            return (0, -999.0)

        max_log = max(log_x, log_y)
        min_log = min(log_x, log_y)
        d = max_log - min_log

        f_m = self._interpolate_table(d, self.table_sub)

        # Result sign depends on which operand was larger
        res_sign = sign_x if log_x > log_y else -sign_x
        return (res_sign, max_log + f_m)


def run_demo():
    print("=== Logarithmic Number System (LNS) Simulator Demo ===")
    lns = LNS(base=2.0)

    # Test multiplications and divisions
    v1 = 4.0
    v2 = 0.5

    x = lns.encode(v1)
    y = lns.encode(v2)

    print(f"Encode {v1} -> {x}")
    print(f"Encode {v2} -> {y}")

    prod = lns.multiply(x, y)
    print(f"Mul: {x} * {y} = {prod} -> decode {lns.decode(prod)} (Expected: {v1 * v2})")

    div = lns.divide(x, y)
    print(f"Div: {x} / {y} = {div} -> decode {lns.decode(div)} (Expected: {v1 / v2})")

    # Test addition and subtraction
    a = 15.0
    b = 3.0

    la = lns.encode(a)
    lb = lns.encode(b)

    l_sum = lns.add(la, lb)
    l_diff = lns.subtract(la, lb)

    print(f"Add: {la} + {lb} = {l_sum} -> decode {lns.decode(l_sum)} (Expected: {a + b})")
    print(f"Sub: {la} - {lb} = {l_diff} -> decode {lns.decode(l_diff)} (Expected: {a - b})")


if __name__ == "__main__":
    run_demo()
