# Modern Reconstructions & Simulators

> *Active software reconstructions, synthesizable hardware blueprints, and executable models translating historical computing paradigms into modern, runnable environments.*

---

## Overview

Welcome to the **Digital Archaeology Reconstructions & Simulators** directory. The repository features zero-dependency Python simulators, synthesizable SystemVerilog hardware cores, and multi-architecture co-simulation fabrics.

Each subdirectory here contains an interactive, fully-functional simulator, synthesizable hardware module, or orchestrator, accompanied by comprehensive unit tests (`pytest`).

---

## Table of Reconstructions & Hardware Blueprints

### 1. [Balanced Ternary & Mixed-Radix Simulator](mixed-radix-sim/)
* **Focus**: Alternative arithmetic, non-binary logic.
* **Paradigm**: [Balanced Ternary](../excavations/balanced-ternary.md) (Setun-style).
* **What it does**: Implements trit-level [balanced ternary](../excavations/balanced-ternary.md) logic, multi-trit addition, and multiplication.
* **Entry point**: `reconstructions/mixed-radix-sim/ternary_sim.py`

### 2. [Dynamic Token-Matching Dataflow Engine](dataflow-engine/)
* **Focus**: Asynchronous spatial execution, non-von Neumann control flow.
* **Paradigm**: [Dataflow Computing](../excavations/dataflow-computing.md) (MIT Tagged-Token style).
* **What it does**: Implements a parallel token-matching execution engine firing nodes asynchronously.
* **Entry point**: `reconstructions/dataflow-engine/dataflow_sim.py`

### 3. [Capability-Based Memory Protection Emulator](capability-security/)
* **Focus**: Hardware-enforced object capabilities and micro-segmentation.
* **Paradigm**: [Capability Systems](../excavations/capability-systems.md) (Burroughs, CHERI-style).
* **What it does**: Simulates CPU and RAM utilizing [tagged memory](../GLOSSARY.md), bounds checking, and domain transitions.
* **Entry point**: `reconstructions/capability-security/capability_sim.py`

### 4. [Neuro-Symbolic Logic Inference Solver](neuro-symbolic/)
* **Focus**: Hybrid AI, structured reasoning under uncertainty.
* **Paradigm**: [Symbolic AI](../excavations/symbolic-ai.md) & [Symbolic Computing](../modern-relevance/symbolic-computing.md).
* **What it does**: Connects statistical classifier confidence scores with a formal forward-chaining symbolic engine.
* **Entry point**: `reconstructions/neuro-symbolic/neuro_symbolic_sim.py`

### 5. [CSP Synchronous Messaging Simulator](csp-messaging/)
* **Focus**: Rendezvous communication, ALT-based multiplexing, deadlock detection.
* **Paradigm**: [Occam](../excavations/occam.md) & [Transputers](../excavations/transputers.md).
* **What it does**: Implements a cooperative scheduler running parallel processes over synchronous unbuffered channels.
* **Entry point**: `reconstructions/csp-messaging/csp_sim.py`

### 6. [Continuous Analog & Optical Wave Accelerator Simulator](analog-optical/)
* **Focus**: Continuous-physical computation, MZI photonic [tensor core](../GLOSSARY.md) wave propagation.
* **Paradigm**: [Analog Computing](../excavations/analog-computing.md) & [Optical Computing](../excavations/optical-computing.md).
* **What it does**: Models a continuous op-amp computer and a Mach-Zehnder Interferometer photonic [tensor core](../GLOSSARY.md).
* **Entry point**: `reconstructions/analog-optical/analog_optical_sim.py`

### 7. [Synthesizable Hardware IP Core Blueprints](synthesizable-hardware/)
* **Focus**: Synthesizable soft-cores and hardware-enforced microarchitectural security.
* **Paradigm**: [Balanced Ternary](../excavations/balanced-ternary.md) and [Capability Systems](../excavations/capability-systems.md).
* **What it does**: Contains SystemVerilog models of a 3-trit [Balanced Ternary](../excavations/balanced-ternary.md) ALU and Tagged RAM Capability Bounds Checker.
* **Entry point**: `reconstructions/synthesizable-hardware/`

### 8. [Multi-Architecture Co-Simulation & Interoperability Fabric](co-simulation/)
* **Focus**: Cross-paradigm sandbox routing and multi-architecture co-simulation.
* **Paradigm**: Concurrent actor messaging (CSP), Spatial Dataflow, and Hybrid AI.
* **What it does**: Orchestrates cross-paradigm messaging between neural classifiers, CSP processes, and dataflow graphs.
* **Entry point**: `reconstructions/co-simulation/orchestrator.py`

### 9. [Linda Tuple Space Simulator](tuple-space/)
* **Focus**: Coordinate-free parallel coordination, [generative communication](../GLOSSARY.md).
* **Paradigm**: [Linda Tuple Spaces](../excavations/linda-tuple-spaces.md).
* **What it does**: Implements a thread-safe, associative [tuple space](../GLOSSARY.md) with matching pattern evaluation.
* **Entry point**: `reconstructions/tuple-space/tuple_space_sim.py`

### 10. [Constraint Migration Predictive Hypothesis Engine](predictive-hypothesis/)
* **Focus**: [Constraint migration](../patterns/constraint-migration.md) forecasting and architectural projection.
* **Paradigm**: [Constraint Migration](../patterns/constraint-migration.md) & [Recurring Ideas](../patterns/recurring-ideas.md).
* **What it does**: Models how shifting physical and economic constraints influence alternative computing lineages.
* **Entry point**: `reconstructions/predictive-hypothesis/predictive_engine.py`

### 11. [Stochastic Computing Simulator](stochastic-computing/)
* **Focus**: Probabilistic stream arithmetic and noise-tolerant computation.
* **Paradigm**: [Stochastic Computing](../excavations/stochastic-computing.md).
* **What it does**: Implements bitstream multiplication via AND/XOR gates, LFSR generation, and saturating FSMs.
* **Entry point**: `reconstructions/stochastic-computing/stochastic_sim.py`

### 12. [Cryogenic Superconducting Simulator](cryogenic-superconducting/)
* **Focus**: Picosecond pulse logic and thermal dissipation modeling.
* **Paradigm**: [Superconducting & Cryogenic Microarchitectures](../excavations/superconducting-cryogenic.md).
* **What it does**: Simulates RSFQ pulse logic timing and thermodynamic cooling penalties.
* **Entry point**: `reconstructions/cryogenic-superconducting/sfq_sim.py`

### 13. [Plan 9 Namespace Simulator](plan9-9p/)
* **Focus**: Stateful [9P protocol](../GLOSSARY.md) and process-private namespaces.
* **Paradigm**: [Plan 9](../excavations/plan-9.md) & [Inferno](../excavations/inferno.md).
* **What it does**: Simulates 9P/Styx transactions, dynamic union directory mounts, and location transparency.
* **Entry point**: `reconstructions/plan9-9p/namespace_sim.py`

### 14. [Systolic Array Simulator](systolic-array/)
* **Focus**: Weight-Stationary and Output-Stationary matrix multiplication dataflows.
* **Paradigm**: [Systolic Arrays](../excavations/systolic-arrays.md).
* **What it does**: Cycle-accurate grid array multiplier with CMOS energy proxy metrics.
* **Entry point**: `reconstructions/systolic-array/systolic_sim.py`

### 15. [Neuromorphic Spiking Simulator](neuromorphic-spiking/)
* **Focus**: Spiking neural network routing and event-driven computation.
* **Paradigm**: [Neuromorphic Hardware](../excavations/neuromorphic-hardware.md).
* **What it does**: Simulates LIF dynamics, Address-Event Representation (AER), and STDP plasticity.
* **Entry point**: `reconstructions/neuromorphic-spiking/spiking_sim.py`

### 16. [Residue Number System (RNS) Simulator](rns-arithmetic/)
* **Focus**: Carry-free parallel arithmetic over coprime moduli sets.
* **Paradigm**: [Residue Number System](../excavations/residue-number-system.md).
* **What it does**: Performs componentwise modular arithmetic and Chinese Remainder Theorem (CRT) decoding.
* **Entry point**: `reconstructions/rns-arithmetic/rns_sim.py`

### 17. [Logarithmic Number System (LNS) Simulator](lns-arithmetic/)
* **Focus**: Signed base-b logarithmic math and non-linear addition/subtraction.
* **Paradigm**: [Logarithmic Number System](../excavations/logarithmic-number-system.md).
* **What it does**: Inverts multiply/divide into add/subtract and models Jacobian log table lookup interpolation.
* **Entry point**: `reconstructions/lns-arithmetic/lns_sim.py`

### 18. [KeyKOS Capability Simulator](keykos-capabilities/)
* **Focus**: Pure object-capability security and Continuous Orthogonal Persistence.
* **Paradigm**: [KeyKOS & Nanokernel Capabilities](../excavations/keykos-nanokernel-capabilities.md).
* **What it does**: Models unforgeable key invocation, attenuation, message routing, and checkpoint persistence.
* **Entry point**: `reconstructions/keykos-capabilities/keykos_sim.py`

### 19. [Cursor IDE Substrate Simulator](cursor_ide/)
* **Focus**: AI-native workspace substrate, context budgeting, and spec-diff patch previews.
* **Paradigm**: [Cursor IDE](../excavations/cursor-ide.md).
* **What it does**: Simulates context packet assembly, multi-mode autonomy gradients, and tool self-correction loops.
* **Entry point**: `reconstructions/cursor_ide/cursor_sim.py`

### 20. [llama.cpp Quantization & GGUF Simulator](llama_cpp/)
* **Focus**: Low-bit integer quantization and local memory-bandwidth-aware inference.
* **Paradigm**: [llama.cpp](../excavations/llama-cpp.md).
* **What it does**: Simulates [GGUF](../GLOSSARY.md) container packing/unpacking, block-wise Q4_0 quantization, and on-the-fly GEMV.
* **Entry point**: `reconstructions/llama_cpp/llama_cpp_sim.py`

### 21. [MapReduce Distributed Compute Simulator](mapreduce/)
* **Focus**: Datacenter scale data partitioning, intermediate key sorting, and fault recovery.
* **Paradigm**: [Google Platform Machine](../excavations/google.md).
* **What it does**: Simulates functional Map/Reduce phases, master-coordinated retry, and worker crash recovery.
* **Entry point**: `reconstructions/mapreduce/mapreduce_sim.py`

### 22. [x86 Microcode µop Translation Simulator](x86_uop_translation/)
* **Focus**: CISC instruction microcode decoding into RISC µops and multi-mode address translation.
* **Paradigm**: [Intel Architecture](../excavations/intel.md).
* **What it does**: Simulates macro-instruction decoding, [CPUID](../GLOSSARY.md) feature negotiation, and Real/Protected/Long mode translation.
* **Entry point**: `reconstructions/x86_uop_translation/x86_uop_sim.py`

### 23. [Apple Metal Command & UMA Storage Simulator](apple_metal/)
* **Focus**: Explicit command encoding, immutable pipeline states, and TBDR load/store actions.
* **Paradigm**: [Apple Metal Architecture](../excavations/apple-metal.md).
* **What it does**: Simulates low-overhead encoders, TBDR tile memory interactions, and explicit UMA storage modes.
* **Entry point**: `reconstructions/apple_metal/metal_sim.py`

### 24. [C++ RAII & Zero-Overhead Dispatch Simulator](cpp_raii/)
* **Focus**: Scope-bound resource allocation, exception unwinding, and template monomorphization.
* **Paradigm**: [C++ Systems Lineage](../excavations/cpp.md).
* **What it does**: Simulates RAII cleanup, stack unwinding, static template vs vtable overhead metrics, and iterator contracts.
* **Entry point**: `reconstructions/cpp_raii/cpp_raii_sim.py`

### 25. [NVIDIA SIMT Microarchitecture Simulator](nvidia_simt/)
* **Focus**: [Warp](../GLOSSARY.md) lockstep execution, active mask divergence stacks, and [Tensor Core](../GLOSSARY.md) WMMA matrix math.
* **Paradigm**: [NVIDIA Architecture & CUDA](../excavations/nvidia.md).
* **What it does**: Simulates 32-lane [warp](../GLOSSARY.md) execution, branch divergence handling, bank conflicts, and Unified Memory page migration.
* **Entry point**: `reconstructions/nvidia_simt/simt_sim.py`

### 26. [Winamp Plugin Host & Audio Pipeline Simulator](winamp_plugin_host/)
* **Focus**: C-ABI jump tables, decoupled audio processing, and declarative UI skinning.
* **Paradigm**: [Winamp](../excavations/winamp.md).
* **What it does**: Simulates In/DSP/Out module plugin dispatching, bitmap sprite rendering, and playlist indexing.
* **Entry point**: `reconstructions/winamp_plugin_host/winamp_sim.py`

### 27. [Netscape Browser Runtime Simulator](netscape_browser_runtime/)
* **Focus**: Event-driven JS host, Same-Origin Policy (SOP), and NPAPI plugin dispatching.
* **Paradigm**: [Netscape](../excavations/netscape.md).
* **What it does**: Models DOM event handling, SOP security boundaries, cookie management, and SSL certificate validation.
* **Entry point**: `reconstructions/netscape_browser_runtime/netscape_sim.py`

### 28. [Safari & WebKit Runtime Simulator](safari_webkit_runtime/)
* **Focus**: WebKit2 multi-process IPC, [WKWebView](../GLOSSARY.md) insulation, and Intelligent Tracking Prevention.
* **Paradigm**: [Safari](../excavations/safari.md).
* **What it does**: Simulates multi-process message passing, host app insulation, and double-keyed storage partitioning.
* **Entry point**: `reconstructions/safari_webkit_runtime/safari_sim.py`

### 29. [Qt Meta-Object & Signals Simulator](qt_meta_object_signals/)
* **Focus**: QObject parent-child trees, Meta-Object Compiler (`moc`) metadata, and Signals/Slots.
* **Paradigm**: [Qt Meta-Object Runtime](../excavations/qt.md).
* **What it does**: Simulates dynamic property reflection, type-safe signals/slots dispatch, and QML binding evaluation.
* **Entry point**: `reconstructions/qt_meta_object_signals/qt_sim.py`

### 30. [Gentoo Portage Engine & USE-Flag Simulator](gentoo_portage/)
* **Focus**: Cascading profile policy inheritance, USE flag graph mutation, and build sandboxing.
* **Paradigm**: [Gentoo](../excavations/gentoo.md) & [Portage](../excavations/portage.md).
* **What it does**: Simulates profile inheritance, dependency graph resolution under [USE flags](../GLOSSARY.md), slotting, and VDB tracking.
* **Entry point**: `reconstructions/gentoo_portage/portage_sim.py`

### 31. [OpenAI Agentic Platform Simulator](openai_sim/)
* **Focus**: ChatML tokenization, stateful server-managed threads, and schema-validated tool run loops.
* **Paradigm**: [OpenAI Platform Substrate](../excavations/openai.md).
* **What it does**: Simulates turn-based ChatML frames, thread message execution runs, and dynamic tool schema invocation.
* **Entry point**: `reconstructions/openai_sim/openai_sim.py`

### 32. [IBM AS/400 TIMI & Single-Level Store Simulator](ibm_as400_timi/)
* **Focus**: Technology Independent Machine Interface (TIMI), AOT CISC/RISC retranslation, Single-Level Store, and DB2 files.
* **Paradigm**: [IBM AS/400](../excavations/ibm-as400.md).
* **What it does**: Simulates TIMI compilation, dynamic SLIC retranslation across CISC/RISC, SLS paging, capability pointers, and DB2 physical/logical files.
* **Entry point**: `reconstructions/ibm_as400_timi/as400_sim.py`

### 33. [Solaris Core Subsystems Simulator](solaris_subsystems/)
* **Focus**: Dynamic tracing (DTrace), dependency-aware service supervision (SMF), copy-on-write pooled storage (ZFS), and OS container virtualization (Zones).
* **Paradigm**: [Solaris Operating System](../excavations/solaris.md).
* **What it does**: Simulates DTrace DIF bytecode verifier and probe firing, SMF topological dependency boot and auto-restarter, ZFS Copy-on-Write Merkle tree checksum verification and snapshots, and Zone process isolation with Fair Share Scheduler (FSS) CPU capping.
* **Entry point**: `reconstructions/solaris_subsystems/solaris_sim.py`

### 34. [FFmpeg Transcode Pipeline & CLI Translator Simulator](ffmpeg_pipeline/)
* **Focus**: 5-stage transcode dataflow, `AVPacket`/`AVFrame` reference counting, filter graph execution, and CLI command translation.
* **Paradigm**: [FFmpeg Substrate](../excavations/ffmpeg.md).
* **What it does**: Simulates packet/frame flow across demuxer, decoder, filter graph, encoder, and muxer, codec capability table lookup, DAG filter processing, and CLI command parsing.
* **Entry point**: `reconstructions/ffmpeg_pipeline/ffmpeg_sim.py`

### 35. [ONNX IR & Graph Runtime Simulator](onnx-ir/)
* **Focus**: Intermediate representation, versioned Opset broadcasting, operator fusion, and execution provider partitioning.
* **Paradigm**: [ONNX Substrate](../excavations/onnx.md).
* **What it does**: Simulates ONNX model IR loading, Opset 6 vs 15 broadcasting, constant folding, Gemm-Relu fusion, and CPU/TensorRT Execution Provider partitioning.
* **Entry point**: `reconstructions/onnx-ir/onnx_sim.py`

---

## Running the Simulators & Tests

All simulators are written in standard Python 3 and require no third-party libraries. Run unit tests across all reconstructions using pytest:

```bash
/home/jules/.local/bin/pytest
```
