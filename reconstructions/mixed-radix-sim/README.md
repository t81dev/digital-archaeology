# [Balanced Ternary](../../excavations/balanced-ternary.md) & Mixed-Radix Simulator

> *An executable model of Base-3 arithmetic and logic, demonstrating the unique properties of Setun-style architectures.*

---

## Background

In standard binary computing, numbers are represented using base-2 with digits `{0, 1}`. Representing negative numbers requires special conventions, such as two's complement, which introduces an asymmetry around zero (e.g., -128 to 127 in 8-bit integers) and requires dedicated hardware paths for subtraction.

**[Balanced Ternary](../../excavations/balanced-ternary.md)** is a positional numeral system using base-3 with three digits (called **trits**):
- `-1` (often represented as `T` or `-`)
- `0`
- `+1` (often represented as `1` or `+`)

### Why [Balanced Ternary](../../excavations/balanced-ternary.md)?

1. **[Radix Economy](../../GLOSSARY.md)**: The theoretical optimum radix for representation efficiency is the mathematical constant $e \approx 2.718$. Three is closer to $e$ than two, meaning base-3 is mathematically more efficient than base-2 at representing numbers with a given number of states.
2. **Symmetric Representation**: The sign of the number is embedded in the digits themselves. The most significant non-zero trit determines whether the number is positive or negative.
3. **Trivial Negation**: Negating a number is accomplished by simply inverting the signs of all its trits (`1` becomes `T`, `T` becomes `1`, `0` remains `0`).
4. **No-Borrow Subtraction**: Subtraction ($A - B$) is performed as addition ($A + (-B)$), entirely eliminating the need for complex borrowing logic in the ALU.
5. **Round-to-Nearest**: Truncating or rounding a [balanced ternary](../../excavations/balanced-ternary.md) number is identical to rounding to the nearest integer, avoiding the bias of truncating binary.

---

## Features of This Simulator

This simulator implements:
1. **Decimal-Ternary Converters**: Convert arbitrary decimal integers to [balanced ternary](../../excavations/balanced-ternary.md) strings and vice versa.
2. **Ternary Logic Gates**: Implements Kleene-style ternary operators:
   - **NOT** (negation)
   - **AND** (min)
   - **OR** (max)
   - **XOR** (ternary sum modulo 3)
3. **Single-Trit Full Adder**: Calculates the sum and carry trits for three input trits (A, B, Carry-In).
4. **Multi-Trit Ripple-Carry Adder**: Adds two arbitrary-length [balanced ternary](../../excavations/balanced-ternary.md) numbers, demonstrating that addition and subtraction share the identical hardware path.
5. **Multi-Trit Multiplier**: Implements Shift-and-Add multiplication for [balanced ternary](../../excavations/balanced-ternary.md).

---

## How to Run

Execute the script from the repository root:

```bash
python3 reconstructions/mixed-radix-sim/ternary_sim.py
```

The script runs a comprehensive interactive test suite and demonstration, illustrating every aspect of ternary arithmetic.
