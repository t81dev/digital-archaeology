# Pattern Impact Audit: Recent Inclusions

> **An systematic mapping of architectural insights from Residue Number System (RNS), Logarithmic Number System (LNS), [Fluidic Logic](../GLOSSARY.md), [KeyKOS](../GLOSSARY.md)-style capabilities, and Prolog/WAM/FGCS logic-programming hardware against the Digital Archaeology pattern catalog.**

---

## 1. Executive Summary

This audit assesses the impact of five newly integrated excavations on the repository's core and emerging architectural patterns. It evaluates whether the recurrent structures visible in these alternative mathematical, protection, and execution substrates warrant the promotion of new, portable patterns or the refinement of existing ones.

---

## 2. Pattern Impact Audit Table

| Finding / Architectural Mechanism | Supporting Lineages | Existing Pattern Coverage | Proposed Action | Confidence | Risk of Overfit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[Interface / Conversion Tax](../patterns/interface-conversion-tax.md)** (The severe performance/resource penalty when translating representations/authority/signals to interface with the dominant ecosystem). | RNS (CRT/MRC), LNS (log/linear conversion), Fluidics (pressure-to-voltage), [KeyKOS](../GLOSSARY.md) (context-switch trap latency), Prolog (FFI/WAM data marshaling). | Partially under *[Ecosystem Lock-In](../patterns/ecosystem-lockin.md)* (as "switching costs"), but not treated as an active mathematical or physical barrier. | **Promote to New Pattern**: `patterns/interface-conversion-tax.md` (Candidate A) | High | Low (Highly generalizable across all hardware/software boundaries). |
| **Hybridization as the Primary Survival Mode** (Pure alternative architectures fail; they survive strictly as specialized coprocessors or integrated sub-layers). | RNS (FHE/Crypto coprocessors), LNS (quantized NPU tensor cores), Fluidics (mechanical/optoelectronic hybrids), Capabilities (CHERI registers/Wasm WASI), Prolog (embedded software WAM). | Partially under *[Heterogeneous Revival](../patterns/heterogeneous-revival.md)*, but focuses on the hybrid survival imperative versus pure standalone replacement. | **Refine and Merge** into `patterns/heterogeneous-revival.md` (Candidate B) to avoid redundancy and strengthen the existing pattern. | High | Very Low (Consolidates the core thesis of heterogeneous computing). |
| **[Abstract Machine Persistence](../patterns/abstract-machine-persistence.md)** (When custom hardware fails, compiling or mapping the model through a portable abstract machine preserves the paradigm). | Prolog/WAM (WAM outlived PSI/PIM hardware), [KeyKOS](../GLOSSARY.md) (capability models resurrected in WebAssembly/WASI runtimes). | Mentioned under *[Forgotten Abstractions](../patterns/forgotten-abstractions.md)*, but without identifying the specific hardware-to-software migration mechanism. | **Promote to New Pattern**: `patterns/abstract-machine-persistence.md` (Candidate C) | High | Medium (Requires distinction between general VM emulation and execution paradigm carriers). |
| **[Operator-Cost Inversion](../patterns/operator-cost-inversion.md)** (Changing representation inverts operator costs—making complex operations cheap while simple operations become complex). | LNS (Mul/Div become simple additions; Add/Sub require complex approximation), RNS (Add/Mul are $O(1)$ carry-free; comparison and division are non-local). | Not covered. Mentioned as localized anomalies, but is a fundamental mathematical design lever. | **Promote to New Pattern**: `patterns/operator-cost-inversion.md` (Candidate D) | High | Low (Applies directly to any non-positional or non-linear arithmetic representation). |
| **[Explicit Authority Substrate](../patterns/explicit-authority-substrate.md)** (Making authority explicit, unforgeable, and composable improves confinement but trades off ambient-authority compatibility). | [KeyKOS](../GLOSSARY.md) (unforgeable keys, Meters, Factories), Burroughs descriptors, iAPX 432. | Partially covered under *[Forgotten Abstractions](../patterns/forgotten-abstractions.md)* / *[Capability Systems](../excavations/capability-systems.md)* excavation, but the architectural trade-offs of explicit delegation vs. ambient authority lack formal pattern structure. | **Promote to New Pattern**: `patterns/explicit-authority-substrate.md` (Candidate E) | High | Low (Relevant to CHERI, capabilities, object capabilities, and WASI). |
| **Static Flow and Medium Leakage** (Substrates requiring active flow or continuous energy state retention experience severe static losses). | [Fluidic Logic](../GLOSSARY.md) (constant venting/power jet leakage), analogous to sub-nanometer CMOS static leakage. | Not covered in pattern catalog; local to substrate dynamics. | **Keep as Synthesis Note** in `synthesis/recent-inclusions-crosscut.md` (Do not promote to pattern to avoid overfitting non-electronic substrates). | Medium | High (Mainly maps [fluidic logic](../GLOSSARY.md) and nanoscale sub-micron CMOS). |

---

## 3. Rationale for New Pattern Promotions

### Candidate A: [Interface / Conversion Tax](../patterns/interface-conversion-tax.md)
*   **Recurrence**: Found in arithmetic converters (RNS's CRT/MRC), signal transducers (Fluidic electro-mechanical valves), security traps ([KeyKOS](../GLOSSARY.md) microkernel context switches), and language boundaries (Prolog's foreign function interface).
*   **Significance**: This "tax" is the primary economic and physical force that determines why a localized technical advantage (like 1-cycle logarithmic multiplication) fails to displace the mainstream. It shifts the design bottleneck from the execution core to the boundary interface.

### Candidate C: [Abstract Machine Persistence](../patterns/abstract-machine-persistence.md)
*   **Recurrence**: Demonstrates how the Warren Abstract Machine (WAM) preserved declarative logic programming past the collapse of FGCS hardware; similarly, the object-capability patterns of [KeyKOS](../GLOSSARY.md) survived by migrating into the WebAssembly VM (WASI) and [Google](../GLOSSARY.md)'s Zircon runtime.
*   **Significance**: It provides a concrete predictive signal for digital archaeology: software-defined virtual machines are highly durable carriers of alternative paradigms, outliving their specialized physical silicon hosts.

### Candidate D: [Operator-Cost Inversion](../patterns/operator-cost-inversion.md)
*   **Recurrence**: In LNS, operations of higher algebraic order (multiplication, division, roots) are reduced to simple addition or shifts, while addition is pushed to transcendental approximation. In RNS, multi-precision multiplication and addition become $O(1)$ carry-free operations, while magnitude comparison and division become non-local, multi-channel feedback loops.
*   **Significance**: A critical design pattern for domain-specific accelerators (NPUs, cryptoprocessors). It explains how representation selection is used as an architectural lever to bypass physical bottlenecks (like carry delay or ALU area constraints).

### Candidate E: [Explicit Authority Substrate](../patterns/explicit-authority-substrate.md)
*   **Recurrence**: Appears in [KeyKOS](../GLOSSARY.md), Burroughs descriptor-based systems, [Intel iAPX 432](../excavations/intel-iapx-432.md), and CHERI.
*   **Significance**: Highlights that unforgeable capabilities dramatically improve containment and least-privilege structures, but shift the architectural complexity from kernel protection into compilation, language bindings, and ecosystem-compatibility boundaries.

---

## 4. Rationale for Merges & Rejections

### Candidate B: Hybridization as Survival Mode
*   **Decision**: Merge into **[`patterns/heterogeneous-revival.md`](../patterns/heterogeneous-revival.md)**.
*   **Reasoning**: "Hybridization as Survival Mode" is the exact functional manifestation of *[Heterogeneous Revival](../patterns/heterogeneous-revival.md)*. Creating a separate pattern would cause massive redundancy. Instead, `heterogeneous-revival.md` will be strengthened by adding a dedicated section on the *hybrid survival imperative*, using RNS-binary coprocessors, LNS-NPU cores, fluidic-mechanical controllers, and CHERI register-level integrations as primary evidence.

---

## 5. Next Steps

1.  **Draft Admitted Patterns**: Create standalone files under `patterns/` for Candidates A, C, D, and E.
2.  **Refine Existing Patterns**: Apply patch-level updates to `ecosystem-lockin.md`, `constraint-migration.md`, `heterogeneous-revival.md`, `economic-failures.md`, `forgotten-abstractions.md`, and `recurring-ideas.md`.
3.  **Update Indexes**: Align `COMPARATIVE_INDEX.md` and `GLOSSARY.md`.
