# Computing Timeline

> *A chronological, high-density timeline of computing with emphasis on architectural lineages, [constraint migration](../patterns/constraint-migration.md), and recurring paradigm revivals.*

---

## Lineage Appearance by Era

The table below maps the six core lineages across historical computing eras, illustrating their periods of peak implementation and modern re-emergence.

| Core Lineage | Peak / Landmark Era | Modern Re-Emergence & Drivers |
|:---|:---|:---|
| **Spatial & Data-Parallel** | 1980s (Transputer, [Connection Machine](../excavations/connection-machine.md)) | AI Accelerators (TPU, Cerebras WSE, RDUs) |
| **Capability, Tagged & Descriptor** | 1970s–1980s (Burroughs B5000, iAPX 432, [Lisp Machines](../excavations/lisp-machines.md)) | Hardware Memory Safety (CHERI, RISC-V extensions) |
| **Physical, Thermodynamic & Optical**| 1940s–1950s (Analog machines), 1980s (Optical gates) | Post-CMOS Physics (AIMC crossbars, Photonics, [Reversible computing](../excavations/reversible-computing.md)) |
| **Distributed & Single-Level-Store OS**| 1960s ([Multics](../excavations/multics.md)), 1990s ([Plan 9](../excavations/plan-9.md), [Inferno](../excavations/inferno.md)) | Multi-Agent AI Systems, Cloud Orchestration, Edge Clusters |
| **Neuromorphic & Stochastic** | 1960s (Stochastic), 1980s (Mead's neuromorphic) | Sparse Edge AI, Noise-Tolerant Spiking Processors (TrueNorth, Loihi) |
| **Superconducting & Cryogenic** | 1950s (Cryotron), 1980s (Superconducting logic) | Quantum Control, High-Frequency SFQ Co-Processors (>100 GHz) |

---

## 1930s–1950s: Foundations & Alternative Logics

- **1936**: Alan Turing publishes *On Computable Numbers*, establishing the mathematical bounds of sequential algorithms.
- **1945**: John von Neumann's *First Draft of a Report on the EDVAC* formalizes the sequential control-flow CPU/memory split, creating the "[von Neumann bottleneck](../GLOSSARY.md)."
- **1940s–1950s**: Vacuum tube analog computers perform real-time continuous differential equation solving. **Key excavation link**: [Analog Computing](../excavations/analog-computing.md)
- **1956**: Dudley Buck proposes the superconducting cryotron switch, launching cryogenic logic research. **Key excavation link**: [Superconducting & Cryogenic Microarchitectures](../excavations/superconducting-cryogenic.md)
- **1958**: Moscow State University builds **Setun**, operating on symmetric ternary logic ($+1, 0, -1$) for superior arithmetic density. **Key excavation link**: [Balanced Ternary](../excavations/balanced-ternary.md)

---

## 1960s: Operating System Virtuosity & Early Scaling

- **1961**: Burroughs launches the **B5000**, integrating a zero-operand hardware evaluation stack with [descriptor-based memory](../GLOSSARY.md). **Key excavation links**: [Burroughs Large Systems](../excavations/burroughs-large-systems.md) | [Stack Machines](../excavations/stack-machines.md)
- **1964**: The **[Multics](../excavations/multics.md)** project begins, introducing dynamic segmentation, concentric ring-based hardware security, and single-level storage. **Key excavation link**: [Multics](../excavations/multics.md)
- **1965**: Ted Nelson conceptualizes **[Project Xanadu](../excavations/project-xanadu.md)**, a [bi-directional hypermedia](../GLOSSARY.md) network featuring deep versioning and micro-payments. **Key excavation link**: [Project Xanadu](../excavations/project-xanadu.md)
- **1967**: B.R. Gaines formalizes stochastic bitstream mathematics for low-cost probabilistic arithmetic. **Key excavation link**: [Stochastic Computing](../excavations/stochastic-computing.md)

---

## 1970s: Personal Environments & The Security Wall

- **1972**: Plessey launches **System 250**, the first commercial multiprocessor operating system utilizing hardware-enforced capabilities. **Key excavation link**: [Capability Systems](../excavations/capability-systems.md)
- **1972**: Xerox PARC develops **[Smalltalk](../excavations/smalltalk.md)-72** (later [Smalltalk](../excavations/smalltalk.md)-80), pioneering dynamic image-based object-oriented environments and virtual machine bytecode. **Key excavation link**: [Smalltalk](../excavations/smalltalk.md)
- **1973**: Charles Bennett proves that reversible, non-dissipative thermodynamic computation is possible. **Key excavation link**: [Reversible Computing](../excavations/reversible-computing.md)
- **1976**: Seymour Cray introduces the **Cray-1**, pioneering pipelined vector register processing. **Key excavation link**: [Vector Supercomputing](../excavations/vector-supercomputing.md)
- **1978**: H.T. Kung and Charles Leiserson formalize **[Systolic Arrays](../excavations/systolic-arrays.md)** for synchronous, localized 2D pipeline data streaming. **Key excavation link**: [Systolic Arrays](../excavations/systolic-arrays.md)

---

## 1980s: The Great Architectural Renaissance (Peak Experimentation)

- **1981**: [Intel](../GLOSSARY.md) ships the **iAPX 432**, a microcoded 32-bit CPU implementing object-oriented capabilities directly in hardware. **Key excavation link**: [Intel iAPX 432](../excavations/intel-iapx-432.md)
- **1981**: Arthur John Codd and colleagues build the **Manchester Dataflow Computer**, proving the viability of [dynamic token-matching](../GLOSSARY.md) execution. **Key excavation link**: [Dataflow Computing](../excavations/dataflow-computing.md)
- **1982**: Symbolics launches the **3600 Lisp Machine**, offering a hardware-tagged dynamic object-oriented environment. **Key excavation link**: [Lisp Machines](../excavations/lisp-machines.md)
- **1983**: Inmos introduces the **IMS T414 Transputer** and the concurrent language **[Occam](../excavations/occam.md)**, establishing native channel-based CSP messaging in hardware. **Key excavation links**: [Transputers](../excavations/transputers.md) | [Occam](../excavations/occam.md)
- **1985**: David Gelernter introduces **Linda**, a coordinate-free [generative communication](../GLOSSARY.md) system using associative tuple matching. **Key excavation link**: [Linda Tuple Spaces](../excavations/linda-tuple-spaces.md)
- **1985**: Chuck Moore designs the **Novix NC4016**, a microprocessor executing Forth instructions directly in hardware. **Key excavation link**: [Stack Machines](../excavations/stack-machines.md)
- **1985**: Danny Hillis designs the **[Connection Machine](../excavations/connection-machine.md) CM-1**, a massively parallel 65,536-processor bit-serial hypercube SIMD architecture. **Key excavation link**: [Connection Machine](../excavations/connection-machine.md)
- **1986**: The **ALICE** graph-reduction machine executes declarative, functional languages natively via packet-switched transputer networks. **Key excavation link**: [Graph Reduction Machines](../excavations/graph-reduction-machines.md)
- **1986**: MIT's **CAM-6** cellular automata machine implements physical field simulations on a custom spatial board. **Key excavation link**: [Cellular Automata Hardware](../excavations/cellular-automata-hardware.md)
- **1986**: Bell Labs demonstrates early photonic logic gates. **Key excavation link**: [Optical Computing](../excavations/optical-computing.md)
- **1988**: IBM launches the **AS/400**, introducing a layered architecture with Technology Independent Machine Interface (TIMI) intermediate code and a 64-bit single-level store. **Key excavation link**: [IBM AS/400](../excavations/ibm-as400.md)
- **1988**: The MIT **J-Machine** implements fine-grained 3D routing for [active messages](../GLOSSARY.md) and concurrent objects. **Key excavation link**: [The MIT J-Machine](../excavations/j-machine.md)
- **1989**: Carver Mead publishes *Analog VLSI and Neural Systems*, establishing the physical foundation for silicon brain-inspired computing. **Key excavation link**: [Neuromorphic Hardware](../excavations/neuromorphic-hardware.md)

---

## 1990s: Commodity Consolidation & The Software Backlash

- **1991**: Linus Torvalds releases Linux v0.01, establishing a monolithic hardware-decoupled kernel with a highly stable SCI. **Key excavation link**: [Linux](../excavations/linux.md)
- **1992**: Bell Labs begins distribution of **[Plan 9](../excavations/plan-9.md)**, a distributed successor to Unix implementing private dynamic namespaces via the Styx/[9P protocol](../GLOSSARY.md). **Key excavation link**: [Plan 9](../excavations/plan-9.md)
- **1994**: Leonard Adleman performs the first DNA-based molecular calculation. **Key excavation link**: [Molecular & Biocomputing](../excavations/molecular-biocomputing.md)
- **1995**: IBM executes the **AS/400 CISC-to-RISC migration**, retranslating compiled TIMI program binaries to 64-bit PowerPC RISC automatically without source code rewrites. **Key excavation link**: [IBM AS/400](../excavations/ibm-as400.md)
- **1995**: Be Inc. releases **BeOS**, a multi-threaded media-centric operating system optimized for responsive symmetrical multiprocessing. **Key excavation link**: [BeOS / Haiku](../excavations/beos-haiku.md)
- **1995**: Bell Labs introduces **[Inferno](../excavations/inferno.md)**, a distributed VM-based OS featuring the Limbo language and Dis virtual machine. **Key excavation link**: [Inferno](../excavations/inferno.md)
- **1990s**: The ARM-based **AMULET** asynchronous microprocessor series demonstrates high-performance, clockless self-timed logic. **Key excavation link**: [Asynchronous Microprocessors](../excavations/asynchronous-processors.md)
- **1990s**: Proliferation of compile-time explicit instruction scheduling. **Key excavation link**: [VLIW / EPIC Architectures](../excavations/vliw-epic.md)
- **1990s**: Early wafer-level packaging experiments fail commercially due to silicon defect rates. **Key excavation link**: [Wafer-Scale Integration](../excavations/wafer-scale-integration.md)

---

## 2000s: The Power Wall & Heterogeneous Offloading

- **2001**: [Intel](../GLOSSARY.md) releases the **Itanium** (EPIC architecture), shifting dependency resolution to compilers, but struggling with legacy x86 performance. **Key excavation link**: [VLIW / EPIC Architectures](../excavations/vliw-epic.md)
- **2003–2006**: The DARPA-funded **TRIPS (EDGE)** processor demonstrates instruction-level spatial dataflow compilation and block-structured scheduling. **Key excavation link**: [Explicit Data Graph Execution (EDGE)](../excavations/edge-architecture.md)
- **2004**: Dennard scaling breaks down (the Power Wall), ending the era of single-thread frequency scaling and forcing the industry toward multi-core CPUs.
- **2007**: Linux integrates the Kernel-based Virtual Machine (KVM) and container groups (cgroups), laying the foundation for modern cloud density. **Key excavation link**: [Linux](../excavations/linux.md)
- **Late 2000s**: The GPU revolution begins, repurposing 3D graphics hardware for massively parallel vector math. **Key excavation link**: [Associative Processors](../excavations/associative-processors.md)

---

## 2010s–Present: Post-CMOS Re-Emergence & AI Dominance

- **2014**: IBM reveals **TrueNorth**, a 1-million-neuron asynchronous spiking processor. **Key excavation link**: [Neuromorphic Hardware](../excavations/neuromorphic-hardware.md)
- **2014**: Apple introduces **[Metal](../excavations/apple-metal.md)**, pioneering low-overhead explicit command encoding, precompiled immutable PSOs, and explicit UMA memory storage modes, leading the transition away from OpenGL/OpenCL. **Key excavation link**: [Apple Metal Architecture](../excavations/apple-metal.md)
- **2014**: eBPF is integrated into the Linux kernel, turning supervisor space into a safe, programmable infrastructure substrate. **Key excavation link**: [Linux](../excavations/linux.md)
- **2019**: Cerebras launches the **Wafer-Scale Engine (WSE)**, bypassing package boundaries with a 400,000-core monolithic silicon wafer for AI workloads. **Key excavation link**: [Wafer-Scale Integration](../excavations/wafer-scale-integration.md)
- **2020**: OpenAI publishes empirical scaling laws for transformers, shifting machine learning systems from heuristic trial-and-error to predictable systems engineering. **Key excavation link**: [OpenAI](../excavations/openai.md)
- **2022**: OpenAI launches ChatGPT, demonstrating conversational interfaces and remote API-as-model abstractions as standard platform layers. **Key excavation link**: [OpenAI](../excavations/openai.md)
- **2023**: OpenAI introduces the Assistants API, standardizing stateful thread run loops and tool call schemas above traditional operating systems. **Key excavation link**: [OpenAI](../excavations/openai.md)
- **2020s**: AI hardware developers resurrect **[Systolic Arrays](../excavations/systolic-arrays.md)** ([Google](../GLOSSARY.md) TPUs), **[Stochastic Computing](../excavations/stochastic-computing.md)** for approximate low-power activations, and **Analog In-Memory Computing** (non-volatile memristors).
- **2020s**: Proliferation of heterogeneous coprocessors as general-purpose Moore's Law slows down.

---

## Major Recurring Themes

1. **[Constraint Migration](../patterns/constraint-migration.md)**: The dynamic shifting of physical limits (Power Wall, Memory Wall, Security Wall) which turns historical "inefficiencies" or "impracticalities" into absolute microarchitectural necessities.
2. **Centralization vs. Distribution of Control and Memory**: Moving from central instruction sequencing and shared memory pools toward decentralized, localized networks of autonomous processors (e.g., J-Machine, [Transputers](../excavations/transputers.md)).
3. **General-Purpose vs. Specialized Hardware**: The perpetual trade-off between the ease of general-purpose programming and the extreme efficiency of spatial/domain-specific hardware (e.g., GPGPUs, TPUs).
4. **Control-Flow vs. Dataflow Execution Models**: The tension between program-counter-driven sequential instruction execution and event-driven, token-matching spatial execution.
5. **Software Abstraction vs. Hardware Transparency**: The trade-off between shielding the developer from hardware physical realities and allowing them direct access for absolute performance.

---

## Lessons from Computing History

1. **Diversity peaks early**, then consolidation occurs around economically dominant solutions. The 1980s represent the absolute peak of architectural diversity, which was flattened by the economics of x86 and commodity packaging.
2. **Major constraint shifts reopen the design space**. Sidelined ideas are evaluated via the [Modern Revival Readiness Scorecard](../modern-relevance/revival-readiness.md), measuring five key pillars:
   - **[Constraint Migration](../patterns/constraint-migration.md) Status (CMS)**: Have physical or software limits pivoted in the lineage's favor?
   - **Silicon Readiness (SR)**: Can modern fabrication nodes and packaging support implementation?
   - **Software Ecosystem Friction (SEF)**: Can modern compilers (e.g., MLIR) hide historical routing complexities?
   - **Energy Advantage (EA)**: Does the lineage bypass the clock-tree and data-movement energy penalties?
   - **AI Synergy (AIS)**: Does the physical architecture map directly to linear algebra or inference tasks?
3. **Many “dead” ideas are not refuted — they are simply uneconomical under previous constraints**. As general-purpose CMOS scaling hits physical walls, historical alternative paradigms return as specialized engines inside heterogeneous systems.

---

## Related Resources

- [AI Timeline](./ai.md)
- [Hardware Timeline](./hardware.md)
- [Modern Revival Readiness Scorecard](../modern-relevance/revival-readiness.md)
- [Constraint Migration Pattern](../patterns/constraint-migration.md)

---
