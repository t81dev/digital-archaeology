# Digital Archaeology

[![Research Phase: Active](https://img.shields.io/badge/Research--Phase-Active-success.svg)](ROADMAP.md)
[![Reconstructions: 33 Simulators & Models](https://img.shields.io/badge/Reconstructions-33%20Simulators-blue.svg)](#interactive-reconstructions-simulators)
[![Completed Excavations: 61](https://img.shields.io/badge/Completed--Excavations-61-orange.svg)](#project-pillars)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> *Excavating forgotten ideas. Recovering lost innovations. Reconstructing alternate futures.*

**Digital Archaeology** is an open-source, multi-disciplinary research initiative and execution sandbox dedicated to the rediscovery, simulation, and hardware-reconstruction of historically sidelined computing paradigms. As modern Silicon scaling hits the Von Neumann memory wall, Dennard scaling limits, and the "security wall," these forgotten architectures offer elegant, proven blueprints for domain-specific acceleration, hardware-enforced security, and distributed coordination.

> 🎓 **Academic Entry Point & Research Reference**: If you are an external researcher, academic, or computer architect, please review and cite our **[Academic Overview & Research Entry Point](synthesis/digital-archaeology-overview.md)**, which compiles our six core lineages, core methodological claims on [constraint migration](patterns/constraint-migration.md) and explanatory density, and a standard BibTeX citation block.

---

### 🏃 Runnable Multi-Paradigm Experiments (One-Command Demo)

We maintain three concrete cross-paradigm architectural experiments implementing synergistic connections across different sidelined lineages ([systolic array](GLOSSARY.md) + cryogenic logic; reversible uncomputation + Landauer thermal dissipation; 9P dynamic namespaces + hardware capability bounds check):

```bash
# Run all three co-simulation experiments with a single clear command
python3 -m reconstructions.co-simulation.experiments --all
```

*For more details on the setup or to run specific experiments, see [State of Revival Synthesis](synthesis/state-of-revival.md) and our [Synthesizable Hardware Integration Guide](reconstructions/synthesizable-hardware/README.md).*

---

### ⚡ Project in <60 Seconds

Digital Archaeology bridges systems history with modern hardware/software co-design through four deeply-deepened architectural lineages:

1. **Spatial & Data-Parallel**: Homogeneous grids bypassing global clock/bus bottlenecks. Features **Systolic Arrays** (TPU-style wave compute), **Dataflow Engines** (token-tag scheduling), and **Transputers** (native CSP channels).
2. **Capability, Tagged & Descriptor**: Fine-grained, hardware-enforced security boundaries. Features **CHERI-style Capabilities**, **Lisp Machine Type Tagging**, and **Burroughs Descriptor-Based Virtualization**.
3. **Physical, Thermodynamic & Optical**: Exploiting continuous physics for sub-nanosecond compute. Features **Analog Memristive Crossbars**, **Silicon Photonics (MZI meshes)**, and **Reversible/Adiabatic Logic** bypassing Landauer limits.
4. **Distributed Systems & Single-Level-Store OS**: Decoupled, location-transparent namespaces. Features **Plan 9 Dynamic Namespaces**, **9P Protocol message servers**, **Multics SLS**, and **Inferno VM**.

* **Where is the Revival Scorecard?** Explore the [Modern Revival Readiness Scorecard](modern-relevance/revival-readiness.md) for a quantitative, analytical comparative scorecard and high-density constraint-migration synthesis evaluating these lineages under modern sub-5nm silicon constraints.
* **Where are the Simulators?** We maintain **18 zero-dependency simulators** and synthesizable SystemVerilog soft-cores. Run them instantly (e.g., `python3 reconstructions/systolic-array/systolic_sim.py` or `python3 reconstructions/plan9-9p/namespace_sim.py`).

---

### 🗺️ Start Here Pathways

Select your specialization to discover immediate entry points into the repository:

#### 🛠️ The Hardware Architect / AI Engineer
* **Understand the Limits**: Read the [Return of Spatial Computing](synthesis/return-of-spatial-computing.md) and [AI & Hardware Bottlenecks](modern-relevance/ai.md) to understand spatial, neuromorphic, and stochastic acceleration.
* **Analyze the Models**: Compare execution efficiencies in the [Revival Readiness Scorecard](modern-relevance/revival-readiness.md).
* **Execute Simulators**: Run the cycle-accurate [Systolic Array Simulator](reconstructions/systolic-array/systolic_sim.py) (`python3 reconstructions/systolic-array/systolic_sim.py`), the [Neuromorphic Spiking Simulator](reconstructions/neuromorphic-spiking/spiking_sim.py), or explore synthesizable RTL (including our stochastic multiplier) under [Synthesizable Hardware Blueprints](reconstructions/synthesizable-hardware/).

#### 🛡️ The Security Researcher / OS Designer
* **Explore Capabilities**: Read the [Capability-Based Security Synthesis](synthesis/capability-based-security.md) and explore the hardware-enforced memory boundary models.
* **Run the Emulators**: Execute the [Capability Memory Protection Emulator](reconstructions/capability-security/capability_sim.py) (`python3 reconstructions/capability-security/capability_sim.py`) to simulate tagged RAM protection, out-of-bounds violations, and Burroughs descriptors.
* **Review synthesizable code**: Inspect the inline [Synthesizable Capability Bounds Checker SV core](reconstructions/synthesizable-hardware/capability_bounds_checker.sv).

#### 🌐 The Distributed Systems Engineer / Agentic AI Designer
* **Unpack Coordination**: Read [The Evolution of Coordination Abstractions](synthesis/evolution-of-coordination-abstractions.md) analyzing how 9P namespaces and tuple spaces decouple communication.
* **Build namespaces**: Walk through [Lab Module 6](reconstructions/LAB_MANUAL.md#lab-module-6-distributed-namespaces-9p-protocol-messages) to understand dynamic union mounts and remote-local transparency.
* **Run 9P simulator**: Execute `python3 reconstructions/plan9-9p/namespace_sim.py` to see 9P protocol messages (Twalk, Tread, Twrite) routing resource namespaces.

#### 🎓 The Computer Science Student / Instructor
* **Interactive Exploration**: Open [explorer.html](explorer.html) to interactively explore the multidimensional taxonomy. Or use [playground.html](playground.html) to run and modify simulators online.
* **Follow University Labs**: Walk through the seven university-level courses in [Academic Lab Manual & Pedagogical Sandboxes](reconstructions/LAB_MANUAL.md).
* **Verify Reconstructions**: Run the complete test suite with `pytest` locally to confirm execution and correctness of every simulator.

---

```text
                     Digital Archaeology Research Framework
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
  [EXCAVATIONS]                    [SYNTHESIS]                   [RECONSTRUCTIONS]
 40 deep dives into              Comparative and                18 executable models
 historical paradigms.          architectural essays.           and simulators.
        │                               │                               │
        └───────────────────────────────┼───────────────────────────────┘
                                        ▼
                                [MODERN RELEVANCE]
                             Applying historic ideas
                              to AI, FPGAs, & ASIC.
```

---

## 👁️ Philosophical Framework: Explanatory Density

The core mission of the **Digital Archaeology** initiative is not merely to catalog historical computing curiosities, but to **increase the explanatory power** of the repository by unearthing and synthesizing the underlying abstractions that govern architectural evolution.

Every technology—whether a clockless asynchronous processor or a hardware-enforced object capability system—is treated not as an isolated dead-end, but as **evidence of a deeper computational idea** that evolves across decades, hardware generations, and software ecosystems.

To achieve this, our research framework operates across six deeply interconnected layers:

```text
               [1. PRESERVE HISTORICAL ARTIFACTS]
                                │
                                ▼
               [2. EXTRACT ENDURING ABSTRACTIONS]
                                │
                                ▼
              [3. RECONSTRUCT PHYSICAL MECHANISMS]
                                │
                                ▼
               [4. WEAVE THE KNOWLEDGE GRAPH]
                                │
                                ▼
               [5. CONNECT TO MODERN ENGINEERING]
                                │
                                ▼
               [6. DERIVE EVIDENCE-BASED HYPOTHESES]
```

1. **Preserving Historical Artifacts**: Documenting the primary-source-backed designs, specific socio-economic constraints, and physical limitations that led to the sidelining of critical historical systems.
2. **Extracting Enduring Abstractions**: Isolating elegant logical principles (e.g., capability bounds, dataflow routing, coordinate-free coordination) from the transient hardware limits that originally bound them.
3. **Reconstructing Historical Mechanisms**: Building executable, zero-dependency software simulators and synthesizable SystemVerilog RTL cores to prove and verify the physical mechanics of alternative architectures.
4. **Connecting Concepts through the Knowledge Graph**: Structuring a dense network of multi-dimensional relationships using machine-readable schemas (`modern-relevance/knowledge_graph.json`) and interactive D3 force-directed visualizations (`explorer.html`) to expose cross-cutting architectural dynamics.
5. **Relating to Modern Engineering Practice**: Directly mapping forgotten paradigms to contemporary frontiers—such as utilizing analog and optical models for sub-nanosecond AI tensor cores, or CHERI-style tagged memory for cloud-native zero-trust networks.
6. **Deriving Evidence-Based Hypotheses**: Formulating predictive models for future computing transitions (e.g., non-von Neumann co-processors, compile-time hardware-compiler co-design) based on how physical constraints migrate over time.

### Non-Linear Evolution & The Sparsity-to-Density Imperative
Computing history is non-linear. Abstractions do not die; they migrate under shifting engineering and economic limits. When physical boundaries (such as the end of Dennard scaling or the Von Neumann memory wall) change, previously discarded designs are resurrected.

Therefore, any expansion of this repository must favor **dense networks of relationships over isolated documents**. Success is measured not by the quantity of articles written, but by the repository's ability to explain why computing evolved as it did—and where those evolutionary forces are likely to lead next. Before proposing or contributing a new excavation, we systematically:
* **Identify Missing Abstractions**: Pinpoint structural gaps in the execution, memory protection, and concurrency taxonomy.
* **Map Weak Connections**: Cross-reference the new concept with existing excavations to trace how similar ideas evolved concurrently.
* **Synthesize Recurring Patterns**: Connect the new technology to economic, ecosystem, and constraint-migration dynamics to explain *why* it was sidelined and *how* it might return.

---

## 🏛️ Project Pillars

The project structure is organized to bridge historical research with modern execution:

### 1. [Excavations](excavations/) (Historical Deep Dives)
Comprehensive, primary-source-backed investigations of 38 landmark computing paradigms, evaluated using a standardized evaluation format and rating system.
* **Architectures**: [Analog Computing](excavations/analog-computing.md) • [Associative Processors](excavations/associative-processors.md) • [Asynchronous Processors](excavations/asynchronous-processors.md) • [Balanced Ternary](excavations/balanced-ternary.md) • [Cellular Automata Hardware](excavations/cellular-automata-hardware.md) • [Connection Machine](excavations/connection-machine.md) • [Dataflow Computing](excavations/dataflow-computing.md) • [EBCDIC](excavations/ebcdic.md) • [Explicit Data Graph Execution (EDGE)](excavations/edge-architecture.md) • [Fluidic Logic Systems](excavations/fluidic-logic-systems.md) • [Graph Reduction Machines](excavations/graph-reduction-machines.md) • [MIT J-Machine](excavations/j-machine.md) • [Logarithmic Number System (LNS)](excavations/logarithmic-number-system.md) • [Molecular/Biocomputing](excavations/molecular-biocomputing.md) • [Neuromorphic](excavations/neuromorphic-hardware.md) • [ONNX Substrate](excavations/onnx.md) • [Optical Computing](excavations/optical-computing.md) • [Posit Arithmetic](excavations/posit-arithmetic.md) • [Residue Number System (RNS)](excavations/residue-number-system.md) • [Reversible Computing](excavations/reversible-computing.md) • [Stack Machines](excavations/stack-machines.md) • [Stochastic Computing](excavations/stochastic-computing.md) • [Superconducting/Cryogenic](excavations/superconducting-cryogenic.md) • [Systolic Arrays](excavations/systolic-arrays.md) • [Transputers](excavations/transputers.md) • [Vector Supercomputing](excavations/vector-supercomputing.md) • [VLIW/EPIC](excavations/vliw-epic.md) • [Wafer-Scale Integration](excavations/wafer-scale-integration.md)
* **Operating Systems & Substrates**: [Apple](excavations/apple.md) • [Apple Metal Architecture](excavations/apple-metal.md) • [BeOS / Haiku](excavations/beos-haiku.md) • [Burroughs Large Systems](excavations/burroughs-large-systems.md) • [Capability Systems](excavations/capability-systems.md) • [Cursor IDE](excavations/cursor-ide.md) • [Gentoo](excavations/gentoo.md) • [Google](excavations/google.md) • [Inferno](excavations/inferno.md) • [Intel](excavations/intel.md) • [Intel iAPX 432](excavations/intel-iapx-432.md) • [KeyKOS & Nanokernel Capabilities](excavations/keykos-nanokernel-capabilities.md) • [Large Language Models](excavations/large-language-models.md) • [Linux](excavations/linux.md) • [Lisp Machines](excavations/lisp-machines.md) • [llama.cpp](excavations/llama-cpp.md) • [Microsoft](excavations/microsoft.md) • [Multics](excavations/multics.md) • [Netscape](excavations/netscape.md) • [NVIDIA](excavations/nvidia.md) • [OpenAI](excavations/openai.md) • [Plan 9](excavations/plan-9.md) • [Portage](excavations/portage.md) • [Project Xanadu](excavations/project-xanadu.md) • [Qt](excavations/qt.md) • [Qwen Lineage](excavations/qwen.md) • [Safari](excavations/safari.md) • [Winamp](excavations/winamp.md)
* **Languages, Concurrency & AI**: [C++](excavations/cpp.md) • [Linda Tuple Spaces](excavations/linda-tuple-spaces.md) • [Occam](excavations/occam.md) • [Smalltalk](excavations/smalltalk.md) • [Symbolic AI](excavations/symbolic-ai.md) • [Prolog, WAM & FGCS Hardware](excavations/prolog-wam-fgcs-hardware.md)

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
* **[Cross-Excavation Recent Inclusions Synthesis](synthesis/recent-inclusions-crosscut.md)** — High-density architectural and mechanistic synthesis of RNS, LNS, fluidic logic, KeyKOS capabilities, and Prolog/WAM/FGCS hardware.
* **[The Return of Spatial Computing](synthesis/return-of-spatial-computing.md)** — How dataflow, parallel grid, and neuromorphic models are taking over AI acceleration.

### 4. [Modern Relevance](modern-relevance/) (Practical Application)
Direct mapping of historical concepts to contemporary engineering challenges:
* **[Academic Research & Hardware Partnerships](modern-relevance/partnerships.md)** — Connecting key excavations to active academic labs, zero-trust security initiatives, and open-source FPGA/ASIC hardware toolchains.
* **[AI & Hardware Bottlenecks](modern-relevance/ai.md)** — Tackling the memory wall and matrix acceleration using non-von Neumann models.
* **[Coprocessors](modern-relevance/coprocessors.md)** — Domain-specific coprocessing offloaded from general-purpose CPUs.
* **[FPGA Prototyping](modern-relevance/fpga.md)** — Reconfigurable logic as a high-fidelity sandbox for architectural experimentation.
* **[Mixed-Radix & Alternative Math](modern-relevance/mixed-radix.md)** — Evaluating ternary logic, logarithmic number systems, and posits in silicon.
* **[Symbolic Computing](modern-relevance/symbolic-computing.md)** — Hybrid neuro-symbolic models, theorem proving, and deterministic LLM guardrails.

---

## 💻 Interactive Reconstructions & Simulators

Moving from historical theory to active software and hardware prototyping, we maintain a suite of **15 zero-dependency executable models and simulators** that let you execute and study these paradigms directly.

| Simulator / Emulator | Target Historical Paradigm | Key Architectural Highlight | Entry Point |
| :--- | :--- | :--- | :--- |
| 🧮 **[Balanced Ternary Simulator](reconstructions/mixed-radix-sim/)** | [Setun Ternary Computer](excavations/balanced-ternary.md) | Sign-bit-free arithmetic, trit-level logic, and radix economy demonstrating Base-3 advantages. | `reconstructions/mixed-radix-sim/ternary_sim.py` |
| ❄️ **[Cryogenic Superconducting Simulator](reconstructions/cryogenic-superconducting/)** | [Superconducting & Cryogenic](excavations/superconducting-cryogenic.md) | Picosecond-accurate Rapid Single Flux Quantum (RSFQ) pulse logic timing, setup-time check, and refrigeration penalty. | `reconstructions/cryogenic-superconducting/sfq_sim.py` |
| 🔄 **[Dynamic Token Dataflow Engine](reconstructions/dataflow-engine/)** | [MIT Tagged-Token Dataflow](excavations/dataflow-computing.md) | Out-of-order, asynchronous spatial execution using token-tag match scheduling. | `reconstructions/dataflow-engine/dataflow_sim.py` |
| 🛡️ **[Capability Memory Protection Emulator](reconstructions/capability-security/)** | [Burroughs Systems / CHERI](excavations/capability-systems.md) | CPU & Tagged RAM emulator simulating hardware-enforced memory bounds and secure domain gates. | `reconstructions/capability-security/capability_sim.py` |
| 🧠 **[Neuro-Symbolic Inference Solver](reconstructions/neuro-symbolic/)** | [Symbolic AI / Expert Systems](excavations/symbolic-ai.md) | Hybrid pipeline mapping probabilistic neural classifier confidences into deterministic logic. | `reconstructions/neuro-symbolic/neuro_symbolic_sim.py` |
| 📞 **[CSP Synchronous Messaging Simulator](reconstructions/csp-messaging/)** | [Occam](excavations/occam.md) • [Transputers](excavations/transputers.md) | Cooperative generator scheduler implementing synchronous rendezvous, ALT choice, and deadlock reporting. | `reconstructions/csp-messaging/csp_sim.py` |
| 🌊 **[Analog & Optical Wave Accelerator](reconstructions/analog-optical/)** | [Analog Computing](excavations/analog-computing.md) • [Optical Computing](excavations/optical-computing.md) | Continuous-physical electronic op-amp solver paired with a Mach-Zehnder Interferometer photonic tensor core. | `reconstructions/analog-optical/analog_optical_sim.py` |
| 🛠️ **[Synthesizable Hardware Blueprints](reconstructions/synthesizable-hardware/)** | [Balanced Ternary](excavations/balanced-ternary.md) • [Capability Systems](excavations/capability-systems.md) • [Stochastic Computing](excavations/stochastic-computing.md) | Synthesizable SystemVerilog models of a 3-trit Balanced Ternary ALU, a Tagged RAM Capability Bounds Checker, and a Stochastic Multiplier. | `reconstructions/synthesizable-hardware/` |
| 🔀 **[Co-Simulation Interoperability Fabric](reconstructions/co-simulation/)** | Hybrid AI • CSP Concurrency • Spatial Dataflow | Sandbox orchestrator running multiple reconstructed engines simultaneously and coordinating cross-paradigm messaging. | `reconstructions/co-simulation/orchestrator.py` |
| 🗃️ **[Linda Tuple Space Simulator](reconstructions/tuple-space/)** | [Linda Tuple Spaces](excavations/linda-tuple-spaces.md) | Thread-safe, associative coordinate-free generative communication engine with pattern-matching. | `reconstructions/tuple-space/tuple_space_sim.py` |
| 🎲 **[Stochastic Computing Simulator](reconstructions/stochastic-computing/)** | [Stochastic Computing](excavations/stochastic-computing.md) | Probabilistic arithmetic, MUX weighted additions, saturating FSM-based activations, LFSR generation, neuron/filter workloads. | `reconstructions/stochastic-computing/stochastic_sim.py` |
| 🕸️ **[Plan 9 Namespace Simulator](reconstructions/plan9-9p/)** | [Plan 9](excavations/plan-9.md) • [Inferno](excavations/inferno.md) | Stateful 9P/Styx transaction processor simulating private namespaces, mounts, binds, and union directories. | `reconstructions/plan9-9p/namespace_sim.py` |
| 🧮 **[Systolic Array Simulator](reconstructions/systolic-array/)** | [Systolic Arrays](excavations/systolic-arrays.md) | Cycle-accurate simulation of Weight-Stationary and Output-Stationary dataflows with CMOS energy proxy metrics. | `reconstructions/systolic-array/systolic_sim.py` |
| 🧠 **[Neuromorphic Spiking Simulator](reconstructions/neuromorphic-spiking/)** | [Neuromorphic Hardware](excavations/neuromorphic-hardware.md) | Event-driven SNN routing using Leaky Integrate-and-Fire (LIF) dynamics and STDP learning rules. | `reconstructions/neuromorphic-spiking/spiking_sim.py` |
| 🎲 **[Predictive Hypothesis Engine](reconstructions/predictive-hypothesis/)** | [Constraint Migration](patterns/constraint-migration.md) • [Recurring Ideas](patterns/recurring-ideas.md) | Forecaster modeling emerging post-CMOS physics and predicting alternative hardware lineage revival scores. | `reconstructions/predictive-hypothesis/predictive_engine.py` |
| 🧮 **[RNS Arithmetic Simulator](reconstructions/rns-arithmetic/)** | [Residue Number System (RNS)](excavations/residue-number-system.md) | Parallel, carry-free componentwise modular addition/multiplication and CRT decoding. | `reconstructions/rns-arithmetic/rns_sim.py` |
| 🧮 **[LNS Arithmetic Simulator](reconstructions/lns-arithmetic/)** | [Logarithmic Number System (LNS)](excavations/logarithmic-number-system.md) | Logarithmic encoding/decoding, multiplication/division, and Jacobian log adder. | `reconstructions/lns-arithmetic/lns_sim.py` |
| 🛡️ **[KeyKOS-style Capability Simulator](reconstructions/keykos-capabilities/)** | [KeyKOS Capabilities](excavations/keykos-nanokernel-capabilities.md) | Unforgeable keys, attenuation, message-invocation routing, and orthogonal persistence. | `reconstructions/keykos-capabilities/keykos_sim.py` |
| 💻 **[Cursor IDE Substrate Simulator](reconstructions/cursor_ide/)** | [Cursor IDE](excavations/cursor-ide.md) | Budgeted context packet assembly, speculative diff patch generation/approval checkpoints, and supervised agent tool self-correction loops. | `reconstructions/cursor_ide/cursor_sim.py` |
| 🧮 **[llama.cpp Local Simulator](reconstructions/llama_cpp/)** | [llama.cpp Quantization](excavations/llama-cpp.md) | GGUF aligned packing/unpacking, block-wise Q4_0 integer quantization, and dequantization-on-the-fly matmul. | `reconstructions/llama_cpp/llama_cpp_sim.py` |
| 🔄 **[MapReduce Simulator](reconstructions/mapreduce/)** | [Google Platform](excavations/google.md) | Functional data partitioning, intermediate key shuffling, and fault-tolerant retry/recovery on node failure. | `reconstructions/mapreduce/mapreduce_sim.py` |
| 🎮 **[Apple Metal Command & UMA Simulator](reconstructions/apple_metal/)** | [Apple Metal Architecture](excavations/apple-metal.md) | Low-overhead command encoding, immutable pipeline state objects, TBDR load/store actions, and UMA memory modes. | `reconstructions/apple_metal/metal_sim.py` |
| ⚡ **[NVIDIA SIMT Microarchitecture Simulator](reconstructions/nvidia_simt/)** | [NVIDIA Architecture](excavations/nvidia.md) | Warp SIMT execution, active mask divergence stack, warp scheduling, shared memory bank conflicts, and Tensor Cores. | `reconstructions/nvidia_simt/simt_sim.py` |
| ⚙️ **[C++ RAII & Zero-Overhead Dispatch Simulator](reconstructions/cpp_raii/)** | [C++](excavations/cpp.md) | Scope-bound RAII cleanup, exception unwinding, static template monomorphization vs. vtable dynamic dispatch metrics, and iterator contracts. | `reconstructions/cpp_raii/cpp_raii_sim.py` |
| 🎵 **[Winamp Plugin Host & Pipeline Simulator](reconstructions/winamp_plugin_host/)** | [Winamp](excavations/winamp.md) | C-ABI plugin jump-tables, decoupled audio pipelines (Input/DSP/Output), classic skin sprite mapping, and M3U/PLS media library indexing. | `reconstructions/winamp_plugin_host/winamp_sim.py` |
| 🌐 **[Netscape Browser Runtime Simulator](reconstructions/netscape_browser_runtime/)** | [Netscape](excavations/netscape.md) | DOM event-driven JS host, Same-Origin Policy (SOP), NPAPI plugin dispatcher, HTTP cookie session state, and SSL/TLS certificate trust evaluation. | `reconstructions/netscape_browser_runtime/netscape_sim.py` |
| 🌐 **[Safari & WebKit Runtime Simulator](reconstructions/safari_webkit_runtime/)** | [Safari](excavations/safari.md) | WebKit2 multi-process IPC, WKWebView host insulation, and ITP double-keyed storage partitioning. | `reconstructions/safari_webkit_runtime/safari_sim.py` |
| 🖥️ **[Qt Meta-Object & Signals Simulator](reconstructions/qt_meta_object_signals/)** | [Qt](excavations/qt.md) | `QObject` parent-child tree ownership, `moc` reflection metadata, Signals & Slots dispatch, and QML property bindings. | `reconstructions/qt_meta_object_signals/qt_sim.py` |
| ⚙️ **[Portage Engine & USE-Flag Simulator](reconstructions/gentoo_portage/)** | [Gentoo](excavations/gentoo.md) | Cascading profile policy inheritance, USE flag dependency graph mutation, slotting, LD_PRELOAD build sandboxing, and VDB state tracking. | `reconstructions/gentoo_portage/portage_sim.py` |

### Quick Start: Running the Simulators
You can run all simulators locally out-of-the-box. They are written in standard Python 3 and require no third-party libraries:

```bash
# Clone the repository
git clone https://github.com/t81dev/digital-archaeology.git
cd digital-archaeology

# Run the Cryogenic Superconducting & SFQ Pulse Simulator
python3 reconstructions/cryogenic-superconducting/sfq_sim.py

# Run the Plan 9 Namespace & 9P Protocol Simulator
python3 reconstructions/plan9-9p/namespace_sim.py

# Run the Systolic Array Matrix-Multiplication Simulator
python3 reconstructions/systolic-array/systolic_sim.py

# Run the Balanced Ternary & Mixed-Radix Simulator
python3 reconstructions/mixed-radix-sim/ternary_sim.py

# Run the Dynamic Dataflow Engine
python3 reconstructions/dataflow-engine/dataflow_sim.py

# Run the Capability-Based Security Emulator
python3 reconstructions/capability-security/capability_sim.py

# Run the Neuro-Symbolic Logic Solver
python3 reconstructions/neuro-symbolic/neuro_symbolic_sim.py

# Run the CSP Synchronous Messaging Simulator
python3 reconstructions/csp-messaging/csp_sim.py

# Run the Continuous Analog & Optical Wave Accelerator Simulator
python3 reconstructions/analog-optical/analog_optical_sim.py

# Run the Multi-Architecture Co-Simulation Orchestrator
python3 reconstructions/co-simulation/orchestrator.py

# Run the Linda Tuple Space Simulator
python3 reconstructions/tuple-space/tuple_space_sim.py

# Run the Stochastic Computing Simulator
python3 reconstructions/stochastic-computing/stochastic_sim.py

# Run the Neuromorphic Spiking Simulator
python3 reconstructions/neuromorphic-spiking/spiking_sim.py

# Run the Constraint Migration Predictive Hypothesis Engine
python3 reconstructions/predictive-hypothesis/predictive_engine.py

# Run the RNS Arithmetic Simulator
python3 reconstructions/rns-arithmetic/rns_sim.py

# Run the LNS Arithmetic Simulator
python3 reconstructions/lns-arithmetic/lns_sim.py

# Run the KeyKOS Capability Simulator
python3 reconstructions/keykos-capabilities/keykos_sim.py

# Run the llama.cpp Local Quantization and GGUF Simulator
python3 reconstructions/llama_cpp/llama_cpp_sim.py

# Run the MapReduce Distributed Compute Simulator
python3 reconstructions/mapreduce/mapreduce_sim.py

# Run the NVIDIA SIMT Microarchitecture Simulator
python3 reconstructions/nvidia_simt/simt_sim.py

# Run the Netscape Browser Runtime Simulator
python3 reconstructions/netscape_browser_runtime/netscape_sim.py

# Run the Safari & WebKit Runtime Simulator
python3 reconstructions/safari_webkit_runtime/safari_sim.py

# Run the Gentoo Portage Engine & USE-Flag Simulator
python3 reconstructions/gentoo_portage/portage_sim.py
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

*For definitions and details of these concepts, explore the [GLOSSARY.md](GLOSSARY.md) and our [COMPARATIVE_INDEX.md](COMPARATIVE_INDEX.md) which maps all 32 excavations across this matrix.*

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

* **[Academic Overview & Research Entry Point](synthesis/digital-archaeology-overview.md)** — A short, dense, citable reference introducing our lineages, methodology, and BibTeX citation block.
* **[INDEX.md](INDEX.md)** — The central directory and conceptual mapping of all files in this repository.
* **[Interactive Taxonomy Explorer](explorer.html)** — A dynamic, client-side visual web page mapping all excavations, paradigms, and execution-safety-concurrency models.
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
