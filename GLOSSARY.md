# Glossary & Abstraction Taxonomy

> **A reference guide to forgotten computing terminology, architectural paradigms, and a taxonomy of historically sidelined abstractions.**

This document provides a conceptual glossary of terms from across the excavations, alongside a taxonomy of computing abstractions. It is designed to help researchers, engineers, and future AI systems navigate the non-standard architectures of computing history.

---

## Part 1: Glossary of Forgotten Computing Terms

### #
* **9P Protocol**: A distributed resource sharing protocol designed for [Plan 9](excavations/plan-9.md) where every system resource (including files, devices, memory, and processes) is represented as a file and accessed via a standardized, network-transparent set of message transactions.
  * *See excavation*: [Plan 9](excavations/plan-9.md)

### A
* **Apple Silicon**: A lineage of custom-designed, ARM-based System-on-Chip (SoC) architectures integrating high-bandwidth Unified Memory, Secure Enclave processors, and dynamic matrix-multiplication co-processors tightly integrated with the system compilers.
  * *See excavation*: [Apple: The Integrated Platform Surface](excavations/apple.md)
* **ABI (Application Binary Interface)**: The low-level interface between compiled binary user-space software and the operating system kernel, encompassing registers, calling conventions, and system calls.
  * *See excavation*: [Linux: The Ubiquitous Substrate](excavations/linux.md)

### A
* **Active Messages**: A communication paradigm for high-performance parallel systems where each message packet contains in its header the address of an execution handler. Upon arrival, the handler executes immediately using the packet's payload as arguments, bypassing operating system scheduling and context-switching overhead.
  * *See excavation*: [The MIT J-Machine](excavations/j-machine.md)
* **Actor Model**: A mathematical model of concurrent computation where the universal primitive is the *actor*. Actors can make local decisions, create more actors, send messages, and designate how to respond to the next message. Unlike the Von Neumann model, communication is asynchronous and there is no shared state.
  * *See excavation*: [Smalltalk](excavations/smalltalk.md)
* **[Analog Computing](excavations/analog-computing.md)**: Computation that utilizes continuous physical phenomena (e.g., electrical voltage, mechanical rotation, fluid flow) to model the problem being solved, bypassing the discretization of binary systems.
  * *See excavation*: [Analog Computing](excavations/analog-computing.md)
* **Associative Processing**: A parallel computing paradigm where data is accessed and operated on by content (associative matching of data values) rather than by hardware memory addresses.
  * *See excavation*: [Associative Processors](excavations/associative-processors.md)

### B
* **[Balanced Ternary](excavations/balanced-ternary.md)**: A base-3 positional numeral system using the trits $-1$ (represented as `T`), $0$, and $+1$ (represented as `1`). It eliminates the need for a separate sign bit, simplifies arithmetic circuits, and possesses a superior radix economy compared to binary.
  * *See excavation*: [Balanced Ternary](excavations/balanced-ternary.md)
* **Bi-Directional Hypermedia**: A network publishing and hypertext model where hyperlinks are inherently two-way and un-breakable, enabling side-by-side visual comparison, micro-transactions, and deep version tracking.
  * *See excavation*: [Project Xanadu](excavations/project-xanadu.md)
* **Bit-Serial Word-Parallel Execution**: An execution technique where operations are performed on one bit-slice of all words in memory simultaneously in parallel, typical of early associative processors like STARAN.
  * *See excavation*: [Associative Processors](excavations/associative-processors.md)

### C
* **[C++](excavations/cpp.md)**: A foundational systems programming language and computational lineage combining low-level machine control with user-defined abstractions via zero-overhead mechanisms, deterministic scope lifetimes (RAII), value semantics, compile-time template monomorphization, and ISO standardization governance.
  * *See excavation*: [C++: Zero-Overhead Abstraction & Deterministic Resource Control](excavations/cpp.md)
* **CUDA**: A parallel computing platform and programming model introduced by NVIDIA in 2006 that exposes GPUs for general-purpose computing using C/C++ language extensions, a grid/block/thread hierarchy, and driver/runtime APIs.
  * *See excavation*: [NVIDIA Architecture: The Programmable Parallel Substrate & CUDA Platform](excavations/nvidia.md)
* **cuDNN**: A software library of hand-optimized primitives for deep neural networks (convolutions, activations, normalizations, attention) that acts as the primary execution surface for AI frameworks on NVIDIA GPUs.
  * *See excavation*: [NVIDIA Architecture: The Programmable Parallel Substrate & CUDA Platform](excavations/nvidia.md)
* **CPUID**: An x86 assembly instruction that returns feature bitfields describing processor family, model, and supported ISA extensions (SSE, AVX, AMX, VT-x), enabling dynamic runtime vector fastpath dispatching.
  * *See excavation*: [Intel: The Architectural & Compatibility Substrate](excavations/intel.md)
* **Capability-Based Security**: An access control model where processors or operating systems reference unforgeable keys called *capabilities*. A capability contains both a memory range (bounds) and specific permissions (read, write, execute), preventing buffer overflows and enforcing micro-segmentation at the hardware level.
  * *See excavation*: [Capability Systems](excavations/capability-systems.md)
* **Coanda Effect**: The physical phenomenon where a fluid jet attaches itself to a nearby solid surface due to localized low-pressure bubbles created by entrainment. In pure fluidics, it provides the physical foundation for bistable state retention (flip-flops) and switching without moving parts.
  * *See excavation*: [Fluidic Logic Systems](excavations/fluidic-logic-systems.md)
* **Chinese Remainder Theorem (CRT)**: A mathematical theorem stating that any integer within a dynamic range can be uniquely reconstructed from its residues modulo a set of pairwise coprime moduli, providing the algebraic foundation of RNS.
  * *See excavation*: [Residue Number System (RNS)](excavations/residue-number-system.md)
* **Cellular Automata (CA) Hardware**: Spatial computing grids where cells update their state in parallel based on localized transition rules. This model completely bypasses the central ALU bottleneck of Von Neumann architectures.
  * *See excavation*: [Cellular Automata Hardware](excavations/cellular-automata-hardware.md)
* **Cursor IDE**: An AI-native software editing substrate forked from VS Code that integrates codebase vector/AST context assembly, spec-diff edit previews, fast speculative code application, and supervised workspace agent loops.
  * *See excavation*: [Cursor IDE: The AI-Native Editor Substrate & Agentic Workspace](excavations/cursor-ide.md)
* **Communicating Sequential Processes (CSP)**: A formal language and mathematical model (introduced by Tony Hoare) for concurrent systems where processes communicate solely through synchronous, unbuffered/buffered channels.
  * *See excavation*: [Occam](excavations/occam.md), [Transputers](excavations/transputers.md)
* **Chat Markup Language (ChatML)**: A structured role-based representation protocol that delimits user, system, and assistant messages inside explicit unforgeable boundary tokens to prevent prompt-injection attacks.
  * *See excavation*: [OpenAI: The Model-as-Platform Substrate](excavations/openai.md)
* **Component Object Model (COM)**: A language-agnostic binary interface standard enabling location-transparent object communication via structured virtual function table (vtable) layouts.
  * *See excavation*: [Microsoft: The Platform Machine](excavations/microsoft.md)
* **Content-Addressable Memory (CAM)**: A specialized computer memory that searches its entire contents in a single clock cycle and returns the address(es) where matching data is found.
  * *See excavation*: [Associative Processors](excavations/associative-processors.md)
* **Continuous Physical Modeling**: Solving differential equations by mapping physical system variables (e.g., fluid dynamics, acoustics) directly onto equivalent physical currents or voltages in analog circuits.
  * *See excavation*: [Analog Computing](excavations/analog-computing.md)
* **Choice Point**: A saved snapshot of the execution state of the Warren Abstract Machine, pushed onto the local stack before attempting alternative clauses in a nondeterministic logic predicate to support backtracking.
  * *See excavation*: [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)
* **Committed-Choice Concurrency**: A concurrent programming paradigm where nondeterminism is restricted (don't-care nondeterminism) so that execution permanently commits to the first clause whose guard conditions are satisfied, eliminating backtracking search in parallel environments.
  * *See excavation*: [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)

### D
* **Dataflow Architecture**: A non-von Neumann computer architecture where the execution order of instructions is not controlled by a program counter, but is determined dynamically by the availability of data (tokens) at instruction inputs.
  * *See excavation*: [Dataflow Computing](excavations/dataflow-computing.md)
* **Demand-Driven Evaluation**: An execution paradigm (also known as lazy evaluation or call-by-need) where an expression is evaluated only when its result is strictly required by another operation or output device, contrasting with data-driven (dataflow) or control-driven (von Neumann) execution.
  * *See excavation*: [Graph Reduction Architectures & Functional Hardware](excavations/graph-reduction-machines.md)
* **Descriptor-Based Memory**: A precursor to capabilities where memory addresses are accessed indirectly through a hardware-recognized data structure (descriptor) containing base, limit, and type information.
  * *See excavation*: [Burroughs Large Systems](excavations/burroughs-large-systems.md)
* **Dynamic Token-Matching**: An execution model in dataflow processors where data packets (tokens) carry tag headers specifying their destination, iteration context, and call frame, allowing out-of-order, parallel execution of loops and functions.
  * *See excavation*: [Dataflow Computing](excavations/dataflow-computing.md)
* **Dereferencing Chain**: A sequence of reference pointers that must be traversed dynamically to locate the canonical value or unbound state of a logic variable.
  * *See excavation*: [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)

### E
* **EBCDIC (Extended Binary Coded Decimal Interchange Code)**: An 8-bit character encoding family designed by IBM in 1963 for the System/360 architecture, combining mechanical zone and digit punch mappings from Herman Hollerith's card layouts, resulting in non-contiguous alphabet segments and unique sorting semantics.
  * *See excavation*: [EBCDIC](excavations/ebcdic.md)
* **Ebuild**: An executable package definition script written in Bash for [Gentoo](excavations/gentoo.md)'s Portage system, defining software lifecycle phases (`src_unpack`, `src_configure`, `src_compile`, `src_install`) and conditional dependencies.
  * *See excavation*: [Portage: Package Management as Policy-Constrained Recipe Execution](excavations/portage.md), [Gentoo](excavations/gentoo.md)
* **eBPF (Extended Berkeley Packet Filter)**: An in-kernel, register-based virtual machine and safe bytecode runtime executing verified programs dynamically inside the supervisor-mode event path of the Linux kernel.
  * *See excavation*: [Linux: The Ubiquitous Substrate](excavations/linux.md)
* **Execution Provider (EP)**: A pluggable compiler and driver adapter inside ONNX Runtime that intercepts, optimizes, and compiles subgraphs for specialized hardware backends (such as CUDA, TensorRT, and OpenVINO).
  * *See excavation*: [ONNX (Open Neural Network Exchange) & The Interoperability Lineage](excavations/onnx.md)
* **Explicit Data Graph Execution (EDGE)**: An alternative class of microprocessors that partition instructions into logically atomic blocks. Within each block, execution is dataflow-driven, with instructions routing operand tokens directly to their consumers over a physical spatial grid, completely bypassing centralized registers and rename tables.
  * *See excavation*: [Explicit Data Graph Execution (EDGE) & The TRIPS Architecture](excavations/edge-architecture.md)
* **Explicitly Parallel Instruction Computing (EPIC)**: An instruction set philosophy (co-developed by HP and Intel for Itanium) where the compiler explicitly bundles instructions that can be executed in parallel, moving the complex scheduling logic from hardware to the compiler.
  * *See excavation*: [VLIW / EPIC Architectures](excavations/vliw-epic.md)

### F
* **Fluidic Logic**: A computational and control paradigm that processes continuous or discrete information using the dynamics of fluid media directly within non-moving channels, relying on the Coanda effect, jet interaction, and laminar-to-turbulent transitions.
  * *See excavation*: [Fluidic Logic Systems](excavations/fluidic-logic-systems.md)

### G
* **Generative Communication**: A parallel coordination model pioneered by Linda where processes communicate asynchronously and anonymously by depositing un-addressed, typed data tuples into a globally shared, associative space, which other processes can query by structural pattern matching.
  * *See excavation*: [Linda Tuple Spaces](excavations/linda-tuple-spaces.md)
* **Gentoo**: A source-centric Linux distribution architecture and platform construction lineage that elevates compile-time feature selection (`USE` flags), executable package recipes (`ebuilds`), cascading profiles, version slotting (`SLOT`), and additive overlays into a first-class operating-system management paradigm.
  * *See excavation*: [Gentoo: Source-Based Distribution Architecture & Compile-Time Configuration](excavations/gentoo.md)
* **Google**: A multi-generational platform machine of scale that pioneered the concept of warehouse-scale computing, converting datacenter operational constraints into narrow, exportable software abstractions.
  * *See excavation*: [Google: The Platform Machine of Scale](excavations/google.md)
* **Google File System (GFS)**: A highly-scalable, fault-tolerant distributed file system designed to run on large clusters of commodity hardware, optimizing for append-only streaming workloads and multi-megabyte files.
  * *See excavation*: [Google: The Platform Machine of Scale](excavations/google.md)
* **Graph Reduction Machine**: A non-von Neumann computer architecture designed to natively execute pure functional programming languages. Instead of sequentially executing compiled assembly instructions, it represents programs as directed acyclic graphs in memory and executes them by repeatedly simplifying and rewriting reducible expressions (redexes) in-place.
  * *See excavation*: [Graph Reduction Architectures & Functional Hardware](excavations/graph-reduction-machines.md)
* **GGML**: A minimal, raw tensor and evaluation graph library written in plain C, designed to pre-allocate memory arenas topologically to perform high-performance neural network inference with zero dynamic memory allocation overhead.
  * *See excavation*: [llama.cpp](excavations/llama-cpp.md)
* **GGUF**: A unified, self-describing, and single-file model packaging format designed for memory-mapped (`mmap`) zero-copy loading of large neural weights and structured key-value metadata.
  * *See excavation*: [llama.cpp](excavations/llama-cpp.md)

### I
* **Intel**: A historical computational lineage whose artifacts include instruction-set architectures (x86, x86-64), microcode µop decoders, CPUID dynamic feature discovery, System Management Mode (SMM), platform chipsets, and long-lived binary compatibility contracts.
  * *See excavation*: [Intel: The Architectural & Compatibility Substrate](excavations/intel.md)
* **Integrated Platform Surface**: An architectural paradigm of hardware-software-distribution vertical integration where custom silicon, core operating system managers, dynamic runtimes, developer toolchains, and centralized monetization gates are co-designed as a single surface.
  * *See excavation*: [Apple: The Integrated Platform Surface](excavations/apple.md)
* **Intelligent Tracking Prevention (ITP)**: A client-side privacy architecture introduced in WebKit that integrates machine learning classification, double-keyed storage partitioning, and cookie expiration caps directly into network and storage execution paths.
  * *See excavation*: [Safari: The WebKit Engine Lineage & Platform Web Runtime Substrate](excavations/safari.md)

### J
* **J-Machine (Jellybean Machine)**: A fine-grained, massively parallel computer architecture that integrated a 3D wormhole-routing network, on-chip SRAM, and a message-driven processor on a single monolithic die to support low-latency active messages.
  * *See excavation*: [The MIT J-Machine](excavations/j-machine.md)

### K
* **KeyKOS**: A pioneering microkernel/nanokernel capability operating system implementing pure object-capabilities, fine-grained access control keys, dynamic factories, and continuous system-wide orthogonal persistence.
  * *See excavation*: [KeyKOS and the Nanokernel Capability Lineage](excavations/keykos-nanokernel-capabilities.md)

### L
* **Large Language Models (LLMs)**: A computational paradigm and execution substrate that converts statistical next-token prediction over transformer neural sequence architectures into a general-purpose soft interface layer over software systems, APIs, and accelerators.
  * *See excavation*: [Large Language Models](excavations/large-language-models.md)
* **Landauer's Limit**: A physical limit stating that any logically irreversible manipulation of information, such as erasing a bit, must dissipate a minimum amount of heat ($k_B T \ln 2$).
  * *See excavation*: [Reversible Computing](excavations/reversible-computing.md)
* **llama.cpp**: A highly optimized, dependency-free C/C++ inference runtime engine that popularized quantization-first execution, unified memory-bandwidth-aware model loading, and dynamic CPU-GPU offloading.
  * *See excavation*: [llama.cpp](excavations/llama-cpp.md)
* **Linear Feedback Shift Register (LFSR)**: A hardware-efficient shift register whose input bit is a linear function (typically XOR) of its previous states. In alternative architectures like [Stochastic Computing](excavations/stochastic-computing.md), LFSRs serve as compact, high-speed pseudo-random number generators.
  * *See excavation*: [Stochastic Computing](excavations/stochastic-computing.md)
* **Logarithmic Number System (LNS)**: An alternative real-number arithmetic representation that encodes values by their sign and the logarithm of their absolute value to a selected base. LNS simplifies multiplication, division, and exponentiation into simple fixed-point additions and subtractions while shifting the complexity bottleneck to non-linear addition/subtraction approximations and format conversions.
  * *See excavation*: [Logarithmic Number System (LNS)](excavations/logarithmic-number-system.md)

### M
* **Metal**: A low-overhead, explicit GPU command and resource architecture engineered by Apple to replace legacy OpenGL/OpenCL stacks with immutable Pipeline State Objects, thread-safe command encoding, explicit UMA memory storage modes, and TBDR rasterization integration across Apple platforms.
  * *See excavation*: [Apple Metal Architecture](excavations/apple-metal.md)
* **Metal Shading Language (MSL)**: A C++14-based graphics and compute shading language compiled ahead-of-time into LLVM bitcode (`.air`/`.metallib`) and specialized at runtime for Apple Silicon GPUs.
  * *See excavation*: [Apple Metal Architecture](excavations/apple-metal.md)
* **Mixed-Radix Conversion (MRC)**: A non-homogeneous weighted representation conversion algorithm used to decode Residue Number System values into a weighted format, facilitating sign detection and comparison.
  * *See excavation*: [Residue Number System (RNS)](excavations/residue-number-system.md)

### M
* **Massively Parallel Processing (MPP)**: A computer architecture that coordinates thousands of independent, single-bit processors in a tightly integrated network to perform highly fine-grained parallel computation.
  * *See excavation*: [Connection Machine](excavations/connection-machine.md)
* **Micropipelines**: A modular, clockless architecture framework that utilizes localized transition-signaling handshakes to synchronize data flow between pipeline stages.
  * *See excavation*: [Asynchronous Microprocessors](excavations/asynchronous-processors.md)
* **Mixed-Radix Arithmetic**: Positional numeral systems where the base (radix) varies from one digit position to another.
  * *See modern relevance*: [Mixed-Radix & Alternative Number Systems](modern-relevance/mixed-radix.md)
* **Molecular/Biocomputing**: A non-silicon hardware paradigm that utilizes biological molecules, DNA strands, or enzymatic chemical reactions to store data and execute highly parallel combinatorial logic.
  * *See excavation*: [Molecular & Biocomputing](excavations/molecular-biocomputing.md)
* **Meta-Object Compiler (moc)**: A domain-specific C++ code-generator pre-processor designed for Qt that parses class declarations containing `Q_OBJECT` macros to emit static C++ compilation units containing runtime reflection metadata tables, property introspection descriptions, and signal/slot dispatch functions.
  * *See excavation*: [Qt](excavations/qt.md)
* **Muller C-element**: A fundamental state-retaining logical component in asynchronous control circuits that acts as an "event AND-gate"—its output transitions only when all of its inputs have transitioned to match.
  * *See excavation*: [Asynchronous Microprocessors](excavations/asynchronous-processors.md)

### N
* **Netscape**: A foundational web runtime lineage whose artifacts transformed the browser from a static hypertext viewer into a programmable, securable application platform through JavaScript, NPAPI plugins, SSL/TLS, HTTP Cookies, and the Mozilla open-source transition.
  * *See excavation*: [Netscape](excavations/netscape.md)
* **NPAPI (Netscape Plugin Application Programming Interface)**: A low-level C-ABI function pointer jump-table interface (`NPP_`/`NPN_`) enabling third-party compiled shared libraries (Flash, Java Applets, QuickTime) to render directly inside browser document bounding boxes and stream media.
  * *See excavation*: [Netscape](excavations/netscape.md)
* **NVIDIA**: A computational lineage whose artifacts include programmable GPU architectures, Streaming Multiprocessors, SIMT execution, the CUDA platform, NVLink interconnects, and Tensor Core matrix acceleration engines.
  * *See excavation*: [NVIDIA Architecture: The Programmable Parallel Substrate & CUDA Platform](excavations/nvidia.md)
* **NVLink**: A high-speed point-to-point and crossbar (NVSwitch) interconnect fabric engineered by NVIDIA to bypass PCIe bottlenecks and enable high-bandwidth inter-GPU memory sharing across multi-GPU data-center clusters.
  * *See excavation*: [NVIDIA Architecture: The Programmable Parallel Substrate & CUDA Platform](excavations/nvidia.md)
* **[Neuromorphic Hardware](excavations/neuromorphic-hardware.md)**: Silicon architectures designed to mimic the neural structures of the brain, utilizing asynchronous, event-driven spiking neural networks and in-memory computation.
  * *See excavation*: [Neuromorphic Hardware](excavations/neuromorphic-hardware.md)

### O
* **ONNX (Open Neural Network Exchange)**: An open-standard intermediate representation format and runtime specification for deep learning graphs, enabling trained models to migrate across training frameworks and deployment environments.
  * *See excavation*: [ONNX (Open Neural Network Exchange) & The Interoperability Lineage](excavations/onnx.md)
* **Opset (Operator Set)**: A mathematically strict, versioned library of neural network operators defined inside ONNX, ensuring backward-compatible execution semantics of portable graphs over time.
  * *See excavation*: [ONNX (Open Neural Network Exchange) & The Interoperability Lineage](excavations/onnx.md)
* **[Optical Computing](excavations/optical-computing.md)**: A hardware paradigm using light waves (photons) instead of electrical currents (electrons) to perform logic operations, leveraging wave interference, spatial division multiplexing, and sub-nanosecond matrix-vector multiplication.
  * *See excavation*: [Optical Computing](excavations/optical-computing.md)
* **OpenAI API**: A stable, remote remote intelligence service that platformizes large-scale learned weights into versioned, billable completions, chat turns, and stateful multi-step agent run loops.
  * *See excavation*: [OpenAI: The Model-as-Platform Substrate](excavations/openai.md)

### Q
* **QML (Qt Modeling Language)**: An object-oriented declarative programming language running over a reactive property binding engine and a hardware-accelerated scene graph (OpenGL/Vulkan/Metal), decoupling presentation UI layout from underlying C++ application backends.
  * *See excavation*: [Qt](excavations/qt.md)
* **Qt Platform Abstraction (QPA)**: A plugin-based windowing and rendering abstraction layer in Qt that isolates GUI application code from platform-specific OS windowing handles (Win32, Cocoa, X11, Wayland, or direct framebuffers).
  * *See excavation*: [Qt](excavations/qt.md)

### P
* **Pervasive Multithreading**: An operating system design featuring granular, per-thread scheduling, heavy optimization for symmetric multiprocessing (SMP), and pervasive multi-threading across both the kernel and media-rich user-space applications.
  * *See excavation*: [BeOS / Haiku](excavations/beos-haiku.md)
* **Portage**: The Python and Bash-based package management and dependency resolution engine created for Gentoo, incorporating constraint graph solvers, version slotting, cascading profiles, LD_PRELOAD build sandboxing, and an on-disk plain-text Var Database (`/var/db/pkg/`).
  * *See excavation*: [Portage: Package Management as Policy-Constrained Recipe Execution](excavations/portage.md)

* **Object-Capability Model**: A software design pattern that combines object-oriented encapsulation with capability-based security. An object reference *is* the unforgeable authority to perform actions on that object.
  * *See excavation*: [Intel iAPX 432](excavations/intel-iapx-432.md), [KeyKOS and the Nanokernel Capability Lineage](excavations/keykos-nanokernel-capabilities.md)

### R
* **RAII (Resource Acquisition Is Initialization)**: A deterministic resource management paradigm pioneered in C++ where system resources (heap memory, file descriptors, locks) are bound to stack object lifetimes, ensuring automatic cleanup upon scope exit or stack unwinding during exception paths.
  * *See excavation*: [C++: Zero-Overhead Abstraction & Deterministic Resource Control](excavations/cpp.md)
* **Radix Economy**: A mathematical measure of the efficiency of representing numbers in a given base, defined as $R \times \lfloor \log_R(N) + 1 \rfloor$ for base $R$ and maximum value $N$. It is mathematically optimized at the transcendental base $e \approx 2.718$, which makes base 3 (ternary) more efficient than base 2 (binary).
  * *See excavation*: [Balanced Ternary](excavations/balanced-ternary.md)
* **Residue Number System (RNS)**: A non-positional numeral system representing integers via remainders modulo pairwise coprime integers. RNS eliminates carry propagation for additions, subtractions, and multiplications, executing them in independent parallel channels.
  * *See excavation*: [Residue Number System (RNS)](excavations/residue-number-system.md)
* **Redundant Residue Number System (RRNS)**: An extension of RNS incorporating extra (redundant) coprime moduli to form an error-detecting or error-correcting arithmetic code capable of real-time fault isolation.
  * *See excavation*: [Residue Number System (RNS)](excavations/residue-number-system.md)
* **[Reversible Computing](excavations/reversible-computing.md)**: A paradigm where logic gates perform bijective (one-to-one) mapping between inputs and outputs, allowing computation to run backward and theoretically bypassing Landauer's thermodynamic limit.
  * *See excavation*: [Reversible Computing](excavations/reversible-computing.md)

### S
* **Safari**: An excavation of Apple's browser application architecture, WebKit rendering engine lineage, JavaScriptCore JIT virtual machine, multi-process content isolation, WKWebView app-embedding substrate, and Intelligent Tracking Prevention.
  * *See excavation*: [Safari: The WebKit Engine Lineage & Platform Web Runtime Substrate](excavations/safari.md)
* **Signals and Slots**: A type-safe, compile-time verified publish/subscribe event communication paradigm introduced by Qt that decouples event emitters from receiver slots without requiring callback function pointers or explicit header dependencies.
  * *See excavation*: [Qt](excavations/qt.md)
* **Same-Origin Policy (SOP)**: A foundational web security boundary introduced in Netscape Navigator 2.02 restricting scripts running on origin $A$ ($\langle\text{scheme, host, port}\rangle$) from accessing or mutating document properties and session data belonging to origin $B$.
  * *See excavation*: [Netscape](excavations/netscape.md)
* **SSL (Secure Sockets Layer)**: A transport-layer cryptographic protocol stack (SSL 2.0/3.0) and public key infrastructure engineered by Netscape to enable encrypted communication, certificate authority trust verification, and HTTPS e-commerce.
  * *See excavation*: [Netscape](excavations/netscape.md)
* **SIMT (Single Instruction, Multiple Threads)**: An execution model where multiple scalar threads execute the same instruction in lockstep groups (warps), managing control-flow divergence automatically via execution mask stacks.
  * *See excavation*: [NVIDIA Architecture: The Programmable Parallel Substrate & CUDA Platform](excavations/nvidia.md)
* **Single-Level Store (SLS)**: A memory management architecture where all secondary storage (such as disk drives) is integrated into a single, flat, virtually-addressed main memory space, completely eliminating the user-level distinction between file systems and RAM.
  * *See excavation*: [Multics](excavations/multics.md), [KeyKOS and the Nanokernel Capability Lineage](excavations/keykos-nanokernel-capabilities.md)
* **Spatial Computing (Hardware)**: Architectures where software logic is mapped directly onto a physical grid of processing elements with localized communication channels (e.g., FPGAs, [Systolic Arrays](excavations/systolic-arrays.md), Cellular Automata), removing global bus bottlenecks.
  * *See excavation*: [Systolic Arrays](excavations/systolic-arrays.md)
* **Stack Machine**: A processor architecture that uses a hardware evaluation stack rather than general-purpose registers to execute zero-operand instructions.
  * *See excavation*: [Stack Machines](excavations/stack-machines.md)
* **[Stochastic Computing](excavations/stochastic-computing.md)**: A computing paradigm where continuous values are encoded as randomized binary bitstreams, mapping complex arithmetic operations (like multiplication) onto simple logic gates (like AND/XNOR) at the cost of execution time.
  * *See excavation*: [Stochastic Computing](excavations/stochastic-computing.md)
* **Styx Protocol**: A network protocol derived from 9P, serving as the universal communication interface in the [Inferno](excavations/inferno.md) operating system to expose system services, devices, and files transparently over public networks.
  * *See excavation*: [Inferno](excavations/inferno.md)
* **Superconducting / Cryogenic Computing**: A high-performance hardware paradigm operating at cryogenic temperatures, using Josephson junctions and Single Flux Quantum (SFQ) logic to achieve ultra-high clock frequencies and near-zero power dissipation.
  * *See excavation*: [Superconducting & Cryogenic Microarchitectures](excavations/superconducting-cryogenic.md)
* **[Symbolic AI](excavations/symbolic-ai.md)**: An approach to artificial intelligence based on high-level, human-readable symbols, formal logic, and rule-based inference engines.
  * *See excavation*: [Symbolic AI](excavations/symbolic-ai.md)
* **Systolic Array**: A network of homogeneous, tightly-coupled processing elements that rhythmically compute and pass data through the system, optimizing matrix multiplication and other highly structured, compute-bound workloads.
  * *See excavation*: [Systolic Arrays](excavations/systolic-arrays.md)

### T
* **Tensor Core**: A specialized microarchitectural execution unit inside NVIDIA GPUs designed to perform 2D Warp Matrix Multiply-Accumulate (WMMA) operations in a single micro-op using mixed-precision numerical formats.
  * *See excavation*: [NVIDIA Architecture: The Programmable Parallel Substrate & CUDA Platform](excavations/nvidia.md)
* **Tagged Memory**: A hardware mechanism where every word in memory is accompanied by a few extra non-addressable bits (tags) indicating its data type (e.g., integer, float, code pointer, capability), allowing hardware to prevent type safety violations and unauthorized execution.
  * *See excavation*: [Lisp Machines](excavations/lisp-machines.md)
* **TrueTime API**: A hardware-backed clock synchronization abstraction that provides bounded time uncertainty intervals, enabling global transactional external consistency without central lock bottlenecks.
  * *See excavation*: [Google: The Platform Machine of Scale](excavations/google.md)
* **Transition Signaling (2-Phase Handshaking)**: A clockless communication protocol where any voltage transition (either low-to-high or high-to-low) represents a control event, enabling high-speed handshake transactions with minimal signal lines and state changes.
  * *See excavation*: [Asynchronous Microprocessors](excavations/asynchronous-processors.md)
* **Tuple Space**: A persistent, associative, multi-set memory pool serving as the central coordination medium in generative communication. It stores both passive data tuples and active process tuples.
  * *See excavation*: [Linda Tuple Spaces](excavations/linda-tuple-spaces.md)
* **Trail (WAM)**: A dedicated memory stack in the Warren Abstract Machine that records the addresses of logic variables bound during unification, enabling those variables to be unbound (reset to free) during chronological backtracking.
  * *See excavation*: [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)

### U
* **Unification**: A mathematical and computational process that binds first-order terms and logic variables dynamically to make two symbolic expressions identical.
  * *See excavation*: [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)
* **USE Flags**: Bi-level compile-time configuration toggles (global in `make.conf`, per-package in `package.use`) in Gentoo's Portage system that dynamically mutate the package dependency graph (`DEPEND`/`RDEPEND`) and configure build parameters prior to compilation.
  * *See excavation*: [Portage: Package Management as Policy-Constrained Recipe Execution](excavations/portage.md), [Gentoo](excavations/gentoo.md)

### V
* **Vector Processing**: A processor design that executes a single instruction on a collection of one-dimensional arrays of data (vectors) using pipelined functional units, optimizing high-throughput scientific workloads.
  * *See excavation*: [Vector Supercomputing](excavations/vector-supercomputing.md)
* **VFS (Virtual File System)**: An in-kernel polymorphic file dispatcher and object-oriented abstraction mapping uniform system-calls (`read`, `write`, `open`) to diverse physical filesystem drivers.
  * *See excavation*: [Linux: The Ubiquitous Substrate](excavations/linux.md)
* **Very Long Instruction Word (VLIW)**: A processor design where the compiler groups independent, parallel operations into a single, very wide instruction word, relying on compile-time analysis rather than dynamic out-of-order execution hardware.
  * *See excavation*: [VLIW / EPIC Architectures](excavations/vliw-epic.md)
* **Von Neumann Bottleneck**: The throughput limitation on computer systems caused by the physical separation of the central processing unit and memory, requiring all instruction and data transfers to share a single bus.
  * *See modern relevance*: [AI & Hardware Bottlenecks](modern-relevance/ai.md)

### Z
* **Zero-Overhead Abstraction**: The core design principle formulated by Bjarne Stroustrup stating that what you don't use, you don't pay for, and what you do use, you couldn't write any better by hand. Higher-level language constructs must compile down to direct machine code matching or exceeding manual C assembly.
  * *See excavation*: [C++: Zero-Overhead Abstraction & Deterministic Resource Control](excavations/cpp.md)

### W
* **Warp**: A group of 32 parallel threads in NVIDIA GPU architectures that execute instructions in lockstep over SIMT execution lanes.
  * *See excavation*: [NVIDIA Architecture: The Programmable Parallel Substrate & CUDA Platform](excavations/nvidia.md)
* **WebKit**: A portable, embeddable web rendering and execution engine lineage forked from KHTML/KJS, comprising WebCore, JavaScriptCore, and the WebKit2 multi-process architecture.
  * *See excavation*: [Safari: The WebKit Engine Lineage & Platform Web Runtime Substrate](excavations/safari.md)
* **WKWebView**: An out-of-process, sandboxed application framework interface exposing WebKit execution to native applications with host memory insulation and full JIT capabilities.
  * *See excavation*: [Safari: The WebKit Engine Lineage & Platform Web Runtime Substrate](excavations/safari.md)
* **WASABI Framework**: Winamp Advanced Software Architecture Building Infrastructure—an object-oriented application and skinning framework introduced in Winamp 3 featuring a declarative XML layout tree and an embedded stack-based virtual machine executing MAKI bytecode scripts.
  * *See excavation*: [Winamp](excavations/winamp.md)
* **Win32 API**: A highly stable, multi-decade 32-bit flat application programming interface designed to decouple application target software from dynamic kernel changes.
  * *See excavation*: [Microsoft: The Platform Machine](excavations/microsoft.md)
* **Winamp Plugin C-ABI**: A low-overhead C struct jump-table interface specification defined by Nullsoft (`In_Module`, `Out_Module`, `winampDSPModule`, `winampGeneralPurposePlugin`) enabling third-party dynamic libraries to plug into host decoding, audio DSP, and UI control pipelines without name mangling or runtime vtable dependencies.
  * *See excavation*: [Winamp](excavations/winamp.md)
* **[Wafer-Scale Integration](excavations/wafer-scale-integration.md) (WSI)**: An advanced semiconductor manufacturing paradigm that builds an entire digital system (incorporating multiple processor nodes, memory blocks, and interconnect networks) on a single, uncut silicon wafer, completely bypassing chip-packaging boundaries.
  * *See excavation*: [Wafer-Scale Integration](excavations/wafer-scale-integration.md)
* **Warren Abstract Machine (WAM)**: An abstract instruction set and memory architecture developed by David H. D. Warren to execute compiled Prolog efficiently using specialized stacks, heap, trail, and register allocations.
  * *See excavation*: [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)

---

## Part 2: A Taxonomy of [Forgotten Abstractions](patterns/forgotten-abstractions.md)

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

* **Associative / Content-Addressable Execution**: Computing directly on matched data fields in parallel without address decoding, driven by associative matching of data content.
  * *Example*: [Associative Processors](excavations/associative-processors.md)
* **Dataflow / Token Matching**: Execution is purely event-driven and parallel. Operations execute as soon as their inputs are physically routed to them.
  * *Example*: [Dataflow Computing](excavations/dataflow-computing.md)
* **Demand-Driven Graph Reduction**: Programs are represented as directed acyclic graphs (DAGs) in a node-based heap, and execution proceeds by dynamically rewriting active reducible expressions (redexes) until a terminal normal form is reached.
  * *Example*: [Graph Reduction Architectures & Functional Hardware](excavations/graph-reduction-machines.md)
* **Zero-Operand Stack Evaluation**: Instructions operate implicitly on a hardware evaluation stack, eliminating register specifiers from the instruction set encoding and simplifying compiler code generation.
  * *Example*: [Stack Machines](excavations/stack-machines.md), [Burroughs Large Systems](excavations/burroughs-large-systems.md)
* **Spatial & Grid Routing**: Processing is mapped onto physical coordinate grids of simple ALUs. Software is compiled as spatial configurations and data routing pathways rather than sequential code.
  * *Example*: [Systolic Arrays](excavations/systolic-arrays.md), [Cellular Automata Hardware](excavations/cellular-automata-hardware.md), [The MIT J-Machine](excavations/j-machine.md)
* **Continuous Analog Scaling**: Solving mathematical systems through continuous physical interactions (voltages, light waves, chemical concentrations) rather than discrete digital clock cycles.
  * *Example*: [Analog Computing](excavations/analog-computing.md), [Optical Computing](excavations/optical-computing.md), [Molecular & Biocomputing](excavations/molecular-biocomputing.md), [Stochastic Computing](excavations/stochastic-computing.md)
* **Self-Timed & Asynchronous Control**: Operations and pipeline stages synchronize locally via request-acknowledge handshake signals, executing at the natural physical speed of physical gates rather than relying on a global clock tree.
  * *Example*: [Asynchronous Microprocessors](excavations/asynchronous-processors.md), [Neuromorphic Hardware](excavations/neuromorphic-hardware.md)
* **Logical & Inference Execution**: Computing via backward-chaining resolution, recursive variable unification, and chronological backtracking search over saved choice points.
  * *Example*: [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)

### 2. Memory & Protection Abstractions

These abstractions define how memory is organized, addressed, and secured against unauthorized access or structural corruption.

* **Content-Addressable / Associative Memory**: Memory is queried and written by content matching rather than address decoders, bypassing the address-space barrier entirely.
  * *Example*: [Associative Processors](excavations/associative-processors.md)
* **Object Capabilities & Descriptors**: Moving access control from software operating system layers to hardware unforgeable tokens. If a processor does not possess the physical capability token, it is physically impossible to construct the memory address.
  * *Example*: [Capability Systems](excavations/capability-systems.md), [Intel iAPX 432](excavations/intel-iapx-432.md)
* **Tagged Memory**: Enforcing data type safety in hardware. An integer can never be executed as instruction code, and a data word can never be treated as a pointer, eliminating entire classes of exploit vectors.
  * *Example*: [Lisp Machines](excavations/lisp-machines.md), [Burroughs Large Systems](excavations/burroughs-large-systems.md), [The MIT J-Machine](excavations/j-machine.md), [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)
* **Single-Level Store (SLS)**: Removing the mental and structural wall between volatile memory (RAM) and non-volatile storage (Disk). Everything exists inside a singular, persistent, universally addressable space.
  * *Example*: [Multics](excavations/multics.md)
* **Hierarchical Ring Protection**: Defining access control as concentric rings of privilege. Inner rings (e.g., Ring 0) have full access, while outer rings must cross formal gates to request services, preventing privilege escalation.
  * *Example*: [Multics](excavations/multics.md)

### 3. Concurrency & Communication Abstractions

These abstractions define how parallel computational threads or systems coordinate, synchronize, and exchange information.

* **Synchronous CSP Channels**: Processes synchronize and communicate exclusively via unbuffered, blocking channels. This forces deterministic execution and prevents race conditions without relying on locks or semaphores.
  * *Example*: [Transputers](excavations/transputers.md), [Occam](excavations/occam.md)
* **Asynchronous Actor Messaging**: Independent processes that communicate exclusively via dynamic, asynchronous messages, avoiding shared-state corruption and making distributed computing identical to local computing.
  * *Example*: [Smalltalk](excavations/smalltalk.md), [The MIT J-Machine](excavations/j-machine.md)
* **Distributed Service Protocols (Everything is a File/Service)**: Standardizing all system resources (CPUs, screens, networks, configurations) under a unified, simple representation protocol (9P) accessed over a network.
  * *Example*: [Plan 9](excavations/plan-9.md), [Inferno](excavations/inferno.md)
* **Massively Parallel SIMD Hypercubes**: Structuring tens of thousands of single-bit processors in a hypercube network, executing operations in lock-step to solve massive-scale parallel data problems.
  * *Example*: [Connection Machine](excavations/connection-machine.md)
* **Generative Tuple Spaces**: Decoupling communication completely in both space (anonymous) and time (asynchronous) via a shared, content-addressable multi-set data pool.
  * *Example*: [Linda Tuple Spaces](excavations/linda-tuple-spaces.md)
* **Committed-Choice Stream Concurrency**: Coordinating concurrent goal-processes using shared, write-once logic variables as event-driven, blocking dataflow communication streams.
  * *Example*: [Prolog, the Warren Abstract Machine, and Fifth Generation Computer Systems (FGCS) Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md)
