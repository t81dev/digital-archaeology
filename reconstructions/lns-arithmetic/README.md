# Logarithmic Number System (LNS) Arithmetic Simulator

Demonstrates real-number encoding as sign and logarithm, simplifying multiplication/division to fixed-point addition/subtraction, and executing addition/subtraction via linear interpolation of the Jacobian Logarithm functions.

## Features
- Dynamic log encoding/decoding for any base (defaults to 2).
- Multiplication and division reduced to addition and subtraction of logarithms.
- Jacobian logarithmic approximation tables for addition ($F_p(d)$) and subtraction ($F_m(d)$).
- Linear interpolation engine over sampled lookup tables.
