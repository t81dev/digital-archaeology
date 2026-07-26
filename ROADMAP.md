# ROADMAP

This document tracks priority excavations and research directions. Status indicators help contributors see what is active.

---

## Completed / Polished

### Core Architecture & Hardware
- [Analog Computing](../excavations/analog-computing.md)
- [Balanced Ternary](../excavations/balanced-ternary.md)
- [Cellular Automata Hardware](../excavations/cellular-automata-hardware.md)
- [Connection Machine](../excavations/connection-machine.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Neuromorphic Hardware](../excavations/neuromorphic-hardware.md)
- [Optical Computing](../excavations/optical-computing.md)
- [Reversible Computing](../excavations/reversible-computing.md)
- [Stack Machines](../excavations/stack-machines.md)
- [Systolic Arrays](../excavations/systolic-arrays.md)
- [Transputers](../excavations/transputers.md)
- [Wafer-Scale Integration](../excavations/wafer-scale-integration.md)

### Systems, Security & Operating Systems
- [Burroughs Large Systems](../excavations/burroughs-large-systems.md) *(new)*
- [Capability Systems](../excavations/capability-systems.md)
- [Inferno](../excavations/inferno.md)
- [Intel iAPX 432](../excavations/intel-iapx-432.md) *(new)*
- [Lisp Machines](../excavations/lisp-machines.md)
- [Multics](../excavations/multics.md) *(new)*
- [Plan 9](../excavations/plan-9.md)
- [Project Xanadu](../excavations/project-xanadu.md)

### Programming Languages & Paradigms
- [Occam](../excavations/occam.md)
- [Smalltalk](../excavations/smalltalk.md)
- [Symbolic AI](../excavations/symbolic-ai.md)

---

## Near Term (High Priority)

- **Molecular & Biocomputing Logic**
- **Superconducting & Cryogenic Microarchitectures (SFQ / RSFQ Logic)**
- **VLIW / EPIC Architectures** (e.g., Itanium lineage) — *strong links to microcode and compiler co-design*
- **Vector Supercomputing** (Cray-style architectures) — *complements Connection Machine and Systolic Arrays*

---

## Future / Exploratory

- DNA Computing
- Quantum Precursors & Early Hybrid Logic
- Microcode-Driven Custom CISC Engines
- Actor Model Hardware / Erlang-inspired designs
- BeOS / Haiku (advanced desktop OS concepts) — *ecosystem lock-in case study*

---

## Notes

- **Focus**: Prioritize items that create strong cross-links with existing excavations and patterns (especially Recurring Ideas, Ecosystem Lock-In, Forgotten Abstractions, and Economic Failures). New excavations should reference 3+ related works.
- New contributions **must** follow the [excavation template](../excavations/excavation-template.md) and include a modern relevance + lessons section.
- Continue expanding **Patterns**, **Modern Relevance**, FPGA reconstructions/simulations, timelines, and bibliography in parallel with new excavations.
- Aim for depth over breadth: Each new item should meaningfully advance synthesis across the map.

Contributions welcome on any item — start with an issue or draft PR. Recent additions (Systolic Arrays, Burroughs, iAPX 432, Multics) have significantly strengthened our coverage of stack/descriptor architectures and capability-like systems.

Last updated: July 26, 2026
