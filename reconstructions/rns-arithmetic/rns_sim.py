#!/usr/bin/env python3
"""
Residue Number System (RNS) Arithmetic Simulator
Demonstrates residue encoding, component-wise carry-free modular operations (add/mul),
and backward conversion to standard positional notation via the Chinese Remainder Theorem (CRT).
"""

import math

class RNS:
    """
    Simulates a Residue Number System with a defined coprime moduli set.
    Allows encoding of decimal integers, carry-free parallel math, and CRT decoding.
    """
    def __init__(self, moduli: list):
        # Validate that moduli are pairwise coprime and greater than 1
        if any(m <= 1 for m in moduli):
            raise ValueError("Moduli must be integers strictly greater than 1.")

        for i in range(len(moduli)):
            for j in range(i + 1, len(moduli)):
                if math.gcd(moduli[i], moduli[j]) != 1:
                    raise ValueError(f"Moduli set {moduli} is not pairwise coprime. GCD({moduli[i]}, {moduli[j]}) = {math.gcd(moduli[i], moduli[j])}")

        self.moduli = moduli
        # Calculate dynamic range (M)
        self.M = math.prod(moduli)

        # Precompute CRT components to show conversion optimization
        self.m_hat = [self.M // m for m in moduli]
        self.m_hat_inv = []
        for i, m in enumerate(moduli):
            # Compute modular multiplicative inverse of m_hat[i] modulo m
            inv = self._mod_inverse(self.m_hat[i], m)
            self.m_hat_inv.append(inv)

    def _mod_inverse(self, a: int, m: int) -> int:
        """Computes modular inverse of a modulo m using Extended Euclidean Algorithm."""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"Modular inverse of {a} mod {m} does not exist.")

    def encode(self, x: int) -> list:
        """
        Encodes a decimal integer x into its residue representation.
        Enforces constraints regarding the dynamic range [0, M).
        Supports negative numbers inside the symmetric range [-M/2, M/2) by shifting.
        """
        if x < 0:
            # Wrap negative numbers within the range modulo M
            x = (x % self.M + self.M) % self.M

        if x >= self.M:
            # Represent overflow warning / out-of-range behavior
            raise ValueError(f"Integer {x} exceeds RNS dynamic range M = {self.M}.")

        return [x % m for m in self.moduli]

    def decode(self, residues: list, signed: bool = False) -> int:
        """
        Decodes RNS residue representation back to a standard decimal integer
        using the Chinese Remainder Theorem (CRT).
        Supports signed integer recovery by mapping values >= M/2 to negative space if signed=True.
        """
        if len(residues) != len(self.moduli):
            raise ValueError("Residues list length mismatch with moduli.")

        # Verify residues bounds
        for r, m in zip(residues, self.moduli):
            if r < 0 or r >= m:
                raise ValueError(f"Residue {r} is out of bounds for modulus {m}.")

        # Apply CRT: x = sum(r_i * m_hat_i * m_hat_inv_i) % M
        total = 0
        for i in range(len(self.moduli)):
            term = residues[i] * self.m_hat[i] * self.m_hat_inv[i]
            total += term

        x = total % self.M

        # Handle signed mapping (symmetric dynamic range representation)
        if signed and x >= self.M // 2:
            return x - self.M
        return x

    def add(self, r1: list, r2: list) -> list:
        """
        Performs component-wise, carry-free addition.
        (r1_i + r2_i) % m_i for each independent channel.
        """
        return [(r1[i] + r2[i]) % self.moduli[i] for i in range(len(self.moduli))]

    def multiply(self, r1: list, r2: list) -> list:
        """
        Performs component-wise, carry-free multiplication.
        (r1_i * r2_i) % m_i for each independent channel.
        """
        return [(r1[i] * r2[i]) % self.moduli[i] for i in range(len(self.moduli))]

    def subtract(self, r1: list, r2: list) -> list:
        """
        Performs component-wise, carry-free subtraction.
        (r1_i - r2_i) % m_i for each independent channel.
        """
        return [(r1[i] - r2[i] + self.moduli[i]) % self.moduli[i] for i in range(len(self.moduli))]


def run_demo():
    print("=== Residue Number System (RNS) Simulator Demo ===")

    # Define coprime moduli set
    moduli = [3, 5, 7]
    rns = RNS(moduli)
    print(f"Moduli: {rns.moduli}")
    print(f"Dynamic Range M: {rns.M} (Symmetric Range: [{-rns.M//2}, {rns.M//2}))")

    # Test encoding/decoding
    x = 12
    y = -8

    rx = rns.encode(x)
    ry = rns.encode(y)

    print(f"Encode {x} -> {rx}")
    print(f"Encode {y} -> {ry}")

    # Perform operations
    r_add = rns.add(rx, ry)
    r_sub = rns.subtract(rx, ry)
    r_mul = rns.multiply(rx, ry)

    print(f"Add Residues: {rx} + {ry} = {r_add}")
    print(f"Sub Residues: {rx} - {ry} = {r_sub}")
    print(f"Mul Residues: {rx} * {ry} = {r_mul}")

    # Decode back
    dec_add = rns.decode(r_add, signed=True)
    dec_sub = rns.decode(r_sub, signed=True)
    dec_mul = rns.decode(r_mul, signed=True)

    print(f"Decode Add: {r_add} -> {dec_add} (Expected: {x + y})")
    print(f"Decode Sub: {r_sub} -> {dec_sub} (Expected: {x - y})")
    print(f"Decode Mul: {r_mul} -> {dec_mul} (Expected: {x * y})")


if __name__ == "__main__":
    run_demo()
