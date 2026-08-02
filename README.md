# Digital Archaeology

[![Research Phase: Active](https://img.shields.io/badge/Research--Phase-Active-success.svg)](#roadmap)
[![Reconstructions: 4 Python Simulators](https://img.shields.io/badge/Reconstructions-4%20Simulators-blue.svg)](#-interactive-reconstructions--simulators)
[![Completed Excavations: 28](https://img.shields.io/badge/Completed--Excavations-28-orange.svg)](#-project-pillars)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> *Excavating forgotten ideas. Recovering lost innovations. Reconstructing alternate futures.*

**Digital Archaeology** is an open-source, multi-disciplinary research initiative dedicated to the rediscovery and implementation of historically sidelined computing architectures, operating environments, programming languages, and hardware paradigms.

Many remarkable technologies did not disappear because they were technically flawed, but because economics, silicon manufacturing limitations, developer lock-in, or historical timing favored alternative paths. As modern computing faces physical and architectural ceilings—such as the Von Neumann memory wall, rising energy constraints, and the immense demands of AI—these "lost" ideas offer elegant, alternative blueprints for specialized acceleration, spatial execution, hardware-enforced security, and alternative mathematics.

Rather than treating computing history as a passive museum, we approach it as an active research discipline. We ask: **If this idea were invented today, under modern physical and economic constraints, would we build it differently?**

---

```text
                     Digital Archaeology Research Framework
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
  [EXCAVATIONS]                    [SYNTHESIS]                   [RECONSTRUCTIONS]
 28 deep dives into              Comparative and                Interactive Python
 historical paradigms.          architectural essays.           functional simulators.
        │                               │                               │
        └───────────────────────────────┼───────────────────────────────┘
                                        ▼
                                [MODERN RELEVANCE]
                             Applying historic ideas
                              to AI, FPGAs, & ASIC.
```

---

## 🏛️ Project Pillars

The project structure is organized to bridge historical research with modern execution:

### 1. [Excavations](excavations/) (Historical Deep Dives)
Comprehensive, primary-source-backed investigations of 28 landmark computing paradigms, evaluated using a standardized evaluation format and rating system.
* **Architectures**: [Analog Computing](excavations/analog-computing.md) • [Balanced Ternary](excavations/balanced-ternary.md) • [Cellular Automata](excavations/cellular-automata-hardware.md) • [Connection Machine](excavations/connection-machine.md) • [Dataflow Computing](excavations/dataflow-computing.md) • [Molecular/Biocomputing](excavations/molecular-biocomputing.md) • [Neuromorphic](excavations/neuromorphic-hardware.md) • [Optical Computing](excavations/optical-computing.md) • [Reversible Computing](excavations/reversible-computing.md) • [Stack Machines](excavations/stack-machines.md) • [Superconducting/Cryogenic](excavations/superconducting-cryogenic.md) • [Systolic Arrays](excavations/systolic-arrays.md) • [Transputers](excavations/transputers.md) • [Vector Supercomputing](excavations/vector-supercomputing.md) • [VLIW/EPIC](excavations/vliw-epic.md) • [Wafer-Scale Integration](excavations/wafer-scale-integration.md)
* **Operating Systems**: [BeOS / Haiku](excavations/beos-haiku.md) • [Burroughs Large Systems](excavations/burroughs-large-systems.md) • [Capability Systems](excavations/capability-systems.md) • [Inferno](excavations/inferno.md) • [Intel iAPX 432](excavations/intel-iapx-432.md) • [Lisp Machines](excavations/lisp-machines.md) • [Multics](excavations/multics.md) • [Plan 9](excavations/plan-9.md) • [Project Xanadu](excavations/project-xanadu.md)
* **Languages & AI**: [Occam](excavations/occam.md) • [Smalltalk](excavations/smalltalk.md) • [Symbolic AI](excavations/symbolic-ai.md)

### 2. [Patterns](patterns/) (Architectural Dynamics)
Identifying the underlying economic, technical, and ecological forces that select for or against computing paradigms.
* **[Economic Failures](patterns/economic-failures.md)** — Cost-per-bit, yield dynamics, and manufacturing scale.
* **[Ecosystem Lock-In](patterns/ecosystem-lockin.md)** — Tooling momentum, legacy APIs, and why sub-optimal software wins.
* **[Forgotten Abstractions](patterns/forgotten-abstractions.md)** — Elegant conceptual models that faded but retain significant utility.
* **[Constraint Migration](patterns/constraint-migration.md)** — How shifting physical, technological, and economic bounds resurrect old ideas.
* **[Heterogeneous Revival](patterns/heterogeneous-revival.md)** — How dead host architectures return as hardware accelerators.
* **[Recurring Ideas](patterns/recurring-ideas.md)** — The cyclicity of ideas under shifting engineering limits.

### 3. [Synthesis](synthesis/) (Comparative Architectural Distillation)
Advanced thematic essays analyzing how failed physical systems leave behind enduring conceptual abstractions that re-shape modern architectures.
* **[Architectural Distillation](synthesis/architectural-distillation.md)** — The process of preserving the logical core of failed hardware paradigms.
* **[Capability-Based Security](synthesis/capability-based-security.md)** — The modern revival of hardware-level capabilities in micro-segmentation and zero-trust computing.
* **[Compiler-Hardware Co-Design](synthesis/compiler-hardware-co-design.md)** — Why modern performance gains rely on treating compilers and custom ASICs as a single system.
* **[The Return of Spatial Computing](synthesis/return-of-spatial-computing.md)** — How dataflow, parallel grid, and neuromorphic models are taking over AI acceleration.

### 4. [Modern Relevance](modern-relevance/) (Practical Application)
Direct mapping of historical concepts to contemporary engineering challenges:
* **[AI & Hardware Bottlenecks](modern-relevance/ai.md)** — Tackling the memory wall and matrix acceleration using non-von Neumann models.
* **[Coprocessors](modern-relevance/coprocessors.md)** — Domain-specific coprocessing offloaded from general-purpose CPUs.
* **[FPGA Prototyping](modern-relevance/fpga.md)** — Reconfigurable logic as a high-fidelity sandbox for architectural experimentation.
* **[Mixed-Radix & Alternative Math](modern-relevance/mixed-radix.md)** — Evaluating ternary logic, logarithmic number systems, and posits in silicon.
* **[Symbolic Computing](modern-relevance/symbolic-computing.md)** — Hybrid neuro-symbolic models, theorem proving, and deterministic LLM guardrails.

---

## 💻 Interactive Reconstructions & Simulators

Moving from historical theory to active software prototyping, we maintain a suite of four **zero-dependency interactive Python simulators** that let you execute and study these paradigms directly.

| Simulator / Emulator | Target Historical Paradigm | Key Architectural Highlight | Entry Point |
| :--- | :--- | :--- | :--- |
| 🧮 **[Balanced Ternary Simulator](reconstructions/mixed-radix-sim/)** | [Setun Ternary Computer](excavations/balanced-ternary.md) | Sign-bit-free arithmetic, trit-level logic, and radix economy demonstrating Base-3 advantages. | `reconstructions/mixed-radix-sim/ternary_sim.py` |
| 🔄 **[Dynamic Token Dataflow Engine](reconstructions/dataflow-engine/)** | [MIT Tagged-Token Dataflow](excavations/dataflow-computing.md) | Out-of-order, asynchronous spatial execution using token-tag match scheduling. | `reconstructions/dataflow-engine/dataflow_sim.py` |
| 🛡️ **[Capability Memory Protection Emulator](reconstructions/capability-security/)** | [Burroughs Systems / CHERI](excavations/capability-systems.md) | CPU & Tagged RAM emulator simulating hardware-enforced memory bounds and secure domain gates. | `reconstructions/capability-security/capability_sim.py` |
| 🧠 **[Neuro-Symbolic Inference Solver](reconstructions/neuro-symbolic/)** | [Symbolic AI / Expert Systems](excavations/symbolic-ai.md) | Hybrid pipeline mapping probabilistic neural classifier confidences into deterministic logic. | `reconstructions/neuro-symbolic/neuro_symbolic_sim.py` |

### Quick Start: Running the Simulators
You can run all simulators locally out-of-the-box. They are written in standard Python 3 and require no third-party libraries:

```bash
# Clone the repository
git clone https://github.com/your-username/digital-archaeology.git
cd digital-archaeology

# Run the Balanced Ternary & Mixed-Radix Simulator
python3 reconstructions/mixed-radix-sim/ternary_sim.py

# Run the Dynamic Dataflow Engine
python3 reconstructions/dataflow-engine/dataflow_sim.py

# Run the Capability-Based Security Emulator
python3 reconstructions/capability-security/capability_sim.py

# Run the Neuro-Symbolic Logic Solver
python3 reconstructions/neuro-symbolic/neuro_symbolic_sim.py
```

---

## 📐 Abstraction Taxonomy

Digital Archaeology categorizes forgotten concepts not by their historical date, but by their core architectural abstractions. We utilize a structured three-part taxonomy:

```
                      ┌─────────────────────────────────┐
                      │  Abstractions Taxonomy Framework │
                      └────────────────┬────────────────┘
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌───────────────────┐        ┌───────────────────┐        ┌───────────────────┐
│     Execution     │        │ Memory Protection │        │    Concurrency    │
│  & Control Flow   │        │   & Safety Mod    │        │  & Communication  │
└────────┬──────────┘        └────────┬──────────┘        └────────┬──────────┘
         ├─ Dataflow                  ├─ Object Capabilities       ├─ CSP Channels
         ├─ Stack Evaluation          ├─ Tagged Memory             ├─ Actor Messaging
         ├─ Spatial Grids             ├─ Single-Level Store        ├─ Massively Parallel
         └─ Continuous Analog         └─ Concentric Rings          └─ Distributed 9P
```

*For definitions and details of these concepts, explore the [GLOSSARY.md](GLOSSARY.md) and our [COMPARATIVE_INDEX.md](COMPARATIVE_INDEX.md) which maps all 28 excavations across this matrix.*

---

## 🔬 Research Methodology

Every excavation follows a strict, comparative research format to ensure objectivity and technical depth.

1. **Summary**: A high-level architectural overview.
2. **Historical Context**: The origin, backers, and contemporary problem statement.
3. **Technical Overview**: Execution, memory, communication models, design strengths, weaknesses, and core innovations.
4. **Why It Didn't Win**: Rigorous breakdown of economic, manufacturing, ecosystem, and political bottlenecks.
5. **Modern Relevance**: Assessment under modern physical bounds (AI demands, custom ASICs, sub-nanosecond hardware, power-limits, FPGAs).
6. **Unearthed Artifacts**: High-fidelity abstractions, algorithms, and design patterns worth preserving or avoiding.
7. **Scorecard**: Standardized 5-star rating matrix (Historical Importance, Technical Innovation, Commercial Success, Modern Potential, AI Synergy, Difficulty to Recreate).

---

## 🗺️ Project Navigation

* **[INDEX.md](INDEX.md)** — The central directory and conceptual mapping of all files in this repository.
* **[ROADMAP.md](ROADMAP.md)** — Current project milestones, track progress, and view upcoming areas of exploration.
* **[GLOSSARY.md](GLOSSARY.md)** — Deep definitions of obscure concepts and our Abstraction Taxonomy.
* **[COMPARATIVE_INDEX.md](COMPARATIVE_INDEX.md)** — Multi-dimensional mapping of all excavations across Execution, Memory, and Concurrency models.
* **[Timelines](timelines/)** — Chronological charts charting milestones in [Computing](timelines/computing.md), [Hardware](timelines/hardware.md), and [AI](timelines/ai.md).
* **[Bibliography](bibliography/)** — Cataloged references to primary documents, [Books](bibliography/books.md), [Papers](bibliography/papers.md), and [Archives](bibliography/archives.md).

---

## 🤝 Contributing

We welcome contributions of all types—whether adding a new excavation, refining a simulator, updating historical references, or drawing new modern-relevance connections.

Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed instructions on standard excavation templates, taxonomy classifications, and the submission process.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> *"Computing history is not a graveyard of obsolete machines. It is a landscape of unrealized possibilities. Every abandoned architecture, forgotten language, and overlooked algorithm represents an alternate path that computing might have taken."* — **[MANIFESTO.md](MANIFESTO.md)**
