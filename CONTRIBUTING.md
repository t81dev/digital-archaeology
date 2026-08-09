# Contributing to Digital Archaeology

Thank you for your interest in contributing to **Digital Archaeology**! This project is a collaborative effort to excavate forgotten, abandoned, and overlooked ideas from computing history and evaluate them under modern technological and economic constraints.

We welcome contributions of all types:
* **New Excavations**: Deep-dives into forgotten architectures, operating systems, languages, or paradigms.
* **Pattern Analysis**: Identifying recurring engineering themes or failure modes across multiple excavations.
* **Modern Relevance Perspectives**: Exploring how modern advancements (AI, FPGAs, specialized silicon, security constraints) alter the feasibility of historic ideas.
* **Syntheses**: Conceptual essays linking diverse discoveries into actionable engineering insights.
* **Corrections & Enhancements**: Improving historical accuracy, adding primary source references, or fixing typos.

---

## Highest-Value Contribution Areas

As the repository has reached a mature, feature-complete state with 35 excavations, 15+ simulators, and fully verified synthesizable RTL cores (formally checked via SymbiYosys/z3 and mapped to Lattice iCE40 FPGAs), we encourage contributions focused on the following next-generation research frontiers:

1. **Tiny Tapeout Submission & Silicon Target Readiness**: Adapting our synthesizable soft-cores (`ternary_alu.sv`, `capability_bounds_checker.sv`, `reversible_gates.sv`, `stochastic_multiplier.sv`) for [Tiny Tapeout](https://tinytapeout.com/), establishing GDSII layouts, and preparing files for the next physical silicon shuttle.
2. **Real-Workload PPA Benchmarks**: Running systems-level benchmarks on physical FPGA boards (e.g. iCEbreaker UP5K) or logic analyzers, measuring Power, Performance, and Area (PPA) scaling curves for alternate computing paradigms against CMOS equivalents.
3. **Distributed WebRTC Co-Simulation**: Writing peer-to-peer browser-native WebRTC signal handlers to connect isolated Python simulators and co-simulation instances across multiple distributed browser clients.
4. **Additional Primary-Source Depth**: Elevating our lighter historical excavations with high-fidelity archival documents, patents, oral histories, and technical schematic data to ensure academic-grade historical precision.

---

## Code of Conduct & Contribution Philosophy

1. **Historical Accuracy First**: Ground your claims in primary sources (manuals, patents, contemporary papers, oral histories) rather than speculation. Distinguish historical facts from your own modern evaluations.
2. **Neutrality**: Avoid romanticizing lost technologies. Analyze *why* they failed (economics, ecosystem, manufacturing, tooling) with the same rigor you use to analyze their technical elegance.
3. **Actionable Insights**: Always bridge the gap between history and the present. Ask: *If we built this today, would we build it differently?*
4. **Cross-Linking**: Help build a dense, navigated web of ideas. Link your contributions to relevant excavations, patterns, timelines, and bibliographies.

---

## Standard Excavation Format

To maintain consistency and make cross-comparison easier, every new excavation *must* follow the format outlined below. A template is available in `excavations/excavation-template.md`.

```markdown
# Project Name

## Summary
Two or three paragraphs describing what it was, what made it unique, and its ultimate outcome.

---

## Historical Context
* When was it developed?
* Who was behind it?
* What specific problem or opportunity prompted its creation?

---

## Technical Overview
* **Architecture**: How did it work? What was the execution, memory, or communication model?
* **Strengths**: What technical advantages did it possess?
* **Weaknesses**: What were its primary design limitations?
* **Innovations**: What novel concepts or abstractions did it introduce?

---

## Why It Didn't Win
Identify the primary forces that prevented its mainstream adoption:
* **Economic**: Cost, manufacturing yield, business models.
* **Manufacturing**: Limitations in silicon fabrication, packaging, or materials of its era.
* **Software/Ecosystem**: Toolchains, compilers, library support, backward compatibility.
* **Timing**: Was it too early (lacking infrastructure) or too late (competing standard had locked in)?
* **Politics/Organization**: Corporate misalignment, antitrust, standard wars.

---

## Modern Relevance
Re-evaluate the technology under modern constraints:
* **Could AI change this?** (e.g., neuro-symbolic integration, automated code porting/generation, AI-specific workloads).
* **Would GPUs/TPUs help?** (e.g., dense matrix multiplication, spatial graphics acceleration).
* **Would FPGAs help?** (e.g., rapid reconfigurable prototyping, custom logic acceleration).
* **Could custom silicon help?** (e.g., cheap transistors, in-memory computing, specialized coprocessors).
* **Do shifting constraints change the math?** (e.g., power limits, memory wall, zero-trust security demands).

---

## Unearthed Artifacts
Identify specific, granular lessons and abstractions worth preserving or reviving:
* **Forgotten Algorithms**: Specific elegant procedures.
* **Lost Design Patterns**: Structural software/hardware patterns.
* **Elegant Abstractions**: Enduring conceptual models.
* **Ideas to Avoid**: Architectural anti-patterns or blind alleys.

---

## Scorecard
Every excavation should end with a comparative rating table.

| Category               | Rating | Rationale |
| ---------------------- | ------ | --------- |
| Historical Importance  | ★★★☆☆  | Brief justification |
| Technical Innovation   | ★★★★★  | Brief justification |
| Commercial Success     | ★☆☆☆☆  | Brief justification |
| Modern Potential       | ★★★★☆  | Brief justification |
| AI Synergy             | ★★★★★  | Brief justification |
| Difficulty to Recreate | ★★★☆☆  | Brief justification |

*Ratings are on a scale of 1 (Lowest) to 5 (Highest) stars.*

---

## References
Cite primary sources, including books, papers, patents, manuals, archives, and oral histories.
```

---

## Taxonomy of Discoveries

When submitting a new excavation, classify it under one or more of these conceptual categories (rather than just chronological periods):

* **Architectures**: Stack machines, dataflow, vector, spatial, cellular automata, non-von Neumann.
* **Operating Systems**: Capability-based, single-level stores, distributed resources, message-passing microkernels.
* **Programming Languages & Runtimes**: Actor model, concurrent (CSP), image-based, pure object-oriented, symbolic.
* **AI & Symbolic Computing**: Knowledge representation, logic programming, inference hardware, expert systems.
* **Hardware & Physics**: Analog, balanced ternary, reversible logic, cryogenic/superconducting, optical, wafer-scale integration, bio/molecular.
* **Mathematics & Arithmetic**: Alternative number systems, mixed-radix representations, logarithmic formats, posits.
* **Security & Memory Safety**: Object-capabilities, tagged memory, capability registers, formal verification.
* **HCI & Networking**: Bi-directional hypermedia, zoomable interfaces, distributed resource sharing protocols.

---

## Contributing to Patterns & Syntheses

* **Patterns** (`patterns/`): If you find a recurring dynamic across three or more excavations, propose it as a pattern. Draft a file explaining the pattern's characteristics, historical case studies, and modern implications.
* **Syntheses** (`synthesis/`): For multi-disciplinary themes or deep architectural trends (like the return of spatial computing or compiler-hardware co-design), write a synthesis essay comparing different technical lineages and evaluating their hybrid future.

---

## Submission Process

1. **Open an Issue**: Discuss your proposed excavation or pattern with the community first.
2. **Create a Branch**: Create a branch off `main` for your changes (e.g., `feature/excavation-mytech`).
3. **Draft the Document**: Follow the standard format and check your files for broken markdown links.
4. **Self-Review**: Run through the checklist in the template and ensure primary sources are properly referenced in the bibliography.
5. **Submit a Pull Request**: Submit your PR with a clear summary of your findings and the modern potential of the excavated tech.
