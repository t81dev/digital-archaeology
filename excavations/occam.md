# Occam

> A concurrent programming language designed specifically to express the parallelism and communication model of the Transputer, embodying Communicating Sequential Processes (CSP).

---

## Summary

Occam is a programming language created by David May and others at INMOS in the 1980s. It was designed hand-in-hand with the Transputer microprocessor to make massive parallelism straightforward, safe, and efficient.

Named after the philosopher William of Ockham (of "Occam's Razor"), the language emphasizes simplicity, explicit concurrency, and communication via channels. While it never achieved widespread adoption outside the Transputer ecosystem, its core ideas — particularly CSP-based message passing — have had lasting influence on modern concurrency models.

---

## Historical Context

In the early 1980s, parallel computing was a major research frontier. Traditional shared-memory approaches were complex and didn't scale well. INMOS, a British semiconductor company, developed both the Transputer hardware and Occam language as a complete solution for building scalable parallel systems.

Occam was tightly coupled to the Transputer’s hardware process scheduler and communication links. It saw use in scientific computing, embedded systems, and some commercial parallel machines, but faded along with the Transputer in the 1990s.

---

## Technical Overview

Occam is based on Tony Hoare’s **Communicating Sequential Processes (CSP)**:
- Programs are built from **processes** that run concurrently.
- Processes communicate exclusively through **synchronous channels** (no shared memory).
- Key primitives: `PAR` (parallel composition), `SEQ` (sequential), `ALT` (alternative), and channel communication (`!` and `?`).
- The language is deliberately minimal and enforces strict rules to prevent common concurrency bugs (e.g., no shared variables between processes).

The compiler and runtime mapped directly onto Transputer hardware features, such as fast context switching and link-based communication.

---

## Innovations

- **Explicit, safe concurrency** — Parallelism is part of the language syntax, not an afterthought.
- **Synchronous message passing** — Communication is simple and deterministic.
- **Composability** — Processes can be combined elegantly using `PAR`, `SEQ`, and `ALT`.
- **Formal foundation** — Strong theoretical basis in CSP, making programs more amenable to reasoning and verification.
- **Hardware-software co-design** — The language and Transputer were designed together for extreme efficiency.

---

## Why It Didn’t Win

- **Hardware dependence** — Strongly tied to the Transputer’s fate.
- **Ecosystem lock-in** — Developers overwhelmingly preferred C and Fortran with emerging libraries (e.g., MPI).
- **Learning curve** — The explicit concurrency model felt unfamiliar compared to sequential imperative languages.
- **Timing** — Arrived just as commodity microprocessors and Ethernet clusters became dominant.
- **Limited portability** — Early implementations were Transputer-centric.

---

## Modern Relevance

Occam’s ideas have had significant indirect impact:
- **Go’s goroutines and channels** — Direct spiritual successor to Occam/CSP.
- **Erlang and actor models** — Similar message-passing philosophy.
- **Modern concurrency libraries** (Rust’s channels, Akka, Ray) draw from CSP principles.
- **Formal verification and safety-critical systems** — CSP remains influential in high-assurance software.
- **Network-on-chip and many-core designs** — Hardware implementations often echo Transputer/Occam thinking.

In an era of massive parallelism, distributed systems, and multicore challenges, Occam’s clean approach to concurrency feels prescient.

---

## Lessons Learned

- Designing a language and hardware together can produce remarkable elegance and performance.
- Explicit, safe concurrency models are powerful but face steep adoption barriers against familiar imperative styles.
- Ideas that fail commercially can reshape thinking for decades (CSP → Go channels is a prime example).
- Simplicity and formal foundations matter — Occam remains a model of minimalism done right.

---

## Rating Scorecard

| Category              | Rating     | Notes |
|-----------------------|------------|-------|
| Historical Importance | ★★★★☆     | Influential in parallel computing |
| Technical Innovation  | ★★★★★     | Clean CSP implementation |
| Commercial Success    | ★☆☆☆☆     | Limited to Transputer ecosystem |
| Modern Potential      | ★★★★☆     | Strong legacy in modern languages |
| AI / Specialized HW Synergy | ★★★★☆ | Excellent for concurrent AI workloads |

---

## Related Excavations
- [Transputers](../excavations/transputers.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Capability Systems](../excavations/capability-systems.md)

## Related Patterns
- [Recurring Ideas](../patterns/recurring-ideas.md)
- [Ecosystem Lock-In](../patterns/ecosystem-lockin.md)
- [Economic Failures](../patterns/economic-failures.md)
- [Forgotten Abstractions](../patterns/forgotten-abstractions.md)

---

## References (Selected)
- May, David et al. — Occam programming manual and Transputer papers.
- Hoare, C.A.R. — *Communicating Sequential Processes* (theoretical foundation).
- INMOS Technical Manuals.
- Modern CSP-inspired work in Go, Rust, and formal methods communities.
