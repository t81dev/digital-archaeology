# Recurring Ideas

> *Concepts and architectural patterns that repeatedly appear across decades of computing history, often in new forms or different domains.*

---

## Summary

Some ideas in computing refuse to stay dead. They resurface again and again — sometimes as academic proposals, sometimes as commercial products, and sometimes as quiet features inside modern systems. Their persistence suggests they address fundamental problems or possess deep conceptual power.

This pattern catalog identifies ideas that keep re-emerging and explores why they endure.

---

## Core Recurring Ideas

### 1. Dataflow and Execution by Availability
- Original: Dataflow architectures (1970s–1990s)
- Modern forms: TensorFlow/PyTorch graphs, GPU shader execution, streaming processors, reactive programming, many AI accelerators

### 2. Message-Passing & CSP Concurrency
- Original: Transputers, occam, Hoare’s CSP
- Modern forms: Go channels, Erlang actors, Akka, Ray, many distributed systems, network-on-chip designs

### 3. Tagged / Capability Architectures
- Original: Lisp Machines, capability-based systems (KeyKOS, CHERI)
- Modern forms: Tagged memory in some secure processors, capability security in modern OS research, typed memory in managed runtimes

### 4. Alternative Number Systems
- Original: Balanced ternary (Setun), decimal machines, residue numbers
- Modern forms: Posits, logarithmic number systems, mixed-precision AI formats, stochastic computing, multi-valued logic research

### 5. Deep Language-Hardware Integration
- Original: Lisp Machines, Symbolics Genera
- Modern forms: Domain-specific accelerators with tight compiler co-design, e-graph rewriting in modern compilers, hardware support for garbage collection and dynamic typing

### 6. Single-Level Storage
- Original: Early Lisp and Smalltalk environments, Multics
- Modern forms: Persistent memory (Optane), unified memory architectures (Apple Silicon), object-capability storage systems

---

## Why These Ideas Recur

- They solve **fundamental problems** that general-purpose solutions only approximate.
- Advances in **manufacturing and cost** periodically remove previous barriers.
- New **application domains** (AI, distributed systems, edge computing, security) expose weaknesses in dominant approaches.
- They offer **elegance and leverage** that become more attractive as system complexity grows.
- Human cognition favors certain abstractions — they feel “right” even after being sidelined.

---

## Relationship to Other Patterns

Recurring ideas often become **Forgotten Abstractions** when economic or ecosystem forces temporarily suppress them. They frequently suffer from **Economic Failures** and **Ecosystem Lock-In**, only to reappear when constraints shift.

Understanding recurrence helps distinguish transient fads from deep structural principles.

---

## Modern Implications

The current environment (specialized hardware, AI-driven design tools, extreme scale, and energy constraints) is particularly favorable for many long-recurring ideas:

- Hybrid neuro-symbolic systems revive symbolic computing concepts.
- Massive parallelism favors dataflow and message-passing models.
- Security demands revive capability-based designs.
- Efficiency pressures encourage alternative number systems.

Many ideas that failed in the past may now be worth revisiting — not as complete replacements, but as powerful components in heterogeneous systems.

---

## Related Excavations
- [Balanced Ternary](../excavations/balanced-ternary.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Lisp Machines](../excavations/lisp-machines.md)
- [Transputers](../excavations/transputers.md)

## Related Patterns
- [Forgotten Abstractions](./forgotten-abstractions.md)
- [Economic Failures](./economic-failures.md)
- [Ecosystem Lock-In](./ecosystem-lockin.md)
