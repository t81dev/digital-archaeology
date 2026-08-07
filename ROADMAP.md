# ROADMAP

This roadmap tracks the evolution of **Digital Archaeology** as both a growing body of excavations and a comparative research framework for recovering, analyzing, and re-evaluating abandoned computing paradigms under modern physical, economic, and architectural constraints.

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

Transitioned from theoretical comparisons to dynamic execution models, implementing fully-functional, interactive software emulators and simulation engines for key historical architectures.

### Executable Reconstructions & Simulators
- [x] [Balanced Ternary & Mixed-Radix Simulator](reconstructions/mixed-radix-sim/): Complete multi-trit arithmetic logic, logic gate suite, and decimal-ternary conversions.
- [x] [Dynamic Tagged-Token Dataflow Engine](reconstructions/dataflow-engine/): Out-of-order dataflow processor simulator with dynamic token-tag matching and parallel execution pipeline.
- [x] [Capability-Based Memory Protection Emulator](reconstructions/capability-security/): Register-level CPU and Tagged RAM emulator implementing unforgeable capability registers, automatic bounds checking, and cross-domain transitions.
- [x] [Neuro-Symbolic Logic Solver](reconstructions/neuro-symbolic/): Hybrid AI pipeline combining statistical neural classification outputs with forward-chaining symbolic logic reasoning.

**Reconstruction Index**: [reconstructions/README.md](reconstructions/README.md)

---

# Phase IV — Research Infrastructure & Dissemination ✅ (Complete)

- [x] [Enhanced bibliography and timelines](timelines/): Categorized reference timelines for [computing history](timelines/computing.md), [hardware milestones](timelines/hardware.md), and [AI development](timelines/ai.md), backed by a comprehensive [bibliography of primary and secondary sources](bibliography/).
- [x] [Glossary and abstraction taxonomy](GLOSSARY.md): Defined a clear terminology base for historically rich concepts and structured them into a 3-part taxonomy (Execution, Memory, Concurrency).
- [x] [Comparative indexes](COMPARATIVE_INDEX.md): Constructed dynamic matrices grouping all 35 excavations across different core technical archetypes.
- [x] [Static site / better navigation](INDEX.md): Enhanced repo-wide index and cross-linking as a foundation for static site generation.
- [x] [Public essays and "idea revival" case studies](synthesis/): Published synthesis essays including [Architectural Distillation](synthesis/architectural-distillation.md), [The Return of Spatial Computing](synthesis/return-of-spatial-computing.md), [Capability-Based Security](synthesis/capability-based-security.md), and [Compiler-Hardware Co-Design](synthesis/compiler-hardware-co-design.md).

---

# Phase V — Interactive Dissemination & Executable Artifact Expansion ✅ (Complete)

To scale the research initiative and expand from descriptive analysis into active engineering leverage, Phase V focuses on three core pillars: interactive discoverability, expanding our executable simulator footprint, and establishing developer engagement pipelines.

### 1. Interactive Knowledge Graphs & Discoverability
- [x] **Interactive Visual Taxonomy and Search**: Created a client-side visual web page (`explorer.html`) using D3.js and Tailwind CSS mapping all excavations across execution, safety, and concurrency models with custom detail drawers and real-time filtering.
- [x] **Static Site Generation & Docs Site**: Established an automated static site build pipeline using MkDocs with the Material theme (`mkdocs.yml` configured with strict compiling) to publish the complete comparative knowledge base.

### 2. Executable Reconstruction Footprint Expansion
- [x] **Expansion of Simulators to WebAssembly**: Enabled Python-based emulators to run interactively inside web browsers via Pyodide.
- [x] **Next-Generation Simulators**: Developed zero-dependency simulators/reconstructions for additional critical, underexplored areas of the 3-part taxonomy:
  - [x] **[CSP Messaging Engine](reconstructions/csp-messaging/)**: Visualizing occam-style synchronized channel execution and structural deadlock avoidance.
  - [x] **[Continuous Analog / Optical Wave Accelerator](reconstructions/analog-optical/)**: A functional simulator modeling matrix-vector multiplication via optical interference or continuous differential integration.
  - [x] **[Stochastic Computing Simulator](reconstructions/stochastic-computing/)**: An interactive probabilistic execution engine implementing unipolar/bipolar logic gate arithmetic, saturating FSM-based activations, and LFSR random generation.

### 3. Developer Onboarding, Tooling, & Community Integration
- [x] **Automated Excavation Checklists & Templates**: Standardized contributions with automated PR checks that validate markdown link integrity, scorecard range compliance, and GLOSSARY referencing.
- [x] **AI-Assisted Knowledge Ingestion**: Provided an API/schema (`knowledge_graph.json`) format of the index and comparative matrices, allowing LLM-based autonomous agents to ingest, reference, and evaluate these historical architectural patterns.
- [x] **Academic & Hardware Partnerships**: Connected historical architectures to active academic research programs, zero-trust security initiatives, and modern open-source FPGA toolchains (documented in [Partnerships](modern-relevance/partnerships.md)).

---

# Phase VI — Synthesizable Hardware, Co-Simulation Fabrics, & WebAssembly Playgrounds ✅ (Complete)

To transition research from functional emulation into the physical silicon pipeline and expand the accessibility of alternative paradigms, Phase VI successfully bridged interactive software simulations with hardware-synthesis blueprints, co-simulation architectures, and browser-native playgrounds.

### 1. Synthesizable IP Core Blueprints (HDL Prototyping)
- [x] **Synthesizable Soft-Cores**: Developed synthesizable open-source RTL cores in SystemVerilog for key simulator subsystems: a multi-trit Balanced Ternary ALU (`reconstructions/synthesizable-hardware/ternary_alu.sv`) and a hardware Tagged RAM capability bounds-checker (`reconstructions/synthesizable-hardware/capability_bounds_checker.sv`).
- [x] **Open-Silicon Target Readiness**: Packaged these soft-cores as portable IP blocks compatible with academic Chipyard/FPGA workflows and targetable for low-cost Google Tiny Tapeout ASIC fabrication, verified with pytest-compatible behavioral models (`reconstructions/synthesizable-hardware/test_synthesizable.py`).

### 2. Multi-Architecture Co-Simulation & Interoperability Fabric
- [x] **The Sandbox Orchestrator**: Built a unified simulation harness (`reconstructions/co-simulation/orchestrator.py`) that runs different reconstructed models in a co-simulation environment and exchanges messages.
- [x] **Cross-Paradigm Integration**: Enabled high-level flows, routing continuous classification outputs from the *Neuro-Symbolic Solver* to trigger concurrent actor-based *CSP channels* and initiate *Tagged-Token Dataflow* graphs, fully tested via `reconstructions/co-simulation/test_orchestrator.py`.

### 3. Native WebAssembly & Pyodide Interactive Playgrounds
- [x] **In-Browser Execution**: Embedded our Python reconstructions directly into a client-side single-page app (`playground.html`) using Pyodide to compile/interpret Python directly in the user's browser.
- [x] **Interactive Visual UIs**: Built lightweight browser-native consoles and dashboards, allowing readers to write code, inject faults, trigger capability bounds violations, and inspect register states in real-time.

### 4. Academic Lab Manual & Pedagogical Sandboxes
- [x] **Curated Lab Modules**: Authored a series of interactive pedagogical lab sheets (`reconstructions/LAB_MANUAL.md`) designed for university systems-architecture curricula.
- [x] **Hands-on Clean-Slate Challenges**: Included problems such as "Designing a Ternary Half-Adder," "Custom Mathematical Pipelined Dataflow Graph," "Implementing Secure Domain Transitions," and "Deadlock-Avoiding Message Broker" complete with model solutions.

---

# Phase VII — Relational Density, Architectural Integrity & Taxonomic Synthesis ✅ (Complete)

To elevate the repository from a decoupled database into a highly cohesive, non-linear knowledge fabric, Phase VII focuses on increasing explanatory density across all architectural and taxonomic layers.

### 1. Eliminating Topological Symmetries & Gaps
- [x] **Weaving Isolated Excavations**: Connected previously isolated excavations—specifically `associative-processors.md`, `intel-iapx-432.md`, and `graph-reduction-machines.md`—to relevant synthesis essays and patterns, fully integrating them into the comparative taxonomy.
- [x] **Taxonomic Cohesion**: Established outbound relational links from all synthesis essays to back their conceptual frameworks with concrete historical excavations.

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

# Phase IX — Quantitative Constraint Forecasting ✅ (Complete)

Designed, verified, and released an active, quantitative forecasting model that translates post-CMOS physical limits directly into alternative hardware lineage scores.

- [x] **Quantitative Constraint Forecasting Model**: Designed dynamic scoring equations that map copper interconnect resistance, memory walls, static gate leakage, and AI tensor demands to our 6 core lineages.
- [x] **Highly Connected Research Hypotheses**: Programmed automated hypothesis generation delivering precise, non-partisan, primary-source-aligned resurrection briefs for high-bottleneck scenarios.
- [x] **Interactive Command-Line Interface**: Released a fully-functional CLI parser supporting customized physical parameters, text tables, star ratings, and JSON export for automated ingestion.
- [x] **Zero-Dependency Validation Suite**: Verified prediction bounds clamping, input sensitivity, and schema layout through extensive pytest unit tests.

---

# Phase X — Co-Simulation Fabric & Alternative Lineage Scorecards ✅ (Complete)

Integrated and validated the multi-architecture co-simulation harness while unifying the scorecard evaluation across all 35 excavations.

- [x] **Physical Co-Simulation Execution**: Established verified execution routines for 15 Python simulators and co-simulation orchestrators.
- [x] **Robust Error Handling & Edge Cases**: Hardened multi-architecture message queues, thread-safe message passing, and deadlock recovery strategies.
- [x] **Lineage Baseline Consolidation**: Linked physical co-simulation behaviors directly to the six architectural lineages documented in the [Modern Revival Readiness Scorecard](modern-relevance/revival-readiness.md) and evaluated in [State of Revival Synthesis](synthesis/state-of-revival.md).

---

# Phase XI — High-Level Hardware Synthesis (HLS) & Open-ASIC Toolchain Integration (2026-2027) 🛠️ (Active / Planning)

As silicon design shifts toward rapid prototyping and domain-specific acceleration, Phase XI bridges functional Python simulators with synthesizable hardware models through open-source high-level synthesis (HLS) and automated ASIC toolchains.

### 1. Python-to-HDL Compilation Pathways
- **High-Level Synthesis (HLS)**: Investigate Python-to-HDL frameworks (such as PyMTL3 or Amaranth HDL) to programmatically transpile our behavioral Python simulators (such as the *Dynamic Dataflow Engine* or *Systolic Array*) into synthesizable SystemVerilog.
- **Parametric RTL Generators**: Build parameterizable Verilog generators for alternate mathematical paradigms, including variable-bit unipolar/bipolar stochastic logic bitstreams and symmetric balanced ternary ALUs scaling from 3-trit to 27-trit widths.

### 2. Open ASIC Toolchain Targeting (Tiny Tapeout & SkyWater 130)
- **Tapeout Readiness**: Adapt synthesizable soft-cores (`ternary_alu.sv` and `capability_bounds_checker.sv`) to meet the strict pin, area, and clock limitations of [Tiny Tapeout](https://tinytapeout.com/).
- **OpenLane GDSII Synthesis**: Establish automated scripts to compile alternative hardware modules through the open-source OpenLane/yosys ASIC synthesis flow, targeting the SkyWater 130nm open shuttle process. Produce report metrics for estimated gate counts, cell area, static power dissipation, and maximum operating frequency.

---

# Phase XII — Distributed WebAssembly Co-Simulation Grid & P2P Research Nodes (2027-2028) 🌐 (Planning)

To scale alternative computational model testing beyond isolated browser windows, Phase XII transitions the Pyodide-based sandbox into a distributed, peer-to-peer co-simulation grid.

### 1. Browser-to-Browser Co-Simulation Fabrics
- **WebRTC Inter-Paradigm Pipelines**: Build a client-side WebRTC messaging layer within `playground.html`, enabling users to connect their browsers into decentralized cluster networks.
- **Distributed Multi-Architecture Pipelines**: Orchestrate cross-browser co-simulations where one browser node runs an event-driven *Neuromorphic Spiking* simulator feeding spikes over WebRTC channels to a second browser running a concurrent *CSP messaging* or *Linda Tuple Space* process engine.

### 2. Visual Performance & Network Profiling
- **Global Logic Analyzer Web-Socket Bridge**: Expand the canvas-based Live Digital Logic Analyzer to monitor, render, and capture logic transitions, queue depths, and channel rendezvous times across distributed physical nodes in real-time.
- **P2P Research Node Exchange**: Allow researchers to share custom simulation profiles, custom-weighted constraint parameters from the Predictive Hypothesis Engine, and binary fault-injection tests directly between nodes without a centralized database.

---

# Phase XIII — Agentic Co-Design, Neuro-Symbolic Validation, & Automated Architectural Discovery (2028-2030) 🧠 (Vision)

The ultimate frontier of Digital Archaeology transitions the researcher from manual excavation to steering autonomous systems that recursively search, evaluate, and synthesize non-von Neumann systems.

### 1. Autonomous Agent-in-the-Loop Synthesis
- **LLM-Driven Hardware Co-Design**: Establish structured JSON schemas and tooling APIs enabling autonomous LLM-based coding agents to query the Predictive Hypothesis Engine, construct alternate mathematical circuits, and evaluate performance bottlenecks.
- **Neuro-Symbolic Search & Verification**: Combine the *Neuro-Symbolic Inference Solver* with formal SAT/SMT verifiers (like z3-solver compiled to WebAssembly) to automatically search the hardware-software design space, checking capability boundary safety rules and proving that synthesized circuits are structurally immune to memory-corruption attacks.

### 2. Self-Optimizing Compilers for Sidelined Silicon
- **Machine-Generated Intermediate Representations (IR)**: Design a unified compiler intermediate representation (IR) capable of compiling high-level programming constructs into targets spanning custom systolic spatial grids, tagged-token dataflow pipelines, and stochastic bit-serial execution units.
- **Recursive Co-Design Optimization**: Implement a machine-learning loop that adjusts simulated hardware topologies (e.g., systolic array weight-stationary sizing, dataflow match-table capacities) and re-compiles the target workloads recursively until the optimal energy-delay-product (EDP) is discovered for a given constraint migration profile.

---

# Long-Term Vision

Digital Archaeology seeks to become the premier comparative reference and execution playground for abandoned and underexplored computing paradigms.

Rather than asking only *"What happened?"*, the project systematically asks:

- What powerful abstraction was introduced?
- Why did it disappear?
- Which engineering or economic forces selected against it?
- Which parts survived in disguise?
- Which physical or logical constraints have migrated since?
- How should we build it differently today under modern sub-5nm, AI, or secure boundaries?

The ultimate goal is to help computer engineers, systems researchers, and autonomous agent networks recover valuable ideas from systems history and re-evaluate them to guide the next fifty years of computer architecture design.

---

**Last updated**: August 2, 2026
