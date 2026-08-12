# Comparative Index of Excavations

> **A multi-dimensional index mapping our 37 excavations across execution models, memory protection schemes, and concurrency paradigms.**

Digital Archaeology studies systems from different eras and physical media. To enable comparative research, this index organizes all 37 core excavations into structured technical categories rather than chronological timelines.

---

## 1. Index by Execution Model

How does the processor sequence and execute instruction streams?

| Execution Model | Description | Mapped Excavations |
|-----------------|-------------|---------------------|
| **Control-Flow (von Neumann)** | Sequential instruction execution guided by a program counter. Includes traditional stack-based and register-based architectures. | - [Apple: The Integrated Platform Surface](excavations/apple.md)<br>- [Asynchronous Microprocessors](excavations/asynchronous-processors.md)<br>- [BeOS / Haiku](excavations/beos-haiku.md)<br>- [Burroughs Large Systems](excavations/burroughs-large-systems.md)<br>- [Capability Systems](excavations/capability-systems.md)<br>- [EBCDIC (Extended Binary Coded Decimal Interchange Code)](excavations/ebcdic.md)<br>- [Inferno](excavations/inferno.md)<br>- [Intel iAPX 432](excavations/intel-iapx-432.md)<br>- [Linux: The Ubiquitous Substrate](excavations/linux.md)<br>- [Lisp Machines](excavations/lisp-machines.md)<br>- [Microsoft: The Platform Machine](excavations/microsoft.md)<br>- [Multics](excavations/multics.md)<br>- [OpenAI: The Model-as-Platform Substrate](excavations/openai.md)<br>- [Plan 9](excavations/plan-9.md)<br>- [Smalltalk](excavations/smalltalk.md)<br>- [Stack Machines](excavations/stack-machines.md)<br>- [The MIT J-Machine](excavations/j-machine.md)<br>- [Transputers](excavations/transputers.md) |
| **Dataflow (Non-von Neumann)** | Non-sequential, asynchronous execution driven entirely by input operand availability (tokens). | - [Dataflow Computing](excavations/dataflow-computing.md)<br>- [Explicit Data Graph Execution (EDGE) & The TRIPS Architecture](excavations/edge-architecture.md) |
| **Demand-Driven (Graph Reduction)** | Non-sequential expression evaluation driven by evaluation demand (lazy evaluation). Execution proceeds by physically rewriting active nodes (redexes) in a graph. | - [Graph Reduction Architectures & Functional Hardware](excavations/graph-reduction-machines.md) |
| **Associative / Content-Addressable** | Parallel execution driven by value matching on content-addressable arrays. Operations are executed simultaneously on matched locations without address decoding. | - [Associative Processors & Content-Addressable Computing](excavations/associative-processors.md) |
| **Spatial / Grid Computing** | Hardware logic and routing paths mapped physically to a static grid. No global ALU or instruction fetch bottleneck. | - [Cellular Automata Hardware](excavations/cellular-automata-hardware.md)<br>- [Explicit Data Graph Execution (EDGE) & The TRIPS Architecture](excavations/edge-architecture.md)<br>- [Systolic Arrays](excavations/systolic-arrays.md)<br>- [The MIT J-Machine](excavations/j-machine.md)<br>- [Wafer-Scale Integration](excavations/wafer-scale-integration.md) |
| **Massively Parallel SIMD** | Tens of thousands of simple processing elements executing a single instruction stream in lockstep. | - [Connection Machine](excavations/connection-machine.md)<br>- [Vector Supercomputing](excavations/vector-supercomputing.md) |
| **Analog / Continuous** | Solving math models directly via continuous physical phenomena (voltages, currents, fluid flow) instead of discrete bits. | - [Analog Computing](excavations/analog-computing.md)<br>- [Stochastic Computing](excavations/stochastic-computing.md)<br>- [Balanced Ternary](excavations/balanced-ternary.md) (ternary logic scaling)<br>- [Residue Number System (RNS)](excavations/residue-number-system.md) (carry-free modular channels) |
| **Photonic / Optical** | Using light propagation, interference, and wavelength division multiplexing to perform matrix operations. | - [Optical Computing](excavations/optical-computing.md) |
| **Biological / Molecular** | Leveraging DNA hybridization, enzymatic reactions, or bacterial states for massively parallel computing. | - [Molecular & Biocomputing](excavations/molecular-biocomputing.md) |
| **Logical & Inference Engine** | Evaluating rules, forward/backward chaining, and symbolic facts natively. | - [Symbolic AI](excavations/symbolic-ai.md) |
| **Associative Hypertext** | Graph-structured, bi-directional versioned information retrieval. | - [Project Xanadu](excavations/project-xanadu.md) |
| **VLIW / EPIC** | Multi-issue execution where the compiler explicitly schedules and bundles instructions for parallel pipelines. | - [VLIW / EPIC Architectures](excavations/vliw-epic.md) |
| **Reversible Logic** | Information-preserving gates that compute bijectively to prevent thermodynamic energy dissipation. | - [Reversible Computing](excavations/reversible-computing.md) |
| **Neuromorphic / Spiking** | Asynchronous, event-driven spike-routing microarchitectures modeling biological brain structures. | - [Neuromorphic Hardware](excavations/neuromorphic-hardware.md) |
| **Superconducting & Cryogenic** | Single Flux Quantum (SFQ) logic operating at extremely high gigahertz frequencies at cryogenic temperatures. | - [Superconducting & Cryogenic Microarchitectures](excavations/superconducting-cryogenic.md) |

---

## 2. Index by Memory & Protection Model

How does the system partition memory, enforce safety, and protect system integrity?

| Memory & Protection Model | Key Mechanism | Mapped Excavations |
|----------------------------|---------------|---------------------|
| **Hardware Capabilities & Descriptors** | Unforgeable pointers and descriptors containing base/bound and permissions enforced at register and ALU levels. | - [Burroughs Large Systems](excavations/burroughs-large-systems.md)<br>- [Capability Systems](excavations/capability-systems.md)<br>- [Intel iAPX 432](excavations/intel-iapx-432.md) |
| **[Tagged Memory](GLOSSARY.md)** | Extra hardware metadata bits on every word in RAM indicating data type, restricting invalid pointer arithmetic or data execution. | - [Burroughs Large Systems](excavations/burroughs-large-systems.md)<br>- [Graph Reduction Architectures & Functional Hardware](excavations/graph-reduction-machines.md)<br>- [Lisp Machines](excavations/lisp-machines.md)<br>- [Intel iAPX 432](excavations/intel-iapx-432.md)<br>- [The MIT J-Machine](excavations/j-machine.md)<br>- [Symbolic AI](excavations/symbolic-ai.md) (types/symbols) |
| **Associative / Content-Addressable Memory** | Memory queried and written in parallel by content match values rather than physical address decoders, completely bypassing the location boundaries. | - [Associative Processors & Content-Addressable Computing](excavations/associative-processors.md) |
| **[Hierarchical Ring Protection](GLOSSARY.md)** | Concentric rings of hardware privilege (e.g., Rings 0–3) preventing direct access to more privileged supervisor segments. | - [Multics](excavations/multics.md) |
| **Single-Level Store (SLS)** | The operating system abstracts memory and secondary storage into a single, flat, persistent virtual address space. | - [Multics](excavations/multics.md) |
| **Virtual Machine / Language-Safe Sandbox** | Enforcing type-safety and isolation inside a managed runtime environment or interpreter instead of hardware. | - [Apple: The Integrated Platform Surface](excavations/apple.md) (iOS Sandbox / ARC)<br>- [Inferno](excavations/inferno.md) (Dis VM)<br>- [Linux: The Ubiquitous Substrate](excavations/linux.md) (Namespaces / cgroups / eBPF VM)<br>- [Microsoft: The Platform Machine](excavations/microsoft.md) (.NET CLR)<br>- [OpenAI: The Model-as-Platform Substrate](excavations/openai.md) (ChatML, Stateful Thread Sandbox)<br>- [Smalltalk](excavations/smalltalk.md) ([Smalltalk](excavations/smalltalk.md) Image)<br>- [Lisp Machines](excavations/lisp-machines.md) (Lisp environment) |
| **Flat / Unprotected Memory** | Minimal or no hardware separation between processes or kernel. Designed for absolute raw speed or embedded simplicity. | - [Asynchronous Microprocessors](excavations/asynchronous-processors.md)<br>- [Stack Machines](excavations/stack-machines.md)<br>- [Stochastic Computing](excavations/stochastic-computing.md)<br>- [Transputers](excavations/transputers.md)<br>- [Balanced Ternary](excavations/balanced-ternary.md)<br>- [EBCDIC (Extended Binary Coded Decimal Interchange Code)](excavations/ebcdic.md)<br>- [Residue Number System (RNS)](excavations/residue-number-system.md) |
| **Bi-Directional Graph Address Space** | Graph-structured document fragments addressed via un-breakable dynamic spans. | - [Project Xanadu](excavations/project-xanadu.md) |

---

## 3. Index by Concurrency & Communication Model

How do independent execution units coordinate and share information?

| Concurrency Model | Coupling & Communication Style | Mapped Excavations |
|-------------------|--------------------------------|---------------------|
| **[Synchronous CSP Channels](GLOSSARY.md)** | Point-to-point, unbuffered synchronous channel messaging forcing deterministic synchronization. | - [Occam](excavations/occam.md)<br>- [Transputers](excavations/transputers.md) |
| **Asynchronous Message Passing** | Dynamic, uncoordinated message queues at the operating system or runtime layer. | - [Apple: The Integrated Platform Surface](excavations/apple.md) (Cocoa / Runloops / Mach ports)<br>- [BeOS / Haiku](excavations/beos-haiku.md) (Ports)<br>- [Linux: The Ubiquitous Substrate](excavations/linux.md) (Sockets / netlink / IPC)<br>- [Microsoft: The Platform Machine](excavations/microsoft.md) (COM / DCOM / Windows Messaging)<br>- [OpenAI: The Model-as-Platform Substrate](excavations/openai.md) (Stateful Threads / Tool-Use Runs)<br>- [Plan 9](excavations/plan-9.md) ([9P protocol](GLOSSARY.md))<br>- [Inferno](excavations/inferno.md) ([Styx protocol](GLOSSARY.md))<br>- [The MIT J-Machine](excavations/j-machine.md) ([Active Messages](GLOSSARY.md)) |
| **Object-Oriented Dynamic Messaging** | Virtual machine dynamic dispatch and runtime messaging between objects. | - [Smalltalk](excavations/smalltalk.md)<br>- [Intel iAPX 432](excavations/intel-iapx-432.md) |
| **Massively Parallel SIMD / Lock-Step** | Synchronous, centralized clock-driven step-by-step broadcast of instruction execution to an array. | - [Connection Machine](excavations/connection-machine.md)<br>- [Vector Supercomputing](excavations/vector-supercomputing.md)<br>- [Systolic Arrays](excavations/systolic-arrays.md)<br>- [Associative Processors & Content-Addressable Computing](excavations/associative-processors.md)<br>- [Stochastic Computing](excavations/stochastic-computing.md) |
| **Decentralized Local Interaction** | No global communication or clock synchronization; grid updates are entirely local and parallel. | - [Cellular Automata Hardware](excavations/cellular-automata-hardware.md) |
| **Shared Memory Multiprocessing** | Synchronous access to global memory segments managed by semaphores, lock instructions, or segment attributes. | - [Multics](excavations/multics.md) |
| **Parallel Graph Reduction** | Concurrent rewriting of a shared expression graph using distributed active packet/node pools and lock-free synchronization. | - [Graph Reduction Architectures & Functional Hardware](excavations/graph-reduction-machines.md) |
| **[Generative Communication](GLOSSARY.md)** | Coordinate-free, associative, time-and-space decoupled communication via a shared multi-set pool. | - [Linda Tuple Spaces](excavations/linda-tuple-spaces.md) |
| **Bi-Directional Hyperlink Coordination** | Structuring parallel synchronization as bidirectional links over versioned publication graphs. | - [Project Xanadu](excavations/project-xanadu.md) |
| **Rule-Based Inference** | Concurrency controlled by logical implication and dynamic resolution trees. | - [Symbolic AI](excavations/symbolic-ai.md) |
| **Symmetric Math Logic** | Balancing concurrency through sign-bit-free mathematical trits or independent, carry-free modular channels. | - [Balanced Ternary](excavations/balanced-ternary.md)<br>- [Residue Number System (RNS)](excavations/residue-number-system.md) |

---

## Summary Insights

Comparing systems along these architectural axes reveals deep engineering lineages:
1. **The Safe Systems Lineage**: *Burroughs* $\rightarrow$ *[Intel iAPX 432](excavations/intel-iapx-432.md)* $\rightarrow$ *[Lisp Machines](excavations/lisp-machines.md)* $\rightarrow$ *[Capability Systems](excavations/capability-systems.md) (CHERI)*. This path favors hardware-enforced type safety and fine-grained capabilities over general-purpose performance.
2. **The Spatial Data-Parallel Lineage**: *[Systolic Arrays](excavations/systolic-arrays.md)* $\rightarrow$ *[Connection Machine](excavations/connection-machine.md)* $\rightarrow$ *[Dataflow Computing](excavations/dataflow-computing.md)* $\rightarrow$ *Associative Processors* $\rightarrow$ *[Stochastic Computing](excavations/stochastic-computing.md)* $\rightarrow$ *FPGAs / Modern AI accelerators (TPUs / PIM)*. This line bypasses the sequential program-counter paradigm to unlock massive spatial and in-memory throughput.
3. **The Distributed Channels Lineage**: *CSP (Hoare)* $\rightarrow$ *[occam](excavations/occam.md)* $\rightarrow$ *[Transputers](excavations/transputers.md)* $\rightarrow$ *Go (channels) / Erlang (actor passing)*. This path proves that message passing can eliminate shared-memory concurrency hazards.
4. **The Distributed Resource Namespace Lineage**: *[Plan 9](excavations/plan-9.md) / Styx* $\rightarrow$ *[Inferno](excavations/inferno.md) / Limbo* $\rightarrow$ *Distributed Object-Cap Systems (KeyKOS / CapROS / CHERI)*. This lineage maps all network and execution resources to process-private file trees to decouple host-level systems from physical network topography.
5. **The Physical & Thermodynamic Lineage**: *[Analog Computing](excavations/analog-computing.md)* $\rightarrow$ *[Optical Computing](excavations/optical-computing.md)* $\rightarrow$ *[Reversible Computing](excavations/reversible-computing.md) (uncomputation)* $\rightarrow$ *Superconducting & Cryogenic (SFQ)*. This lineage bypasses standard room-temperature silicon CMOS charging constraints, utilizing continuous physics, coherent wave interference, or macroscopic quantum phase slips to compute near or below the traditional Landauer energy limits at speeds up to $500 \text{ GHz}$.

---

## Revival Readiness Scorecard Integration

To see how these lineages perform under modern design conditions, consult the [Modern Revival Readiness Scorecard](modern-relevance/revival-readiness.md), which scores each lineage against active modern hardware, software, and AI design constraints.
