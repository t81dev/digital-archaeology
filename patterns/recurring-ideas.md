# Recurring Ideas

> Concepts and architectural patterns that repeatedly appear across decades of computing history, often in new forms or different domains.

---

## Summary

Some ideas in computing refuse to stay dead. They resurface again and again — sometimes as academic proposals, sometimes as commercial products, and sometimes as quiet features embedded in modern systems. Their persistence suggests they address fundamental problems or possess deep conceptual power that transcends specific eras of technology.

This pattern catalog identifies recurring ideas, documents their historical appearances, and explores why they endure despite earlier setbacks.

---

## Core Recurring Ideas (Updated July 2026)

### 1. Dataflow and Execution by Availability
- **Original**: Dataflow architectures (1970s–1990s), [Systolic Arrays](../excavations/systolic-arrays.md)
- **Modern forms**: TensorFlow/PyTorch computation graphs, GPU shader/tensor execution, streaming processors, reactive programming, and many AI accelerators.

### 2. Message-Passing & CSP Concurrency
- **Original**: [Transputers](../excavations/transputers.md), [Occam](../excavations/occam.md), Hoare’s Communicating Sequential Processes (CSP)
- **Modern forms**: Go channels, Erlang actors, Akka, Ray, many distributed systems, and network-on-chip designs.

### 3. Tagged / Capability Architectures
- **Original**: [Lisp Machines](../excavations/lisp-machines.md) ([tagged memory](../GLOSSARY.md)), Burroughs descriptors, [Capability Systems](../excavations/capability-systems.md), iAPX 432, [Multics](../excavations/multics.md)
- **Modern forms**: CHERI hardware capabilities, ARM Memory Tagging Extension (MTE), typed memory in managed runtimes, and object-capability models.

### 4. Alternative Number Systems & Representations
- **Original**: [Balanced Ternary](../excavations/balanced-ternary.md) (Setun), decimal machines, residue number systems
- **Modern forms**: Posits, logarithmic number systems, mixed-precision AI formats, [stochastic computing](../excavations/stochastic-computing.md), and multi-valued logic research.

### 5. Deep Language-Hardware Integration
- **Original**: [Lisp Machines](../excavations/lisp-machines.md), [Burroughs Large Systems](../excavations/burroughs-large-systems.md), Symbolics Genera (microcode + rich runtime)
- **Modern forms**: Domain-specific accelerators with tight compiler co-design, e-graph rewriting, hardware support for garbage collection, dynamic typing, and high-level operations.

### 6. Single-Level Storage / Persistent Object Models
- **Original**: Early Lisp/[Smalltalk](../excavations/smalltalk.md) environments, [Multics](../excavations/multics.md), Burroughs
- **Modern forms**: Persistent memory (Optane-style), unified memory architectures (e.g., Apple Silicon), and object-capability storage systems.

### 7. Vector / Spatial / Streaming Data Parallelism (new)
- **Original**: Cray [Vector Supercomputing](../excavations/vector-supercomputing.md), [Systolic Arrays](../excavations/systolic-arrays.md), [Connection Machine](../excavations/connection-machine.md)
- **Modern forms**: GPU tensor cores, SIMD extensions (AVX-512, SVE), spatial computing fabrics, and systolic-style matrix engines in AI hardware.

---

## Why These Ideas Recur

- They solve **fundamental problems** that general-purpose solutions only approximate.
- Advances in **manufacturing, fabrication, packaging, and cost** periodically remove previous barriers.
- New **application domains** (AI, massive parallelism, distributed/zero-trust systems, edge computing, security, energy efficiency) expose weaknesses in dominant approaches.
- They offer **elegance, leverage, composability, and correctness** that become more attractive as system complexity grows.
- Human cognition and engineering intuition favor certain abstractions — they simply “feel right.”

---

## Relationship to Other Patterns

Recurring ideas often become **[Forgotten Abstractions](forgotten-abstractions.md)** when economic or ecosystem forces temporarily suppress them. They frequently suffer from **[Economic Failures](economic-failures.md)** and **[Ecosystem Lock-In](ecosystem-lockin.md)**, only to reappear when technological or market constraints shift.

Understanding recurrence helps us distinguish transient fads from deep structural principles in computing.

---

## Modern Implications

The current environment — specialized hardware, AI-augmented design tools, extreme scale, energy constraints, and security demands — is particularly favorable for many of these long-recurring ideas:

- Hybrid neuro-symbolic systems revive symbolic and tagged architectures.
- Massive parallelism and matrix operations favor dataflow, vector, and spatial models.
- Security and formal verification needs revive capability-based designs.
- Efficiency and precision pressures encourage alternative number systems and spatial computing.

Many ideas that failed commercially in the past may now be worth revisiting — not as wholesale replacements for existing systems, but as powerful components in heterogeneous, domain-specific architectures.

---

## Related Excavations

- [Balanced Ternary](../excavations/balanced-ternary.md)
- [Burroughs Large Systems](../excavations/burroughs-large-systems.md)
- [Capability Systems](../excavations/capability-systems.md)
- [Connection Machine](../excavations/connection-machine.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Lisp Machines](../excavations/lisp-machines.md)
- [Multics](../excavations/multics.md)
- [Systolic Arrays](../excavations/systolic-arrays.md)
- [Transputers](../excavations/transputers.md)
- [Vector Supercomputing](../excavations/vector-supercomputing.md)

## Related Patterns

- [Forgotten Abstractions](../patterns/forgotten-abstractions.md)
- [Economic Failures](../patterns/economic-failures.md)
- [Ecosystem Lock-In](../patterns/ecosystem-lockin.md)

---

**Last updated**: July 26, 2026
