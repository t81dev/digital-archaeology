# Glossary & Abstraction Taxonomy

> **A reference guide to forgotten computing terminology, architectural paradigms, and a taxonomy of historically sidelined abstractions.**

This document provides a conceptual glossary of terms from across the excavations, alongside a taxonomy of computing abstractions. It is designed to help researchers, engineers, and future AI systems navigate the non-standard architectures of computing history.

---

## Part 1: Glossary of Forgotten Computing Terms

### #
* **9P Protocol**: A distributed resource sharing protocol designed for Plan 9 where every system resource (including files, devices, memory, and processes) is represented as a file and accessed via a standardized, network-transparent set of message transactions.
  * *See excavation*: [Plan 9](excavations/plan-9.md)

### A
* **Actor Model**: A mathematical model of concurrent computation where the universal primitive is the *actor*. Actors can make local decisions, create more actors, send messages, and designate how to respond to the next message. Unlike the Von Neumann model, communication is asynchronous and there is no shared state.
  * *See excavation*: [Smalltalk](excavations/smalltalk.md)
* **Analog Computing**: Computation that utilizes continuous physical phenomena (e.g., electrical voltage, mechanical rotation, fluid flow) to model the problem being solved, bypassing the discretization of binary systems.
  * *See excavation*: [Analog Computing](excavations/analog-computing.md)

### B
* **Balanced Ternary**: A base-3 positional numeral system using the trits $-1$ (represented as `T`), $0$, and $+1$ (represented as `1`). It eliminates the need for a separate sign bit, simplifies arithmetic circuits, and possesses a superior radix economy compared to binary.
  * *See excavation*: [Balanced Ternary](excavations/balanced-ternary.md)
* **Bi-Directional Hypermedia**: A network publishing and hypertext model where hyperlinks are inherently two-way and un-breakable, enabling side-by-side visual comparison, micro-transactions, and deep version tracking.
  * *See excavation*: [Project Xanadu](excavations/project-xanadu.md)

### C
* **Capability-Based Security**: An access control model where processors or operating systems reference unforgeable keys called *capabilities*. A capability contains both a memory range (bounds) and specific permissions (read, write, execute), preventing buffer overflows and enforcing micro-segmentation at the hardware level.
  * *See excavation*: [Capability Systems](excavations/capability-systems.md)
* **Cellular Automata (CA) Hardware**: Spatial computing grids where cells update their state in parallel based on localized transition rules. This model completely bypasses the central ALU bottleneck of Von Neumann architectures.
  * *See excavation*: [Cellular Automata Hardware](excavations/cellular-automata-hardware.md)
* **Communicating Sequential Processes (CSP)**: A formal language and mathematical model (introduced by Tony Hoare) for concurrent systems where processes communicate solely through synchronous, unbuffered/buffered channels.
  * *See excavation*: [Occam](excavations/occam.md), [Transputers](excavations/transputers.md)
* **Continuous Physical Modeling**: Solving differential equations by mapping physical system variables (e.g., fluid dynamics, acoustics) directly onto equivalent physical currents or voltages in analog circuits.
  * *See excavation*: [Analog Computing](excavations/analog-computing.md)

### D
* **Dataflow Architecture**: A non-von Neumann computer architecture where the execution order of instructions is not controlled by a program counter, but is determined dynamically by the availability of data (tokens) at instruction inputs.
  * *See excavation*: [Dataflow Computing](excavations/dataflow-computing.md)
* **Descriptor-Based Memory**: A precursor to capabilities where memory addresses are accessed indirectly through a hardware-recognized data structure (descriptor) containing base, limit, and type information.
  * *See excavation*: [Burroughs Large Systems](excavations/burroughs-large-systems.md)
* **Dynamic Token-Matching**: An execution model in dataflow processors where data packets (tokens) carry tag headers specifying their destination, iteration context, and call frame, allowing out-of-order, parallel execution of loops and functions.
  * *See excavation*: [Dataflow Computing](excavations/dataflow-computing.md)

### E
* **Explicitly Parallel Instruction Computing (EPIC)**: An instruction set philosophy (co-developed by HP and Intel for Itanium) where the compiler explicitly bundles instructions that can be executed in parallel, moving the complex scheduling logic from hardware to the compiler.
  * *See excavation*: [VLIW / EPIC Architectures](excavations/vliw-epic.md)

### G
* **Generative Communication**: A parallel coordination model pioneered by Linda where processes communicate asynchronously and anonymously by depositing un-addressed, typed data tuples into a globally shared, associative space, which other processes can query by structural pattern matching.
  * *See excavation*: [Linda Tuple Spaces](excavations/linda-tuple-spaces.md)

### L
* **Landauer's Limit**: A physical limit stating that any logically irreversible manipulation of information, such as erasing a bit, must dissipate a minimum amount of heat ($k_B T \ln 2$).
  * *See excavation*: [Reversible Computing](excavations/reversible-computing.md)

### M
* **Massively Parallel Processing (MPP)**: A computer architecture that coordinates thousands of independent, single-bit processors in a tightly integrated network to perform highly fine-grained parallel computation.
  * *See excavation*: [Connection Machine](excavations/connection-machine.md)
* **Micropipelines**: A modular, clockless architecture framework that utilizes localized transition-signaling handshakes to synchronize data flow between pipeline stages.
  * *See excavation*: [Asynchronous Microprocessors](excavations/asynchronous-processors.md)
* **Mixed-Radix Arithmetic**: Positional numeral systems where the base (radix) varies from one digit position to another.
  * *See modern relevance*: [Mixed-Radix & Alternative Number Systems](modern-relevance/mixed-radix.md)
* **Molecular/Biocomputing**: A non-silicon hardware paradigm that utilizes biological molecules, DNA strands, or enzymatic chemical reactions to store data and execute highly parallel combinatorial logic.
  * *See excavation*: [Molecular & Biocomputing](excavations/molecular-biocomputing.md)
* **Muller C-element**: A fundamental state-retaining logical component in asynchronous control circuits that acts as an "event AND-gate"—its output transitions only when all of its inputs have transitioned to match.
  * *See excavation*: [Asynchronous Microprocessors](excavations/asynchronous-processors.md)

### N
* **Neuromorphic Hardware**: Silicon architectures designed to mimic the neural structures of the brain, utilizing asynchronous, event-driven spiking neural networks and in-memory computation.
  * *See excavation*: [Neuromorphic Hardware](excavations/neuromorphic-hardware.md)

### O
* **Optical Computing**: A hardware paradigm using light waves (photons) instead of electrical currents (electrons) to perform logic operations, leveraging wave interference, spatial division multiplexing, and sub-nanosecond matrix-vector multiplication.
  * *See excavation*: [Optical Computing](excavations/optical-computing.md)

### P
* **Pervasive Multithreading**: An operating system design featuring granular, per-thread scheduling, heavy optimization for symmetric multiprocessing (SMP), and pervasive multi-threading across both the kernel and media-rich user-space applications.
  * *See excavation*: [BeOS / Haiku](excavations/beos-haiku.md)

* **Object-Capability Model**: A software design pattern that combines object-oriented encapsulation with capability-based security. An object reference *is* the unforgeable authority to perform actions on that object.
  * *See excavation*: [Intel iAPX 432](excavations/intel-iapx-432.md)

### R
* **Radix Economy**: A mathematical measure of the efficiency of representing numbers in a given base, defined as $R \times \lfloor \log_R(N) + 1 \rfloor$ for base $R$ and maximum value $N$. It is mathematically optimized at the transcendental base $e \approx 2.718$, which makes base 3 (ternary) more efficient than base 2 (binary).
  * *See excavation*: [Balanced Ternary](excavations/balanced-ternary.md)
* **Reversible Computing**: A paradigm where logic gates perform bijective (one-to-one) mapping between inputs and outputs, allowing computation to run backward and theoretically bypassing Landauer's thermodynamic limit.
  * *See excavation*: [Reversible Computing](excavations/reversible-computing.md)

### S
* **Single-Level Store (SLS)**: A memory management architecture where all secondary storage (such as disk drives) is integrated into a single, flat, virtually-addressed main memory space, completely eliminating the user-level distinction between file systems and RAM.
  * *See excavation*: [Multics](excavations/multics.md)
* **Spatial Computing (Hardware)**: Architectures where software logic is mapped directly onto a physical grid of processing elements with localized communication channels (e.g., FPGAs, Systolic Arrays, Cellular Automata), removing global bus bottlenecks.
  * *See excavation*: [Systolic Arrays](excavations/systolic-arrays.md)
* **Stack Machine**: A processor architecture that uses a hardware evaluation stack rather than general-purpose registers to execute zero-operand instructions.
  * *See excavation*: [Stack Machines](excavations/stack-machines.md)
* **Styx Protocol**: A network protocol derived from 9P, serving as the universal communication interface in the Inferno operating system to expose system services, devices, and files transparently over public networks.
  * *See excavation*: [Inferno](excavations/inferno.md)
* **Superconducting / Cryogenic Computing**: A high-performance hardware paradigm operating at cryogenic temperatures, using Josephson junctions and Single Flux Quantum (SFQ) logic to achieve ultra-high clock frequencies and near-zero power dissipation.
  * *See excavation*: [Superconducting & Cryogenic Microarchitectures](excavations/superconducting-cryogenic.md)
* **Symbolic AI**: An approach to artificial intelligence based on high-level, human-readable symbols, formal logic, and rule-based inference engines.
  * *See excavation*: [Symbolic AI](excavations/symbolic-ai.md)
* **Systolic Array**: A network of homogeneous, tightly-coupled processing elements that rhythmically compute and pass data through the system, optimizing matrix multiplication and other highly structured, compute-bound workloads.
  * *See excavation*: [Systolic Arrays](excavations/systolic-arrays.md)

### T
* **Tagged Memory**: A hardware mechanism where every word in memory is accompanied by a few extra non-addressable bits (tags) indicating its data type (e.g., integer, float, code pointer, capability), allowing hardware to prevent type safety violations and unauthorized execution.
  * *See excavation*: [Lisp Machines](excavations/lisp-machines.md)
* **Transition Signaling (2-Phase Handshaking)**: A clockless communication protocol where any voltage transition (either low-to-high or high-to-low) represents a control event, enabling high-speed handshake transactions with minimal signal lines and state changes.
  * *See excavation*: [Asynchronous Microprocessors](excavations/asynchronous-processors.md)
* **Tuple Space**: A persistent, associative, multi-set memory pool serving as the central coordination medium in generative communication. It stores both passive data tuples and active process tuples.
  * *See excavation*: [Linda Tuple Spaces](excavations/linda-tuple-spaces.md)

### V
* **Vector Processing**: A processor design that executes a single instruction on a collection of one-dimensional arrays of data (vectors) using pipelined functional units, optimizing high-throughput scientific workloads.
  * *See excavation*: [Vector Supercomputing](excavations/vector-supercomputing.md)
* **Very Long Instruction Word (VLIW)**: A processor design where the compiler groups independent, parallel operations into a single, very wide instruction word, relying on compile-time analysis rather than dynamic out-of-order execution hardware.
  * *See excavation*: [VLIW / EPIC Architectures](excavations/vliw-epic.md)
* **Von Neumann Bottleneck**: The throughput limitation on computer systems caused by the physical separation of the central processing unit and memory, requiring all instruction and data transfers to share a single bus.
  * *See modern relevance*: [AI & Hardware Bottlenecks](modern-relevance/ai.md)

### W
* **Wafer-Scale Integration (WSI)**: An advanced semiconductor manufacturing paradigm that builds an entire digital system (incorporating multiple processor nodes, memory blocks, and interconnect networks) on a single, uncut silicon wafer, completely bypassing chip-packaging boundaries.
  * *See excavation*: [Wafer-Scale Integration](excavations/wafer-scale-integration.md)

---

## Part 2: A Taxonomy of Forgotten Abstractions

Digital Archaeology categorizes forgotten concepts not by their historical date, but by the architectural *abstractions* they introduced. Below is the structured classification framework.

```
                  ┌───────────────────────────────┐
                  │      Abstractions Class       │
                  └───────────────┬───────────────┘
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│    Execution     │    │     Memory &     │    │   Concurrency    │
│    & Control     │    │    Protection    │    │  & Communication │
└────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
         ├─ Dataflow             ├─ Capabilities         ├─ CSP Channels
         ├─ Stack evaluation     ├─ Tagged Memory        ├─ Actor Messaging
         ├─ Spatial Routing      ├─ Single-Level Store   ├─ Massively Parallel
         └─ Analog/Continuous    └─ Protection Rings     └─ Decentralized CA
```

### 1. Execution & Control Flow Abstractions

These models depart from standard sequential, instruction-pointer-driven (von Neumann) execution.

* **Dataflow / Token Matching**: Execution is purely event-driven and parallel. Operations execute as soon as their inputs are physically routed to them.
  * *Example*: [Dataflow Computing](excavations/dataflow-computing.md)
* **Zero-Operand Stack Evaluation**: Instructions operate implicitly on a hardware evaluation stack, eliminating register specifiers from the instruction set encoding and simplifying compiler code generation.
  * *Example*: [Stack Machines](excavations/stack-machines.md), [Burroughs Large Systems](excavations/burroughs-large-systems.md)
* **Spatial & Grid Routing**: Processing is mapped onto physical coordinate grids of simple ALUs. Software is compiled as spatial configurations and data routing pathways rather than sequential code.
  * *Example*: [Systolic Arrays](excavations/systolic-arrays.md), [Cellular Automata Hardware](excavations/cellular-automata-hardware.md)
* **Continuous Analog Scaling**: Solving mathematical systems through continuous physical interactions (voltages, light waves, chemical concentrations) rather than discrete digital clock cycles.
  * *Example*: [Analog Computing](excavations/analog-computing.md), [Optical Computing](excavations/optical-computing.md), [Molecular & Biocomputing](excavations/molecular-biocomputing.md)
* **Self-Timed & Asynchronous Control**: Operations and pipeline stages synchronize locally via request-acknowledge handshake signals, executing at the natural physical speed of physical gates rather than relying on a global clock tree.
  * *Example*: [Asynchronous Microprocessors](excavations/asynchronous-processors.md), [Neuromorphic Hardware](excavations/neuromorphic-hardware.md)

### 2. Memory & Protection Abstractions

These abstractions define how memory is organized, addressed, and secured against unauthorized access or structural corruption.

* **Object Capabilities & Descriptors**: Moving access control from software operating system layers to hardware unforgeable tokens. If a processor does not possess the physical capability token, it is physically impossible to construct the memory address.
  * *Example*: [Capability Systems](excavations/capability-systems.md), [Intel iAPX 432](excavations/intel-iapx-432.md)
* **Tagged Memory**: Enforcing data type safety in hardware. An integer can never be executed as instruction code, and a data word can never be treated as a pointer, eliminating entire classes of exploit vectors.
  * *Example*: [Lisp Machines](excavations/lisp-machines.md), [Burroughs Large Systems](excavations/burroughs-large-systems.md)
* **Single-Level Store (SLS)**: Removing the mental and structural wall between volatile memory (RAM) and non-volatile storage (Disk). Everything exists inside a singular, persistent, universally addressable space.
  * *Example*: [Multics](excavations/multics.md)
* **Hierarchical Ring Protection**: Defining access control as concentric rings of privilege. Inner rings (e.g., Ring 0) have full access, while outer rings must cross formal gates to request services, preventing privilege escalation.
  * *Example*: [Multics](excavations/multics.md)

### 3. Concurrency & Communication Abstractions

These abstractions define how parallel computational threads or systems coordinate, synchronize, and exchange information.

* **Synchronous CSP Channels**: Processes synchronize and communicate exclusively via unbuffered, blocking channels. This forces deterministic execution and prevents race conditions without relying on locks or semaphores.
  * *Example*: [Transputers](excavations/transputers.md), [Occam](excavations/occam.md)
* **Asynchronous Actor Messaging**: Independent processes that communicate exclusively via dynamic, asynchronous messages, avoiding shared-state corruption and making distributed computing identical to local computing.
  * *Example*: [Smalltalk](excavations/smalltalk.md)
* **Distributed Service Protocols (Everything is a File/Service)**: Standardizing all system resources (CPUs, screens, networks, configurations) under a unified, simple representation protocol (9P) accessed over a network.
  * *Example*: [Plan 9](excavations/plan-9.md), [Inferno](excavations/inferno.md)
* **Massively Parallel SIMD Hypercubes**: Structuring tens of thousands of single-bit processors in a hypercube network, executing operations in lock-step to solve massive-scale parallel data problems.
  * *Example*: [Connection Machine](excavations/connection-machine.md)
* **Generative Tuple Spaces**: Decoupling communication completely in both space (anonymous) and time (asynchronous) via a shared, content-addressable multi-set data pool.
  * *Example*: [Linda Tuple Spaces](excavations/linda-tuple-spaces.md)
