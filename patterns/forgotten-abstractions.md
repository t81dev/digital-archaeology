# Forgotten Abstractions

> Powerful ideas, mental models, and architectural concepts that were once central to computing but have faded from mainstream practice, even though they still hold deep value.

---

## Summary

Throughout computing history, certain abstractions, programming models, and architectural concepts achieved remarkable elegance and power but were later sidelined by simpler, more practical, or more commercially successful alternatives. These “forgotten abstractions” often represent elegant solutions to problems we still grapple with today.

Digital Archaeology seeks not only to document these ideas but to evaluate whether modern technology (specialized hardware, AI tools, abundant resources, energy/security constraints) makes them newly viable.

---

## Common Characteristics

Forgotten abstractions typically share these traits:
- They offered superior elegance, safety, expressiveness, composability, or correctness.
- They required more sophisticated implementation or a significant shift in thinking.
- They were overtaken by “good enough” alternatives that scaled faster or fit existing ecosystems better.
- They continue to reappear in new forms or niche domains.

---

## Notable Examples (Updated)

### From This Repository

* **[Balanced Ternary](../excavations/balanced-ternary.md)** — A more symmetric and mathematically elegant number system than binary.
* **[Burroughs Large Systems](../excavations/burroughs-large-systems.md)** *(new)* — Hardware-supported block structure, descriptors, and high-level language integration.
* **[Dataflow Computing](../excavations/dataflow-computing.md)** — Execution driven by data availability rather than a program counter.
* **[Lisp Machines](../excavations/lisp-machines.md)** — Tagged architectures with hardware support for dynamic typing, garbage collection, and symbolic computation.
* **[Transputers](../excavations/transputers.md) & [Occam](../excavations/occam.md)** — Communicating Sequential Processes (CSP) and lightweight message-passing concurrency.
* **[Capability Systems](../excavations/capability-systems.md)** — Fine-grained, unforgeable rights instead of ACLs or ambient permissions.
* **Vector Chaining & Systolic Dataflow** *(new)* — Rhythmic, streaming spatial computation models.
* **iAPX 432 / [Multics](../excavations/multics.md) abstractions** *(new)* — Strong object-oriented and protection models in hardware/OS.
* **9P/Styx Dynamic Namespaces & Union Mounts** *(new)* — Completely transparent, network-independent resource sharing via stateful, simple file messages, resolving search lookups with fallthrough directory bindings.
* **Single-Level Store (SLS)** *(new)* — Erasing the logical and physical boundary between volatile register heap memory and persistent filesystem storage (e.g., Multics, KeyKOS).
* **Unforgeable Object Capabilities** *(new)* — Integrating designation and authority into unforgeable hardware-checked keys (e.g., KeyKOS, iAPX 432).
* **Carry-Free Modular Arithmetic** *(new)* — Decomposing wide mathematical calculations into mutually independent modular channels to bypass carry-propagation bottlenecks (e.g., RNS).
* **Log-domain Cost Inversion** *(new)* — Trading representation formats to simplify high-order arithmetic operations like multiplication and division into fixed-point additions (e.g., LNS).
* **Non-moving Fluidic Switching** *(new)* — Relying on boundary fluid attachment (Coanda effect) and momentum-driven jet amplification to perform logic operations without moving parts (e.g., Fluidic logic).
* **Two-way Logical Unification & Backtracking** *(new)* — Computing via bidirectional pattern matching and chronological state unbinding over choice points (e.g., Prolog, Warren Abstract Machine).

### Other Classic Cases
* Persistent / single-level object stores (vs. filesystems + databases)
* Advanced live coding and incremental development environments
* Pure functional models taken to hardware
* Hardware-assisted generational garbage collection

---

## Why They Were Forgotten

* **Implementation complexity** on the hardware and software of their era.
* **Performance trade-offs** on then-current technology (especially memory and interconnect limitations).
* **Education and developer inertia** — simpler mental models won out in education and hiring.
* **Economic and ecosystem pressure** — see [Economic Failures](../patterns/economic-failures.md) and [Ecosystem Lock-In](../patterns/ecosystem-lockin.md).
* **Lack of immediate killer applications** at the time of their introduction.

---

## Modern Relevance (Strengthened)

Many forgotten abstractions are finding new life because the constraints have shifted:

* **Hardware abundance & specialization** — We can now afford richer abstractions in silicon or domain-specific accelerators.
* **AI-assisted tools** — Can help manage complexity (code generation, verification, optimization) that was previously prohibitive.
* **Safety and correctness demands** — As systems grow more complex and critical, abstractions that reduce errors (capabilities, [tagged memory](../GLOSSARY.md), dataflow) become highly valuable.
* **New domains** — Distributed systems, multi-agent AI, scientific computing, edge devices, and zero-trust environments often align well with these older ideas.
* **Energy & Memory Wall** — Abstractions that minimize data movement or improve locality (systolic, vector chaining, dataflow) are newly attractive.

---

## Lessons Learned

1. “Forgotten” does not mean “inferior.” Many abstractions were simply ahead of their time or mismatched to contemporary constraints.
2. The best abstractions often feel more complex initially but deliver massive long-term leverage, clarity, and safety.
3. Hardware and tool evolution periodically makes old abstractions newly practical (e.g., [tagged memory](../GLOSSARY.md), fine-grained capabilities, and spatial dataflow are far more feasible today).
4. Studying forgotten abstractions expands our design vocabulary and helps us avoid poorly reinventing old solutions under new names.
5. The most powerful future systems will likely be **hybrids** — combining dominant ecosystems with carefully chosen forgotten abstractions as specialized components.

The goal is not nostalgia, but **technological optionality** — keeping powerful ideas alive so they can be reconsidered when conditions change.

---

## Related Patterns

- [Recurring Ideas](../patterns/recurring-ideas.md)
- [Economic Failures](../patterns/economic-failures.md)
- [Ecosystem Lock-In](../patterns/ecosystem-lockin.md)

## Related Excavations

- [Balanced Ternary](../excavations/balanced-ternary.md)
- [Burroughs Large Systems](../excavations/burroughs-large-systems.md)
- [Capability Systems](../excavations/capability-systems.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Intel iAPX 432](../excavations/intel-iapx-432.md)
- [Lisp Machines](../excavations/lisp-machines.md)
- [Multics](../excavations/multics.md)
- [Systolic Arrays](../excavations/systolic-arrays.md)
- [Transputers](../excavations/transputers.md)
- [Vector Supercomputing](../excavations/vector-supercomputing.md)
- [Plan 9](../excavations/plan-9.md)
- [Inferno](../excavations/inferno.md)
- [Residue Number System](../excavations/residue-number-system.md)
- [Logarithmic Number System](../excavations/logarithmic-number-system.md)
- [Fluidic Logic Systems](../excavations/fluidic-logic-systems.md)
- [KeyKOS and the Nanokernel Capability Lineage](../excavations/keykos-nanokernel-capabilities.md)
- [Prolog / WAM / FGCS Hardware](../excavations/prolog-wam-fgcs-hardware.md)

---

**Last updated**: August 2, 2026
