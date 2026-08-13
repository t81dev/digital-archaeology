# Patterns

> Recurring themes, dynamics, and forces discovered across multiple excavations.

While individual excavations focus on specific technologies, the **Patterns** directory identifies deeper, cross-cutting insights that explain why certain ideas succeeded or failed — and which may still hold value today.

These patterns help transform isolated historical case studies into a coherent framework for understanding technological evolution and rediscovery.

---

## Purpose

- Extract reusable lessons from computing history.
- Identify why technically strong ideas were abandoned.
- Highlight dynamics that have changed under modern conditions (AI, specialized hardware, energy constraints, security).
- Guide the evaluation and design of future architectures.

---

## Core Patterns (Updated August 2026)

- **[Economic Failures](economic-failures.md)** — Technically sound ideas defeated by manufacturing economics, scale, or timing.
- **[Ecosystem Lock-In](ecosystem-lockin.md)** — Self-reinforcing cycles of compatibility, tools, skills, and investment.
- **[Forgotten Abstractions](forgotten-abstractions.md)** — Elegant concepts and mental models that faded but retain power.
- **[Recurring Ideas](recurring-ideas.md)** — Architectural patterns that repeatedly re-emerge under new physical constraints.

---

## Emerging & Synthesis Patterns

- **[Constraint Migration](constraint-migration.md)** — How shifting technological, physical, and economic bottlenecks turn previously impractical ideas into optimal modern solutions.
- **[Heterogeneous Revival](heterogeneous-revival.md)** — How historically sidelined architectures return as specialized coprocessors or instruction set extensions inside hybrid general-purpose systems.
- **[Interface / Conversion Tax](interface-conversion-tax.md)** — The performance, resource, or security penalty paid when translating alternative abstractions to interface with mainstream systems.
- **[Abstract Machine Persistence](abstract-machine-persistence.md)** — Decoupling execution models into software-defined virtual machines to survive on commodity hardware.
- **[Operator-Cost Inversion](operator-cost-inversion.md)** — Changing underlying representations to invert relative mathematical operator latencies and silicon costs.
- **[Explicit Authority Substrate](explicit-authority-substrate.md)** — Replacing ambient permissions with unforgeable, fine-grained object-capabilities.

---

## Key Insights from Recent Excavations

- **Spatial & Data-Parallel Thinking** ([Systolic Arrays](../excavations/systolic-arrays.md), [Vector Supercomputing](../excavations/vector-supercomputing.md), [Connection Machine](../excavations/connection-machine.md)) continues to recur in AI accelerators. See [Heterogeneous Revival](heterogeneous-revival.md).
- **High-Level Hardware Integration** (Burroughs, [Lisp Machines](../excavations/lisp-machines.md), iAPX 432) shows the tension between safety/abstraction and raw performance.
- **Capability & Protection Models** (Burroughs descriptors, [Multics](../excavations/multics.md), [Capability Systems](../excavations/capability-systems.md)) remain highly relevant to modern security needs. See [Constraint Migration](constraint-migration.md).
- Many failures were **not technical** but economic/ecosystem-driven, reinforcing our core patterns of [Economic Failures](economic-failures.md) and [Ecosystem Lock-In](ecosystem-lockin.md).

---

## Usage & Contribution

Link generously from excavations. These documents are **living** — update them as new excavations add evidence. See [CONTRIBUTING.md](../CONTRIBUTING.md) for details on adding or editing patterns.

---

**This directory is the intellectual core of the project, moving beyond isolated histories toward a deeper theory of technological evolution and rediscovery.**
