# Digital Archaeology Index

                 Digital Archaeology
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   Architectures    Operating      Languages
        │            Systems            │
        │               │               │
  ┌─────┼─────┐     ┌───┼───┐      ┌────┼────┐
  │     │     │     │   │   │      │    │    │
Stack  Ternary Data  Plan [Inferno](excavations/inferno.md) Small Lisp [Occam](excavations/occam.md)
        │      │
        └───Modern AI──────FPGA────Mixed-Radix
        
> **A high-level map connecting excavations, patterns, and modern architectural relevance.**

---

## Architectures

- [Analog Computing](excavations/analog-computing.md) — *[Continuous physical modeling](GLOSSARY.md) via wave, power, and operational amplifier dynamics.*
- [Asynchronous Microprocessors](excavations/asynchronous-processors.md) — *Self-timed [micropipelines](GLOSSARY.md) and clockless processor architectures bypassing global clock constraints.*
- [Associative Processors & Content-Addressable Computing](excavations/associative-processors.md) — *Content-addressable parallel execution and bit-serial in-memory computing.*
- [Balanced Ternary](excavations/balanced-ternary.md) — *Ternary logic, arithmetic, and power efficiency advantages over binary.*
- [Cellular Automata Hardware](excavations/cellular-automata-hardware.md) — *Decentralized, spatial grid arrays executing local interaction rules.*
- [Connection Machine](excavations/connection-machine.md) — *Fine-grained SIMD massively parallel hypercube processing.*
- [Dataflow Computing](excavations/dataflow-computing.md) — *Non-von Neumann, event-driven, token-matching spatial execution.*
- [Explicit Data Graph Execution (EDGE) & The TRIPS Architecture](excavations/edge-architecture.md) — *Instruction-level spatial dataflow and block-structured microarchitectures.*
- [EBCDIC (Extended Binary Coded Decimal Interchange Code)](excavations/ebcdic.md) — *IBM's 8-bit punched-card-derived character representation establishing durable ecosystem boundaries.*
- [Fluidic Logic Systems](excavations/fluidic-logic-systems.md) — *Wall attachment, jet interaction, and fluid-dynamic computation without moving parts or electronics in extreme environments.*
- [Graph Reduction Architectures & Functional Hardware](excavations/graph-reduction-machines.md) — *Non-von Neumann expression-rewriting architectures executing pure functional programs natively.*
- [Molecular & Biocomputing](excavations/molecular-biocomputing.md) — *Computation using molecules, DNA strands, chemical reactions, and synthetic biology.*
- [Neuromorphic Hardware](excavations/neuromorphic-hardware.md) — *Asynchronous, event-driven spiking neural networks and in-memory compute.*
- [ONNX Open Neural Network Exchange Substrate](excavations/onnx.md) — *Standardized open computational graph representation, versioned operator sets (Opsets), and pluggable Execution Provider (EP) hardware backends.*
- [Optical Computing](excavations/optical-computing.md) — *Photonic interference, spatial WDM, and sub-nanosecond matrix processing.*
- [Logarithmic Number System (LNS)](excavations/logarithmic-number-system.md) — *Real-number logarithmic representation simplifying multiplication, division, and exponentiation into addition and subtraction.*
- [Posit Arithmetic & Type-3 Unum Systems](excavations/posit-arithmetic.md) — *Tapered regime bit encoding, exact quire accumulation, and low-bitwidth LLM quantization.*
- [Residue Number System (RNS)](excavations/residue-number-system.md) — *Carry-free parallel arithmetic representing integers modulo coprime sets for DSP, cryptography, and FHE.*
- [Reversible Computing](excavations/reversible-computing.md) — *Information-preserving logic gates bypassing Landauer's thermodynamic limit.*
- [Stack Machines](excavations/stack-machines.md) — *Hardware zero-operand evaluation stack evaluation architectures.*
- [Stochastic Computing](excavations/stochastic-computing.md) — *Trading execution latency for extreme structural simplicity and noise tolerance by computing mathematically with random binary bitstreams.*
- [Superconducting & Cryogenic Microarchitectures](excavations/superconducting-cryogenic.md) — *SFQ/RSFQ logic at cryogenic temperatures for ultra-high speed and efficiency.*
- [Systolic Arrays](excavations/systolic-arrays.md) — *Regular, pipelined grids of processing elements for dense compute-bound workloads.*
- [The MIT J-Machine](excavations/j-machine.md) — *Fine-grained message-driven 3D routing fabric executing [active messages](GLOSSARY.md) in hardware.*
- [Transputers](excavations/transputers.md) — *Massively parallel microprocessors with native channel-based CSP messaging.*
- [Vector Supercomputing](excavations/vector-supercomputing.md) — *Cray-style vector processors optimized for scientific and high-throughput workloads.*
- [VLIW / EPIC Architectures](excavations/vliw-epic.md) — *Compiler-driven explicit instruction-level parallelism (Itanium and predecessors).*
- [Wafer-Scale Integration](excavations/wafer-scale-integration.md) — *Eliminating the package boundary by integrating entire digital systems monolithically across silicon wafers.*

---

## Operating Systems & Environments

- [Apple: The Integrated Platform Surface](excavations/apple.md) — *How hardware, system software, runtimes, sandboxes, and distribution were co-designed into a resilient, vertically [integrated platform surface](GLOSSARY.md).*
- [Apple Metal Architecture: The Vertically Integrated GPU Substrate](excavations/apple-metal.md) — *How a low-overhead, explicit GPU command model co-evolved with [Apple Silicon](GLOSSARY.md), TBDR rasterization, unified memory, and OS framework pipelines to create an ecosystem-scale platform substrate.*
- [BeOS / Haiku](excavations/beos-haiku.md) — *Media-optimized, responsive OS with modern design (revived as open-source Haiku).*
- [eBPF: In-Kernel Virtualization and Programmable Infrastructure Substrate](excavations/ebpf.md) — *How an in-kernel virtual machine, static verifier contract, map state substrate, attach-point ecosystem, and CO-RE portability layer transformed Linux into a dynamically programmable kernel and universal observability/networking substrate.*
- [FFmpeg: Multimedia Pipeline Architecture & Universal Processing Substrate](excavations/ffmpeg.md) — *Demux–decode–filter–encode–mux 5-stage media dataflow pipeline, `libav*` library decomposition, format capability negotiation, and universal CLI operator interface.*
- [Gentoo: Source-Based Distribution Architecture & Compile-Time Configuration](excavations/gentoo.md) — *[Portage](GLOSSARY.md) package manager, [ebuild](GLOSSARY.md) executable recipes, USE flag compile-time feature selection, cascading profile policy hierarchy, and binhost hybridization.*
- [Burroughs Large Systems](excavations/burroughs-large-systems.md) — *High-level language hardware integration with descriptors and stack architecture.*
- [Capability Systems](excavations/capability-systems.md) — *Object-capability OS models ([KeyKOS](GLOSSARY.md), EROS, CHERI).*
- [Google: The Platform Machine of Scale](excavations/google.md) — *How the repeated conversion of warehouse-scale operational problems into narrow, exportable software abstractions established the datacenter as the computer.*
- [IBM AS/400: Layered Technology-Independent Substrate & Single-Level Store](excavations/ibm-as400.md) — *Layered, object-based machine architecture decoupling application semantics from physical hardware via TIMI and single-level store addressability.*
- [Inferno](excavations/inferno.md) — *Distributed VM OS utilizing Limbo and the Styx/[9P protocol](GLOSSARY.md).*
- [Intel: The Architectural & Compatibility Substrate](excavations/intel.md) — *How binary instruction compatibility, microcode µop translation, platform chipsets, and process co-design created an enduring ecosystem substrate.*
- [Intel iAPX 432](excavations/intel-iapx-432.md) — *Capability-based object-oriented architecture.*
- [KeyKOS and the Nanokernel Capability Lineage](excavations/keykos-nanokernel-capabilities.md) — *Pure object-capability security, minimal nanokernel trusted computing bases, and Continuous Orthogonal Persistence.*
- [Linux: The Ubiquitous Substrate](excavations/linux.md) — *How the decoupling of a stable SCI from dynamic kernel internals coupled with open, collaborative production turned a monolithic Unix-like kernel into ubiquitous platform infrastructure.*
- [Lisp Machines](excavations/lisp-machines.md) — *Single-user, hardware-integrated dynamic environment.*
- [Microsoft: The Platform Machine](excavations/microsoft.md) — *How architectural compatibility, APIs (Win32, COM, .NET), and developer-facing abstractions converted software into a self-reinforcing platform machine.*
- [Model Context Protocol: Host-Server Capability Bus & Open Primitive Substrate](excavations/model-context-protocol.md) — *An open client-server RPC contract, dynamic capability negotiation, JSON Schema tool gates, resource URI context surfaces, and transport-decoupled session lifecycles establishing a standardized host-server capability bus for model-driven systems.*
- [NVIDIA Architecture: The Programmable Parallel Substrate & CUDA Platform](excavations/nvidia.md) — *How fixed-function graphics hardware evolved into a general-purpose SIMT compute substrate, and how the [CUDA](GLOSSARY.md) platform and Tensor Cores established platform persistence for HPC and AI.*
- [Multics](excavations/multics.md) — *Influential secure, multi-user timesharing system with segmentation and rings.*
- [Netscape: The Programmable Web Runtime & Network Client Substrate](excavations/netscape.md) — *Browser as an application platform, embedded JavaScript runtime, NPAPI plugin architecture, SSL/TLS security stack, HTTP cookies, and Mozilla open-source transition.*
- [llama.cpp: Quantization-First local Inference](excavations/llama-cpp.md) — *How low-bit block quantization, unified memory-bandwidth-aware containers, and decoupled execution runtimes shifted large language models to consumer devices.*
- [Cursor IDE: The AI-Native Editor Substrate & Agentic Workspace](excavations/cursor-ide.md) — *How the integration of codebase context indexing, supervised multi-file edit agents, diff-mediated trust boundaries, and VS Code extension-host compatibility transformed the code editor into an AI-mediated software production environment.*
- [Large Language Models: The Autoregressive Sequence Substrate](excavations/large-language-models.md) — *How scaled neural sequence modeling, transformer architectures, post-training alignment, and tool-augmented runtimes transformed next-token prediction into a general-purpose programmable interface substrate.*
- [OpenAI: The Model-as-Platform Substrate](excavations/openai.md) — *How the standardization of foundation models, remote APIs, alignment, and stateful agentic threads turned learned weights into stable platform infrastructure.*
- [Qwen Lineage: Mid-Size Open-Weight Substrate](excavations/qwen.md) — *Alibaba's industrial model family, multi-tier parameter scaling (8B–27B/32B VRAM sweet spot), 151k multilingual vocabulary, ChatML role framing, native JSON tool calling, and Apache 2.0 open-weight packaging.*
- [Plan 9](excavations/plan-9.md) — *Distributed UNIX successor ("Everything is a 9P service").*
- [Portage: Package Management as Policy-Constrained Recipe Execution](excavations/portage.md) — *Executable package recipes (`ebuilds`), feature-predicate dependency resolution (`USE` flags), cascading system policy surfaces (`profiles`), plain-text state tracking (`VDB`), LD_PRELOAD build sandboxing, and resolution planning.*
- [Project Xanadu](excavations/project-xanadu.md) — *[Bi-directional hypermedia](GLOSSARY.md) network and deep versioning system.*
- [Qt: The Cross-Platform Application Substrate & Meta-Object Runtime Lineage](excavations/qt.md) — *Meta-Object Compiler (`moc`), signals/slots communication, hierarchical QObject ownership, platform backends (QPA), and Qt Quick / QML declarative scene graph.*
- [Safari: The WebKit Engine Lineage & Platform Web Runtime Substrate](excavations/safari.md) — *KHTML engine fork, WebKit2 multi-process architecture, JavaScriptCore JIT VMs, app-embedded [WKWebView](GLOSSARY.md) substrate, and Intelligent Tracking Prevention privacy runtime.*
- [Solaris Operating System](excavations/solaris.md) — *SVR4 commercial Unix platform, production-safe dynamic observability (DTrace), dependency-aware service management (SMF), integrity-centered pooled storage (ZFS), and lightweight OS virtualization (Zones).*
- [VirtualBox: Hosted x86 Hypervisor, Paravirtual Guest Services & Desktop Appliance Packaging](excavations/virtualbox.md) — *Hosted (Type-2) x86 hypervisor architecture, VT-x/AMD-V hardware virtualization integration, Pluggable Device Manager (PDM) virtual hardware, Guest Additions Host-Guest Communication Manager (HGCM) backdoor protocols, Virtual Disk Image (VDI) differencing snapshot trees, Innotek Portable Runtime (IPRT) cross-host portability, and open-core GPLv2 distribution.*
- [Winamp: The Modular Media Substrate & Extensible Application Platform](excavations/winamp.md) — *C-ABI plugin host architecture, decoupled audio pipelines, declarative skinning layers, and local collection metadata substrate.*

---

## Programming Languages & AI Paradigms

- [C++: Zero-Overhead Abstraction & Deterministic Resource Control](excavations/cpp.md) — *Combining low-level machine control with user-defined abstractions via zero-overhead mechanisms, RAII resource control, value semantics, and template generic programming.*
- [Linda Tuple Spaces](excavations/linda-tuple-spaces.md) — *Coordinate-free parallel coordination, [generative communication](GLOSSARY.md), and associative pattern-matching.*
- [Python: Dynamic Language Substrate & Native Extension Engine](excavations/python.md) — *Dynamic object model, dunder protocols, C-extension C-API boundary, "batteries included" standard library, PyPI packaging, and scientific/ML orchestration gravity.*
- [Occam](excavations/occam.md) — *Concurrent language based on Communicating Sequential Processes (CSP).*
- [Smalltalk](excavations/smalltalk.md) — *Pure image-based object-oriented environment and dynamic messaging.*
- [Symbolic AI](excavations/symbolic-ai.md) — *Logic programming, inference engines, and formal knowledge representation.*
- [Prolog, the Warren Abstract Machine, and FGCS Hardware Lineages](excavations/prolog-wam-fgcs-hardware.md) — *Logic programming compiled execution, stack-heap-trail environments, and committed-choice process networks.*

---

## Patterns

- [Abstract Machine Persistence](patterns/abstract-machine-persistence.md) — *Decoupling language runtimes from physical hardware ISAs.*
- [Constraint Migration](patterns/constraint-migration.md) — *How shifting physical, technological, and economic limits resurrect discarded abstractions.*
- [Economic Failures](patterns/economic-failures.md) — *Why technically superior ideas fail due to manufacturing economics and cost dynamics.*
- [Ecosystem Lock-In](patterns/ecosystem-lockin.md) — *How developer tooling, compilers, and legacy momentum favor established norms.*
- [Explicit Authority Substrate](patterns/explicit-authority-substrate.md) — *Hardware- and capability-enforced principal isolation models.*
- [Forgotten Abstractions](patterns/forgotten-abstractions.md) — *Elegant concepts and mental models that faded from mainstream use but retain significant potential.*
- [Heterogeneous Revival](patterns/heterogeneous-revival.md) — *How historical architectures return as specialized hardware engines inside general systems.*
- [Interface / Conversion Tax](patterns/interface-conversion-tax.md) — *Performance overheads when bridging disparate representations.*
- [Operator-Cost Inversion](patterns/operator-cost-inversion.md) — *When historical hardware bottlenecks become modern performance bargains.*
- [Recurring Ideas](patterns/recurring-ideas.md) — *How abandoned computing paradigms re-emerge under new physical constraints.*

---

## Synthesis

- [Academic Overview & Research Entry Point](synthesis/digital-archaeology-overview.md) — *A short, dense, and citable reference introducing our six core lineages, methodology, and BibTeX records.*
- [AI Capability Runtime Synthesis](synthesis/ai-capability-runtime-gguf-ebpf.md) — *An architectural synthesis of GGUF model artifacts, llama.cpp local inference, and verifier-constrained eBPF in-kernel execution mediated by a capability broker.*
- [MCP & File-Sharing Descriptors Synthesis](synthesis/mcp-and-file-sharing-descriptors.md) — *An architectural synthesis of Model Context Protocol (MCP) host-server capability buses and file-sharing descriptor lineages (.torrent, .nzb, Napster, .par2).*
- [Architectural Distillation](synthesis/architectural-distillation.md) — *How failed computing systems leave behind enduring abstractions that shape modern architectures.*
- [Architectural Roadmap Re-Evaluation](synthesis/architectural-roadmap-re-evaluation.md) — *A comprehensive, academically rigorous phase-by-phase re-evaluation of the Digital Archaeology Roadmap (Phases I through XIII) under modern post-Dennard, sub-5nm scaling, and zero-trust security constraints.*
- [Alternative Mathematical Execution Paradigms](synthesis/alternative-mathematical-execution-paradigms.md) — *How symmetric [balanced ternary](excavations/balanced-ternary.md), probabilistic stochastic bitstreams, and symbolic logic resolution trees bypass the memory wall and density constraints of modern AI.*
- [Capability-Based Security](synthesis/capability-based-security.md) — *The revival of fine-grained, unforgeable hardware-level rights in the zero-trust and AI era.*
- [Compiler-Hardware Co-Design](synthesis/compiler-hardware-co-design.md) — *Why the modern performance frontier relies on treating compilers and custom silicon as a single unified system.*
- [The Evolution of Coordination Abstractions](synthesis/evolution-of-coordination-abstractions.md) — *The evolution of process communication and concurrency models from shared-memory to decoupled coordination.*
- [Cross-Excavation Recent Inclusions Synthesis](synthesis/recent-inclusions-crosscut.md) — *High-density architectural and mechanistic synthesis of RNS, LNS, fluidics, [KeyKOS](GLOSSARY.md) capabilities, and Prolog/WAM/FGCS logic-programming hardware.*
- [Excavation Completeness Audit](synthesis/excavation-completeness-formatting-audit.md) — *Systematic completeness and formatting audit covering all excavation deep dives.*
- [Heterogeneous Revival Synergies](synthesis/heterogeneous-revival-synergies.md) — *Pairwise and triple co-design integrations combining spatial, neuromorphic, capability, optical, and cryogenic computing.*
- [Pattern Catalog Revision Report](synthesis/pattern-catalog-revision-report.md) — *Report on pattern promotion, structural revisions, and cross-paradigm insights.*
- [Pattern Impact Audit](synthesis/pattern-impact-audit-recent-inclusions.md) — *Impact analysis of newly introduced patterns on historical excavations.*
- [Repository Consistency Audit](synthesis/repo-consistency-audit.md) — *Full-repository structural, conceptual, and relational consistency audit.*
- [Repo-Wide Gap Analysis](synthesis/repo-wide-gap-analysis.md) — *Comprehensive audit and resolution report for repository structural coherence.*
- [The Return of Spatial Computing](synthesis/return-of-spatial-computing.md) — *How sidelined parallel, grid, and dataflow execution models are reclaiming dominance in AI hardware.*
- [State of Revival: Architectural Synthesis](synthesis/state-of-revival.md) — *High-density evaluation of all six lineages under modern physical, energy, and security constraints.*

---

## Modern Relevance & Perspectives

- [AI & Hardware Bottlenecks](modern-relevance/ai.md) — *Applying non-von Neumann models to the memory wall and matrix acceleration.*
- [Coprocessors](modern-relevance/coprocessors.md) — *Offloading domain-specific execution from general-purpose CPUs.*
- [Academic Research & Hardware Partnerships](modern-relevance/partnerships.md) — *Connecting key excavations to active academic labs, zero-trust security initiatives, and open-source FPGA/ASIC hardware toolchains.*
- [FPGA Prototyping & Reconfigurable Computing](modern-relevance/fpga.md) — *Modern programmable logic as a time machine for architectural experimentation.*
- [Mixed-Radix & Alternative Number Systems](modern-relevance/mixed-radix.md) — *Evaluating ternary, posits, and log number systems in modern silicon.*
- [Modern Revival Readiness Scorecard](modern-relevance/revival-readiness.md) — *Quantitative comparative evaluation of alternative computing lineages, assessing Spatial, Capability, Continuous/Thermodynamic, and Distributed SLS OS technologies under modern CMOS constraints.*
- [Symbolic Computing](modern-relevance/symbolic-computing.md) — *Neuro-symbolic integration, automated theorem proving, and deterministic guardrails.*

---

## Reconstructions & Simulators

- [Plan 9 Namespace Simulator](reconstructions/plan9-9p/) — *Stateful 9P/Styx transaction simulator demonstrating process-private directories and dynamic union directory mounts.*
- [Systolic Array Simulator](reconstructions/systolic-array/) — *Cycle-accurate, parameterizable matrix multiplier comparing Weight-Stationary and Output-Stationary execution dataflows with CMOS energy proxy metrics.*
- [Balanced Ternary & Mixed-Radix Simulator](reconstructions/mixed-radix-sim/) — *Multi-trit arithmetic logic, logic gate suite, and decimal-ternary conversions.*
- [Dynamic Tagged-Token Dataflow Engine](reconstructions/dataflow-engine/) — *Parallel execution engine with dynamic token-tag matching and asynchronous scheduling.*
- [Capability-Based Memory Protection Emulator](reconstructions/capability-security/) — *Register-level CPU and Tagged RAM simulating hardware capabilities and domain transitions.*
- [Neuro-Symbolic Logic Solver](reconstructions/neuro-symbolic/) — *Hybrid AI decision system combining neural network outputs with forward-chaining rules.*
- [CSP Synchronous Messaging Simulator](reconstructions/csp-messaging/) — *Synchronous channel rendezvous messaging, ALT-based multiplexing, and deadlock reporting.*
- [Continuous Analog & Optical Wave Accelerator Simulator](reconstructions/analog-optical/) — *Photonic [tensor core](GLOSSARY.md) wave interference and op-amp mass-spring solvers.*
- [Synthesizable Hardware IP Core Blueprints](reconstructions/synthesizable-hardware/) — *Synthesizable SystemVerilog models of [Balanced Ternary](excavations/balanced-ternary.md) ALUs and tagged RAM bounds checkers.*
- [Multi-Architecture Co-Simulation Orchestrator](reconstructions/co-simulation/) — *A cross-paradigm execution fabric linking hybrid AI, concurrent CSP, and spatial dataflow.*
- [Linda Tuple Space Simulator](reconstructions/tuple-space/) — *An interactive [generative communication](GLOSSARY.md) engine implementing associative pattern-matching and coordinate-free parallel processing.*
- [Stochastic Computing Simulator](reconstructions/stochastic-computing/) — *An interactive probabilistic execution engine implementing unipolar/bipolar logic gate arithmetic, saturating FSM-based activations, and LFSR random generation.*
- [Cryogenic Superconducting Simulator](reconstructions/cryogenic-superconducting/) — *Picosecond-accurate Rapid Single Flux Quantum (RSFQ) pulse logic timing and thermodynamic cooling penalty simulator.*
- [Neuromorphic Spiking Simulator](reconstructions/neuromorphic-spiking/) — *An event-driven SNN routing simulator modeling Leaky Integrate-and-Fire (LIF) dynamics and STDP learning rules.*
- [Cursor IDE Substrate & Agentic Workspace Simulator](reconstructions/cursor_ide/) — *A zero-dependency Python reconstruction simulating budgeted context packet assembly, speculative diff patch generation/approval checkpoints, and supervised agent self-correcting tool loops.*
- [OpenAI Assistants Thread & Tool Run Loop Simulator](reconstructions/openai_sim/) — *An interactive agentic runtime executing turn-based ChatML tokenizer frames, stateful server-managed threads, and schema-validated tool output run steps.*
- [Constraint Migration Predictive Hypothesis Engine](reconstructions/predictive-hypothesis/) — *A Python-based forecasting tool that maps historically sidelined architectural failures to emerging post-CMOS physical limits, predicting their revival potential.*
- [RNS Arithmetic Simulator](reconstructions/rns-arithmetic/) — *Parallel, carry-free componentwise modular addition/multiplication and Chinese Remainder Theorem decoding.*
- [LNS Arithmetic Simulator](reconstructions/lns-arithmetic/) — *Logarithmic encoding/decoding, multiplication/division, and Jacobian log adder.*
- [KeyKOS-style Capability Simulator](reconstructions/keykos-capabilities/) — *Unforgeable keys, attenuation, message-invocation routing, and continuous orthogonal persistence.*
- [llama.cpp Local Quantization and GGUF Simulator](reconstructions/llama_cpp/) — *A high-fidelity simulator demonstrating aligned [GGUF](GLOSSARY.md) container packing/unpacking, block-wise Q4_0 integer quantization, dequantization-on-the-fly matrix multiplications, and autoregressive KV-cache tracking.*
- [MapReduce Distributed Compute Simulator](reconstructions/mapreduce/) — *Fault-tolerant MapReduce coordinator executing functional partitioning, intermediate shuffling, key hashing, and map-task recovery on node failure.*
- [x86 Microcode µop & Platform Architecture Simulator](reconstructions/x86_uop_translation/) — *CISC macro-instruction microcode decoding into RISC µops, [CPUID](GLOSSARY.md) feature negotiation, and multi-mode memory address translation.*
- [Apple Metal Command & UMA Simulator](reconstructions/apple_metal/) — *Low-overhead explicit command encoding, immutable pipeline state objects, TBDR load/store actions, and explicit UMA memory storage modes.*
- [C++ RAII & Zero-Overhead Dispatch Simulator](reconstructions/cpp_raii/) — *Interactive simulator modeling scope-bound RAII resource cleanup, exception stack unwinding, static template monomorphization vs. vtable dynamic dispatch metrics, and iterator contracts.*
- [NVIDIA SIMT Microarchitecture Simulator](reconstructions/nvidia_simt/) — *[Warp](GLOSSARY.md)-level SIMT execution, branch divergence mask stacks, [warp](GLOSSARY.md) scheduler latency hiding, shared memory bank conflicts, [Tensor Core](GLOSSARY.md) WMMA matrix operations, and Unified Memory page migration.*
- [Winamp Plugin Host & Pipeline Simulator](reconstructions/winamp_plugin_host/) — *C-ABI plugin jump-tables, decoupled audio pipelines (Input/DSP/Output), classic skin sprite mapping, and M3U/PLS media library indexing.*
- [FFmpeg Pipeline & CLI Translator Simulator](reconstructions/ffmpeg_pipeline/) — *5-stage transcode pipeline (demux/decode/filter/encode/mux), `AVPacket`/`AVFrame` reference-counted buffer flow, filter graph execution, and CLI command translator.*
- [Netscape Browser Runtime & Network Client Simulator](reconstructions/netscape_browser_runtime/) — *DOM event-driven JS host, Same-Origin Policy (SOP), NPAPI plugin dispatcher, HTTP cookie session state, and SSL/TLS certificate trust evaluation.*
- [Safari & WebKit Runtime Simulator](reconstructions/safari_webkit_runtime/) — *WebKit2 multi-process IPC message passing, [WKWebView](GLOSSARY.md) host app process insulation, and Intelligent Tracking Prevention (ITP) double-keyed storage partitioning.*
- [Qt Meta-Object & Signals Simulator](reconstructions/qt_meta_object_signals/) — *`QObject` parent-child ownership trees, Meta-Object Compiler introspection metadata, type-safe signals/slots dispatch, central event loop, and QML reactive property bindings.*
- [Portage Engine & USE-Flag Simulator](reconstructions/gentoo_portage/) — *Cascading profile policy inheritance, USE flag dependency graph mutation, slotting, LD_PRELOAD build sandboxing, and Var Database (VDB) tracking.*
- [IBM AS/400 TIMI & Single-Level Store Simulator](reconstructions/ibm_as400_timi/) — *TIMI instruction representation, AOT CISC/RISC retranslation engine, Single-Level Store paging, and DB2 physical/logical file access.*
- [Solaris Core Subsystems Simulator](reconstructions/solaris_subsystems/) — *DTrace DIF safety verification & probe firing, SMF dependency resolution & restarter state machine, ZFS Copy-on-Write Merkle tree integrity & snapshots, and Zone process isolation & FSS resource controls.*
- [Model Context Protocol Simulator](reconstructions/model_context_protocol/) — *JSON-RPC 2.0 host-server session handshakes, capability negotiation, JSON Schema tool validation gates, URI resource reading, prompt templates, and multi-server tool multiplexing.*

---

## Interactive Playgrounds & Academic Materials

- **Interactive Playground:** [Interactive Pyodide & WebAssembly Simulator Playground](playground.html)
- **Academic Lab Manual:** [Pedagogical Lab Modules & Clean-Slate Architecture Challenges](reconstructions/LAB_MANUAL.md)
- **Interactive Explorer:** [Interactive Visual Taxonomy Explorer](explorer.html)
- **Glossary & Taxonomy:** [Glossary & Abstraction Taxonomy](GLOSSARY.md)
- **Comparative Indexes:** [Index by Execution, Memory, and Concurrency Models](COMPARATIVE_INDEX.md)
- **Timelines:** [Computing](timelines/computing.md) | [Hardware](timelines/hardware.md) | [AI](timelines/ai.md)
- **Bibliography:** [Books](bibliography/books.md) | [Papers](bibliography/papers.md) | [Archives](bibliography/archives.md)

---

> *Track active research directions and roadmap progress in [ROADMAP.md](ROADMAP.md).*

---

**Last updated**: August 2, 2026
