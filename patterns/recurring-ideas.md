# Recurring Ideas

> Concepts and architectural patterns that repeatedly appear across decades of computing history, often in new forms or different domains.

---

## Summary

Some ideas in computing refuse to stay dead. They resurface again and again — sometimes as academic proposals, sometimes as commercial products, and sometimes as quiet features embedded in modern systems. Their persistence suggests they address fundamental problems or possess deep conceptual power that transcends specific eras of technology.

This pattern catalog identifies recurring ideas, documents their historical appearances, and explores why they endure despite earlier setbacks.

---

## Core Recurring Ideas

### 1. Dataflow and Execution by Availability
- **Original**: Dataflow architectures (1970s–1990s)
- **Modern forms**: TensorFlow/PyTorch computation graphs, GPU shader execution, streaming processors, reactive programming, and many AI accelerators.

### 2. Message-Passing & CSP Concurrency
- **Original**: Transputers, occam, Hoare’s Communicating Sequential Processes (CSP)
- **Modern forms**: Go channels, Erlang actors, Akka, Ray, many distributed systems, and network-on-chip designs.

### 3. Tagged / Capability Architectures
- **Original**: Lisp Machines (tagged memory), capability-based systems (KeyKOS, HYDRA, CAP)
- **Modern forms**: CHERI hardware capabilities, capability security in OS research (seL4 and others), typed memory in managed runtimes, and object-capability models.
- *See [Capability Systems](../excavations/capability-systems.md)*

### 4. Alternative Number Systems
- **Original**: Balanced ternary (Setun), decimal machines, residue number systems
- **Modern forms**: Posits, logarithmic number systems, mixed-precision AI formats, stochastic computing, and multi-valued logic research.
- *See [Balanced Ternary](../excavations/balanced-ternary.md)*

### 5. Deep Language-Hardware Integration
- **Original**: Lisp Machines, Symbolics Genera (microcode + rich runtime)
- **Modern forms**: Domain-specific accelerators with tight compiler co-design, e-graph rewriting, hardware support for garbage collection, dynamic typing, and high-level operations.

### 6. Single-Level Storage
- **Original**: Early Lisp/Smalltalk environments, Multics
- **Modern forms**: Persistent memory (Optane), unified memory architectures (e.g., Apple Silicon), and object-capability storage systems.

---

## Why These Ideas Recur

- They solve **fundamental problems** that general-purpose solutions only approximate.
- Advances in **manufacturing, fabrication, and cost** periodically remove previous barriers.
- New **application domains** (AI, massive parallelism, distributed/zero-trust systems, edge computing, security) expose weaknesses in dominant approaches.
- They offer **elegance, leverage, and composability** that become more attractive as system complexity grows.
- Human cognition and engineering intuition favor certain abstractions — they simply “feel right.”

---

## Relationship to Other Patterns

Recurring ideas often become **Forgotten Abstractions** when economic or ecosystem forces temporarily suppress them. They frequently suffer from **Economic Failures** and **Ecosystem Lock-In**, only to reappear when technological or market constraints shift.

Understanding recurrence helps us distinguish transient fads from deep structural principles in computing.

---

## Modern Implications

The current environment — specialized hardware, AI-augmented design tools, extreme scale, energy constraints, and security demands — is particularly favorable for many of these long-recurring ideas:
- Hybrid neuro-symbolic systems revive symbolic and tagged architectures.
- Massive parallelism favors dataflow and message-passing models.
- Security and formal verification needs revive capability-based designs.
- Efficiency and precision pressures encourage alternative number systems.

Many ideas that failed commercially in the past may now be worth revisiting — not as wholesale replacements for existing systems, but as powerful components in heterogeneous, domain-specific architectures.

---

## Related Excavations
- [Balanced Ternary](../excavations/balanced-ternary.md)
- [Capability Systems](../excavations/capability-systems.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Lisp Machines](../excavations/lisp-machines.md)
- [Transputers](../excavations/transputers.md)

## Related Patterns
- [Forgotten Abstractions](./forgotten-abstractions.md)
- [Economic Failures](./economic-failures.md)
- [Ecosystem Lock-In](./ecosystem-lockin.md)
