# Capability-Based Memory Protection Emulator

> *An instruction-level CPU and RAM emulator simulating hardware-enforced object-capabilities and tagged-memory security.*

---

## Background

In conventional computer architectures (such as x86 and ARM), memory is treated as a flat, untyped array of bytes. Memory safety (such as preventing buffer overflows) is left to compilers and software runtimes. If software fails to check bounds, the hardware blindly executes the invalid access, leading to critical vulnerabilities (like buffer overflows, privilege escalation, and code injection).

A **Capability System** enforces security directly at the hardware level. Memory addresses are replaced by **Capabilities**: unforgeable, token-like pointers that combine:
1. **Base Address**: The start of the allocated memory range.
2. **Length/Bounds**: The exact size of the allocated range.
3. **Permissions (Rights)**: Permissions like Read (R), Write (W), and Execute (X).

### Key Architectural Concepts

1. **[Tagged Memory](../../GLOSSARY.md)**: To prevent software from forging capabilities (e.g., creating a capability by doing integer arithmetic), memory is "tagged" at the hardware level. Every word in RAM has an extra bit (the tag) indicating whether it is plain **Data** or a **Capability**. If software attempts to modify a capability as if it were data, the hardware automatically clears the capability tag, rendering it invalid.
2. **Bounds Checking**: Every load and store instruction must present a valid capability register. The CPU hardware automatically verifies that the accessed address is within the capability's `[Base, Base + Length)` range. If not, the hardware raises a fault.
3. **Domain Transitions (Object Calls)**: To safely call code in another protection domain (e.g., invoking a microkernel service or a third-party library), the CPU supports safe transitions. A user process calls a "sealed" capability, which the hardware securely unseals, switching the active capability register set to the target domain, and then restores the caller's rights upon return. This is the hardware basis of object-capabilities.

---

## Features of This Simulator

This simulator implements a complete register-level virtual CPU and Tagged RAM:
1. **Tagged RAM**: Simulated memory where each slot can contain either a `DataWord` (a raw integer/string) or a `CapabilityWord` (containing bounds and permissions).
2. **Virtual Registers**:
   - `D0` - `D3` (Data registers for arithmetic and logic).
   - `C0` - `C3` (Capability registers for memory operations).
3. **Instruction Set**:
   - **Data operations**: `LOAD_CONST`, `ADD`, `SUB`.
   - **Capability operations**: `DERIVE_CAP` (create a restricted sub-capability from an existing one), `LOAD_DATA`, `STORE_DATA`, `LOAD_CAP`, `STORE_CAP`.
   - **System/Transition operations**: `CALL_OBJECT` (performs a hardware-enforced domain transition to execute sandboxed code).
4. **Hardware Exception Engine**: Raises detailed exceptions for violations:
   - Buffer overflow / bounds check violation.
   - Missing permissions (e.g., attempting to write with a Read-Only capability).
   - Tag violation (e.g., attempting to load a capability from untagged memory or treating data as a capability).
5. **Interactive Attack Scenarios**:
   - **Scenario 1: Out-of-bounds Buffer Overflow**: Demonstrates how bounds checking stops an off-by-one or buffer-overflow attack.
   - **Scenario 2: Capability Forgery Attack**: Demonstrates how modifying capability memory clears the tag, preventing forgery.
   - **Scenario 3: Secure Domain Transition**: Demonstrates invoking an isolated logging service without exposing the caller's private memory.

---

## How to Run

Execute the script from the repository root:

```bash
python3 reconstructions/capability-security/capability_sim.py
```

The script runs the interactive attack scenarios and prints detailed CPU and register state traces.
