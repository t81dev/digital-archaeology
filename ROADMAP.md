# ROADMAP

This roadmap tracks the evolution of **Digital Archaeology** as both a growing body of excavations and a comparative research framework for recovering, analyzing, and re-evaluating abandoned computing paradigms.

---

# Phase I — Core Excavations ✅ (Complete)

## Architectures & Hardware (22)
- [x] Analog Computing, Associative Processors, Asynchronous Processors, Balanced Ternary, Cellular Automata Hardware, Connection Machine, Dataflow Computing, Explicit Data Graph Execution (EDGE), Graph Reduction Machines, The MIT J-Machine, Molecular & Biocomputing, Neuromorphic Hardware, Optical Computing, Reversible Computing, Stack Machines, Stochastic Computing, Superconducting & Cryogenic Microarchitectures, Systolic Arrays, Transputers, Vector Supercomputing, VLIW/EPIC Architectures, Wafer-Scale Integration

## Systems & Operating Environments (9)
- [x] BeOS / Haiku, Burroughs Large Systems, Capability Systems, Inferno, Intel iAPX 432, Lisp Machines, Multics, Plan 9, Project Xanadu

## Languages & AI Paradigms (4)
- [x] Linda Tuple Spaces, Occam, Smalltalk, Symbolic AI

**Total Excavations**: 35

---

# Phase II — Comparative Analysis & Synthesis ✅ (Complete)

### Cross-Excavation Studies
- [x] Execution models (stack, dataflow, vector, spatial, etc.)
- [x] Memory & protection models (capabilities, descriptors, tagging)
- [x] Concurrency & communication models
- [x] Economic & ecosystem failure patterns
- [x] Modern AI / hardware relevance mapping

### Pattern Expansion
- [x] [Economic Failures](patterns/economic-failures.md)
- [x] [Ecosystem Lock-In](patterns/ecosystem-lockin.md)
- [x] [Forgotten Abstractions](patterns/forgotten-abstractions.md)
- [x] [Recurring Ideas](patterns/recurring-ideas.md)

**Emerging Patterns**:
- [x] [Architectural Distillation](synthesis/architectural-distillation.md)
- [x] [Constraint Migration](patterns/constraint-migration.md)
- [x] [Hardware-Software Co-Evolution](synthesis/compiler-hardware-co-design.md)
- [x] [Heterogeneous Revival](patterns/heterogeneous-revival.md)

### Synthesis Documents
- [x] [architectural-distillation.md](synthesis/architectural-distillation.md)
- [x] [return-of-spatial-computing.md](synthesis/return-of-spatial-computing.md)
- [x] [capability-based-security.md](synthesis/capability-based-security.md)
- [x] [compiler-hardware-co-design.md](synthesis/compiler-hardware-co-design.md)

---

# Phase III — Modern Reconstruction & Prototyping ✅ (Complete)

We have transitioned from theoretical comparisons to dynamic execution models, implementing fully-functional, interactive software emulators and simulation engines for key historical architectures.

### Executable Reconstructions & Simulators
- [x] [Balanced Ternary & Mixed-Radix Simulator](reconstructions/mixed-radix-sim/): Complete multi-trit arithmetic logic, logic gate suite, and decimal-ternary conversions.
- [x] [Dynamic Tagged-Token Dataflow Engine](reconstructions/dataflow-engine/): Out-of-order dataflow processor simulator with dynamic token-tag matching and parallel execution pipeline.
- [x] [Capability-Based Memory Protection Emulator](reconstructions/capability-security/): Register-level CPU and Tagged RAM emulator implementing unforgeable capability registers, automatic bounds checking, and cross-domain transitions.
- [x] [Neuro-Symbolic Logic Solver](reconstructions/neuro-symbolic/): Hybrid AI pipeline combining statistical neural classification outputs with forward-chaining symbolic logic reasoning.

**Reconstruction Index**: [reconstructions/README.md](reconstructions/README.md)

---

# Phase IV — Research Infrastructure & Dissemination ✅ (Complete)

- [x] [Enhanced bibliography and timelines](timelines/): Categorized reference timelines for [computing history](timelines/computing.md), [hardware milestones](timelines/hardware.md), and [AI development](timelines/ai.md), backed by a comprehensive [bibliography of primary and secondary sources](bibliography/).
- [x] [Glossary and abstraction taxonomy](GLOSSARY.md): Defined a clear terminology base for 21 historically rich concepts and structured them into a 3-part taxonomy (Execution, Memory, Concurrency).
- [x] [Comparative indexes (by execution, memory, and concurrency models)](COMPARATIVE_INDEX.md): Constructed dynamic matrices grouping all 35 excavations across different core technical archetypes.
- [x] [Static site / better navigation (future)](INDEX.md): Enhanced repo-wide index and cross-linking as a foundation for future static site generation.
- [x] [Public essays and "idea revival" case studies](synthesis/): Published synthesis essays including [Architectural Distillation](synthesis/architectural-distillation.md), [The Return of Spatial Computing](synthesis/return-of-spatial-computing.md), [Capability-Based Security](synthesis/capability-based-security.md), and [Compiler-Hardware Co-Design](synthesis/compiler-hardware-co-design.md).

---

# Phase V — Interactive Dissemination & Executable Artifact Expansion ✅ (Complete)

To scale the research initiative and expand from descriptive analysis into active engineering leverage, Phase V focuses on three core pillars: interactive discoverability, expanding our executable simulator footprint, and establishing developer engagement pipelines.

### 1. Interactive Knowledge Graphs & Discoverability
- [x] **Interactive Visual Taxonomy and Search**: Shift from a static `INDEX.md` and `GLOSSARY.md` to an interactive, client-side visual web page (`explorer.html`) using D3.js and Tailwind CSS mapping all 35 excavations across execution, safety, and concurrency models with custom detail drawers and real-time filtering.
- [x] **Static Site Generation & Docs Site**: Establish an automated static site build pipeline using MkDocs with the Material theme (`mkdocs.yml` configured with strict compiling) to publish the complete comparative knowledge base under a clean, searchable user interface.

### 2. Executable Reconstruction Footprint Expansion
- [x] **Expansion of Simulators to WebAssembly**: Compile or wrap existing Python-based emulators into interactive web applications so readers can execute alternative arithmetic, token-matching, and capability logic directly inside the documentation browser.
- [x] **Next-Generation Simulators**: Develop zero-dependency simulators/reconstructions for additional critical, underexplored areas of the 3-part taxonomy:
  - [x] **[CSP Messaging Engine](reconstructions/csp-messaging/)**: Visualizing occam-style synchronized channel execution and structural deadlock avoidance.
  - [x] **[Continuous Analog / Optical Wave Accelerator](reconstructions/analog-optical/)**: A functional simulator modeling matrix-vector multiplication via optical interference or continuous differential integration.
  - [x] **[Stochastic Computing Simulator](reconstructions/stochastic-computing/)**: An interactive probabilistic execution engine implementing unipolar/bipolar logic gate arithmetic, saturating FSM-based activations, and LFSR random generation.

### 3. Developer Onboarding, Tooling, & Community Integration
- [x] **Automated Excavation Checklists & Templates**: Improve the standardization of contributions with automated pull request action checks that validate markdown link integrity, scorecard range compliance, and GLOSSARY referencing.
- [x] **AI-Assisted Knowledge Ingestion**: Provide an API/schema (JSON/JSON-LD) format of the index and comparative matrices, allowing LLM-based autonomous agents to ingest, reference, and evaluate these historical architectural patterns.
- [x] **Academic & Hardware Partnerships**: Connect historical architectures (e.g., CHERI, Neuromorphic, Spatial) to active academic research programs, zero-trust security initiatives, and modern open-source FPGA toolchains (documented in `modern-relevance/partnerships.md`).

---

# Phase VI — Synthesizable Hardware, Co-Simulation Fabrics, & WebAssembly Playgrounds ✅ (Complete)

To transition our research from functional emulation into the physical silicon pipeline and expand the accessibility of alternative paradigms, Phase VI has successfully bridged interactive software simulations with hardware-synthesis blueprints, co-simulation architectures, and browser-native playgrounds.

### 1. Synthesizable IP Core Blueprints (HDL Prototyping)
- [x] **Synthesizable Soft-Cores**: Developed synthesizable open-source RTL cores in SystemVerilog for key simulator subsystems: a multi-trit Balanced Ternary ALU (`reconstructions/synthesizable-hardware/ternary_alu.sv`) and a hardware Tagged RAM capability bounds-checker (`reconstructions/synthesizable-hardware/capability_bounds_checker.sv`).
- [x] **Open-Silicon Target Readiness**: Packaged these soft-cores as portable IP blocks compatible with academic Chipyard/FPGA workflows and targetable for low-cost Google Tiny Tapeout ASIC fabrication, verified with pytest-compatible behavioral models (`reconstructions/synthesizable-hardware/test_synthesizable.py`).

### 2. Multi-Architecture Co-Simulation & Interoperability Fabric
- [x] **The Sandbox Orchestrator**: Built a unified simulation harness (`reconstructions/co-simulation/orchestrator.py`) that runs different reconstructed models in a co-simulation environment and exchanges messages.
- [x] **Cross-Paradigm Integration**: Enabled high-level flows, routing continuous classification outputs from the *Neuro-Symbolic Solver* to trigger concurrent actor-based *CSP channels* and initiate *Tagged-Token Dataflow* graphs, fully tested via `reconstructions/co-simulation/test_orchestrator.py`.

### 3. Native WebAssembly & Pyodide Interactive Playgrounds
- [x] **In-Browser Execution**: Embedded our Python reconstructions directly into a client-side single-page app (`playground.html`) using Pyodide to compile/interpret Python directly in the user's browser.
- [x] **Interactive Visual UIs**: Built lightweight browser-native consoles and dashboards, allowing readers to write code, inject faults, trigger capability bounds violations, and inspect register states in real-time without terminal setups.

### 4. Academic Lab Manual & Pedagogical Sandboxes
- [x] **Curated Lab Modules**: Authored a series of interactive pedagogical lab sheets (`reconstructions/LAB_MANUAL.md`) designed for university systems-architecture curricula.
- [x] **Hands-on Clean-Slate Challenges**: Included problems such as "Designing a Ternary Half-Adder," "Custom Mathematical Pipelined Dataflow Graph," "Implementing Secure Domain Transitions," and "Deadlock-Avoiding Message Broker" complete with model solutions.

---

# Phase VII — Relational Density, Architectural Integrity & Taxonomic Synthesis ✅ (Complete)

To elevate the repository from a decoupled database into a highly cohesive, non-linear knowledge fabric, Phase VII focuses on increasing explanatory density across all architectural and taxonomic layers.

### 1. Eliminating Topological Symmetries & Gaps
- [x] **Weaving Isolated Excavations**: Connected previously isolated excavations—specifically `associative-processors.md`, `intel-iapx-432.md`, and `graph-reduction-machines.md`—to relevant synthesis essays and patterns, fully integrating them into the comparative taxonomy.
- [x] **Taxonomic Cohesion**: Established outbound relational links from all synthesis essays (`capability-based-security.md`, `return-of-spatial-computing.md`, `compiler-hardware-co-design.md`, and `architectural-distillation.md`) to back their conceptual frameworks with concrete historical excavations.

### 2. Graph and Network Optimization
- [x] **Metric Analysis and Density Doubling**: Developed custom network analysis tools (`density_analyzer.py`) to systematically map the repository's topological layout, successfully doubling active cross-reference connections from 96 to 192 and achieving a high network density metric of 0.1171 with zero dead-ends or isolated nodes.
- [x] **Dynamic Knowledge Graph Synthesis**: Recompiled the machine-readable database `knowledge_graph.json` via automated scripts to dynamically update the interactive D3 force-directed visual explorer (`explorer.html`).

---

# Phase VIII — Semantic Navigation & Browser-Native Hardware-in-the-Loop Co-Simulation ✅ (Complete)

To transition our comparative research network into a dynamically queryable and physically interactive environment, Phase VIII introduces advanced browser-native semantic routing, interactive hardware panels, and cycle-accurate co-simulation visualization.

### 1. Multi-Dimensional Semantic Query Engine
- [x] **Smart Query Console**: Implemented an advanced client-side semantic query and constraint parser inside `explorer.html`, allowing readers to execute queries like `synergy:high potential:high ternary` or `type:excavation stars:>=4`.
- [x] **Relational Highlighting**: Highlights shortest connection paths and dims non-matching clusters on the D3.js force-directed knowledge graph based on query constraints, keeping navigational results highly relational.

### 2. Browser-Native Hardware-in-the-Loop Sandbox
- [x] **Interactive Peripherals Board**: Integrated physical sliders and fault-injection toggle switches in `playground.html` representing continuous sensor feeds, active-low reset lines, and bounds protection tags.
- [x] **Live Digital Logic Analyzer**: Engineered a canvas-based waveform viewer displaying synchronized transitions of `CLK`, `SEN_TRIG`, `LOGIC_DEC`, `CSP_RDV`, `DF_OP`, `EDGE_WR`, and `HW_EXC` logic signals.
- [x] **Inter-Paradigm Fault Injection**: Toggles like `FORCE_EXCEPTION` dynamically override soft-core bounds rules to manually trigger hardware capability violations or ternary carry overflows live in the Wasm sandbox.

---

# Long-Term Vision

Digital Archaeology seeks to become the premier comparative reference for abandoned and underexplored computing paradigms.

Rather than asking only *"What happened?"*, the project systematically asks:

- What powerful abstraction was introduced?
- Why did it disappear?
- Which forces selected against it?
- Which parts survived in disguise?
- Which constraints have changed?
- Should we build it differently today?

The goal is to help engineers, researchers, and future AI systems recover valuable ideas from computing history and evaluate them under modern technological and economic constraints.

---

**Last updated**: August 2, 2026
