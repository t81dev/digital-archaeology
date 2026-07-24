# Hardware Timeline

> *Evolution of computing hardware with emphasis on architectural diversity, specialization, and rediscovered ideas.*

---

## 1940s–1950s: Early Electronic Era

- Vacuum tubes and relays
- ENIAC, EDVAC, UNIVAC
- Early exploration of number systems (binary dominant but not universal)
- Emergence of the von Neumann architecture

**Key note**: Multiple number systems (binary, decimal, ternary) were still actively considered.

---

## 1960s: Mainframes and Architectural Experimentation

- Transistor-based systems
- IBM System/360 — family compatibility concept
- Early supercomputers (CDC 6600)
- Research into non-von Neumann architectures

---

## 1970s: Minicomputers and Microprocessors

- PDP series (DEC)
- Intel 4004 (1971) → 8080, Z80, 6502
- Rise of personal computing hardware
- Early parallel and distributed system research

---

## 1980s: The Peak of Diversity

- **Lisp Machines** — Symbolic computing hardware
- **Transputers** — Massively parallel message-passing chips
- Dataflow machines (Manchester, MIT Tagged-Token)
- Graphics accelerators begin to emerge
- RISC vs CISC wars

**This decade represents one of the highest points of architectural experimentation in history.**

**Key excavation links**:
- [Lisp Machines](../excavations/lisp-machines.md)
- [Transputers](../excavations/transputers.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Balanced Ternary](../excavations/balanced-ternary.md)

---

## 1990s–2000s: Consolidation and Commoditization

- x86 dominance (Intel, AMD)
- PowerPC, ARM rise in embedded/mobile
- GPUs evolve from graphics to general computing
- Multi-core era begins (power wall hits)

**Pattern highlight**: Strong ecosystem lock-in around commodity components.

---

## 2010s–Present: Heterogeneous & Domain-Specific Era

- Explosion of specialized accelerators
- GPUs become default AI training engines
- TPUs, NPUs, and custom AI silicon
- FPGA resurgence for prototyping and acceleration
- Return of research into alternative number systems, in-memory computing, neuromorphic chips, and optical computing

**Current period**: Greatest architectural diversity since the 1980s, driven by AI and efficiency demands.

---

## Major Hardware Trends

| Era              | Dominant Approach          | Key Characteristic                  |
|------------------|----------------------------|-------------------------------------|
| 1950s–1960s      | Mainframes                 | General-purpose, expensive          |
| 1970s–1980s      | Microprocessors + Custom   | High diversity                      |
| 1990s–2000s      | Commodity x86 + GPUs       | Standardization & scaling           |
| 2010s–Present    | Heterogeneous + Specialized| Domain-specific accelerators        |

---

## Recurring Hardware Ideas

- Alternative number systems (ternary, posits, logarithmic)
- Dataflow and spatial computing
- Message-passing / network-on-chip designs
- Tagged/capability architectures
- Reconfigurable computing (FPGAs as modern enablers)
- Analog and mixed-signal computing

Many of these are currently experiencing renewed interest as general-purpose scaling slows and specialization becomes economically viable.

---

## Lessons from Hardware History

1. **Periods of consolidation** are usually followed by renewed diversity when physical or economic constraints change.
2. **Specialization beats general-purpose** when the value of a workload is high enough (see: AI accelerators).
3. **FPGAs** act as a powerful time machine, allowing rapid testing of historical concepts.
4. The economics of hardware have shifted dramatically — many ideas that failed due to manufacturing cost in the past are newly viable.

We are currently in one of the most exciting periods for hardware innovation since the 1980s.

---

## Related Resources

- [Computing Timeline](./computing.md)
- [AI Timeline](./ai.md)
- [Modern Relevance](../modern-relevance/)
  - [Coprocessors](../modern-relevance/coprocessors.md)
  - [FPGA](../modern-relevance/fpga.md)
  - [Mixed-Radix](../modern-relevance/mixed-radix.md)

---