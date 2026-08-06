# Changelog

All notable changes to the Digital Archaeology repository will be documented in this file.

## [Neuromorphic & Stochastic Deepening] - August 2026

### Added
- **Neuromorphic Spiking SNN Simulator**: Developed a stateful, zero-dependency, event-driven spiking neural network simulator under `reconstructions/neuromorphic-spiking/spiking_sim.py`. Models Leaky Integrate-and-Fire (LIF) neural dynamics, Address-Event Representation (AER) packet logging, and Spike-Timing-Dependent Plasticity (STDP) learning rules.
- **Synthesizable Stochastic Multiplier soft-core**: Added a synthesizable, sequential registered `stochastic_multiplier.sv` SystemVerilog module combining an 8-bit LFSR pseudo-random bit source, comparator-based unipolar generation, and 1-gate AND multiplication.
- **Pedagogical Spiking & Stochastic Lab**: Integrated **Lab Module 7** to `reconstructions/LAB_MANUAL.md` covering LIF neural integration challenges and unipolar multiplier precision/latency trade-offs.

### Improved
- **Stochastic Computing Simulator Expansion**: Upgraded `reconstructions/stochastic-computing/stochastic_sim.py` with multi-input stochastic artificial neuron and 1-D moving-average smoothing filter workloads. Added a quantitative accuracy-vs-energy proxy (active CMOS logic gate transitions) trade-off evaluation comparing stochastic multipliers with standard 8-bit binary multipliers.
- **Sourced Historical Documentation**:
  - Deepened `excavations/neuromorphic-hardware.md` with MOSFET subthreshold exponential physics, ASCII diagrams of LIF neuron and AER routing mechanics, and a detailed comparison table of historical metrics (IBM TrueNorth, Stanford Neurogrid, Heidelberg BrainScaleS, Manchester SpiNNaker, Intel Loihi).
  - Deepened `excavations/stochastic-computing.md` with Gaines' saturating state counter FSM activation math, unipolar/bipolar SCG comparator diagrams, and historical metrics (Gaines' ADDIE, RASCEL).
- **Relational Density & scorecards**: Integrated the Neuromorphic & Stochastic cluster as the 5th scored lineage inside `modern-relevance/revival-readiness.md`. Strengthened bidirectional links from excavations to `patterns/constraint-migration.md`, `modern-relevance/ai.md`, and `synthesis/return-of-spatial-computing.md`. Updated the top-of-README simulator index to 13 simulators and featured new co-processor paths in `using-this-repo.md`.

## [Consolidation & Usability] - August 2026

### Added
- **Analytical Architect Guide**: Created `modern-relevance/using-this-repo.md` detailing concrete application paths of excavations, simulators, and RTL blueprints to contemporary accelerator, security processor, and distributed runtime designs.
- **Synthesizable Soft-Core Documentation**: Added a comprehensive `reconstructions/synthesizable-hardware/README.md` providing Lattice iCE40 UP5K and Tiny-Tapeout layout paths, clock frequencies, and RTL simulation instructions.

### Improved
- **Knowledge-Graph & Explorer Synchronization**: Enhanced `tools/generate_knowledge_graph.py` to recursively parse and map the 7 comparative synthesis essays (including the Revival Readiness Scorecard) and all 12 zero-dependency reconstructions/simulators.
- **Top-of-README Navigation**: Completely redesigned the top of `README.md` with a <60-second summary of the four key deepened lineages, a dynamic simulator table, and role-based "Start Here" pathways.
- **Strict Quality Gates**: Integrated strict link and anchor checks, ensuring the complete documentation site builds flawlessly with zero warnings or errors using `mkdocs build --strict`.

### Future Gaps & Next-Iteration Targets
The highest-value remaining gaps for the next iteration of the Digital Archaeology initiative include:
1. **Formal Verification of Soft-Cores**: Extending our SystemVerilog verification suite with formal mathematical proofs (e.g., using SymbiYosys) to rigorously guarantee capability and bounds isolation on the capability bounds checker RTL.
2. **Deepening Physical Lineages**: Expanding physical and alternative-mathematics excavations with deeper models of neuromorphic spike-routing mesh networks and continuous stochastic hardware coprocessors.
3. **Academic Outreach & Lab Integration**: Developing standardized lecture slides, auto-grading harnesses, and lab companion guides to facilitate full course integration of the 6 lab modules into university systems architecture curricula.

---

## [Unreleased] - August 2026

### Added
- **9P Distributed Resource Namespace & Message Protocol Simulator**: Developed a zero-dependency, connection-oriented, stateful 9P protocol simulator under `reconstructions/plan9-9p/namespace_sim.py`. Supports standard transaction messages (`Tversion`, `Tattach`, `Twalk`, `Topen`, `Tread`, `Twrite`, `Tcreate`, `Tclunk`) mapped directly to hierarchical FileNode directories. Features dynamic per-process private namespaces and dynamic fallback union mounts. Fully unit tested in `reconstructions/plan9-9p/test_namespace_sim.py`.
- **Pedagogical Namespace Lab Module**: Integrated **Lab Module 6** to `reconstructions/LAB_MANUAL.md` covering distributed namespaces, union directory mounts, and 9P protocol messages with a complete model solution.
- **Reversible Logic & Thermodynamic Energy Simulator**: Developed an interactive physical simulator inside `reconstructions/analog-optical/analog_optical_sim.py` featuring Toffoli, CNOT, and Fredkin logic gates, Bennett's 3-phase uncomputation strategy tracking, and quantitative modeling of the Landauer erasure limit ($k_B T \ln 2$) vs. adiabatic dynamic charge recovery ($E = \frac{RC}{T_{\text{ramp}}} C V^2$) at 300K room temp and 4K cryogenic bounds. Fully unit tested in `test_analog_optical_sim.py`.
- **Synthesizable Reversible Gate Core**: Created a synthesizable SystemVerilog module `reconstructions/synthesizable-hardware/reversible_gates.sv` defining a 3-bit Toffoli CCNOT and CSWAP Fredkin gate with sequential registered interfaces, and verified correctness via golden-model checks in `test_synthesizable.py`.
- **Modern Revival Readiness Scorecard**: Introduced `modern-relevance/revival-readiness.md` defining a transparent scoring rubric across CMS, SR, SEF, EA, and AIS criteria to compare spatial, capability/tagged, and physical-optical post-CMOS lineages.
- **Dynamic Type Checked Lisp Word Simulator**: Added `LispWord` to `reconstructions/capability-security/capability_sim.py` supporting dynamic type tags (`Fixnum`, `Flonum`, `Symbol`) and CDR-coding sequential list traversals, enabling realistic simulation of Lisp Machine hardware architectures.
- **Burroughs B5000-Style Descriptor Memory Checks**: Added `DescriptorWord` and presence-bit checking to `reconstructions/capability-security/capability_sim.py`, simulating virtual memory page faults, write-protection, and descriptor-mediated bounds verification.
- **Systolic Array Cycle-Accurate Simulator**: Added a zero-dependency spatial simulation engine at `reconstructions/systolic-array/systolic_sim.py` supporting both Weight-Stationary and Output-Stationary execution dataflows. Features cycle-by-cycle logic execution, interconnect hop counting, and customizable CMOS energy proxy reporting. Complete with full unit test coverage in `test_systolic_sim.py`.
- **Multi-Trit Balanced Ternary Instruction Set ALU**: Implemented `TernaryALU` in `reconstructions/mixed-radix-sim/ternary_sim.py` simulating standard register operations (`LOAD`, `ADD`, `SUB`, `MUL`, `NEG`, `NOT`, `AND`, `OR`, `SHL`, `SHR`) with natural rounded-to-nearest right-shifts. Added extensive verification tests in `test_ternary_sim.py`.
- **Parallel Dataflow Benchmark Suite**: Integrated fully parallel vector dot-product (`run_vector_dot_product`) and 2x2 matrix multiplication (`run_matrix_multiply_2x2`) benchmarks into `reconstructions/dataflow-engine/dataflow_sim.py`, complete with cycle and token-matching performance counters and unit test validation.
- **Advanced Capability Safety Scenarios**: Developed Scenario 4 (Confused Deputy Attack vs. POLA Capability Defense) and Scenario 5 (Fine-grained Privilege Attenuation and Revocation via Gates) inside `reconstructions/capability-security/capability_sim.py`. Added corresponding unit tests in `test_capability_sim.py` covering hardware performance counters and revocation.

### Improved
- **Deepened Distributed OS Lineage Excavations**:
  - `excavations/plan-9.md`: Extensively expanded historical context of AT&T Bell Labs Computing Science Research releases, CPU servers, file servers (WORM), and terminal nodes. Included detailed ASCII/Mermaid dynamic routing, 9P protocol transaction sequences (Twalk, Tread, Twrite), Dynamic Union Mounts, and modern container/WSL2 evaluations.
  - `excavations/multics.md`: Fully documented Project MAC (MIT/GE/Bell Labs) historical context, PL/I systems programming, NCSC B2 Orange Book security rating, and Honeywell 6180 hardware mmus. Visualized concentric hardware ring protection (Rings 0-7), gates, and Segmented virtual memory/Single-Level Store (SLS) persistent addresses.
  - `excavations/inferno.md`: Documented Lucent Technologies (1995) embedded VM push, Vita Nuova acquisitions, register-based Dis virtual machine registers, Limbo CSP concurrent channels, deterministic reference-counting memory cleanup, and modern WebAssembly evaluations.
- **Deepened Thermodynamic, Optical and Analog Computing Excavations**:
  - `excavations/analog-computing.md`: Deepened historical context of differential analyzers, electronic op-amps, and modern In-Memory analog GEMM matrix accelerators. Expanded standard 6-category scorecard.
  - `excavations/optical-computing.md`: Documented Clements and Reck MZI meshes for optical matrix acceleration, wave speed propagation limits, and co-packaged optics (CPO). Expanded standard scorecard.
  - `excavations/reversible-computing.md`: Expanded thermodynamic limits ($E = k_B T \ln 2$), uncomputation pipeline mathematics, and adiabatic charge-recovery dynamic energy equations ($E = \frac{RC}{T_{\text{ramp}}} C V^2$). Expanded standard scorecard.
- **Academic Lab Manual & Pedagogical Sandboxes**:
  - Added **Lab Module 5** to `reconstructions/LAB_MANUAL.md` covering Reversible Logic, Landauer Limits, and Adiabatic Charge Recovery calculations, complete with model solution and verification checks.
- **Deepened Security and Tagged Memory Excavations**:
  - `excavations/lisp-machines.md`: Extensively expanded historical details on MIT CONS, CADR, Symbolics 3600 (40-bit words), and Symbolics Ivory VLSI microprocessors (~110,000 transistors). Visualized word structures, CDR-coding compression, and generational write barriers for Ephemeral Garbage Collection (EGC).
  - `excavations/intel-iapx-432.md`: Documented three-chip HMOS architecture (43201/02/03), 2-level object reference mappings (Access Descriptor -> Object Table -> Segment Base/Limit), and variable-length bit-aligned instruction decoders. Mapped to CHERI and seL4 microkernels.
  - `excavations/burroughs-large-systems.md`: Grounded in Barton's design philosophy, B6500 51-bit words with 3-bit hardware tags, array boundary checking, and recursive display registers. Visualized stack-based evaluations and descriptor-mediated memory safety.
- **SystemVerilog Soft-Core Hardening**:
  - `reconstructions/synthesizable-hardware/capability_bounds_checker.sv`: Hardened with a `desc_mode` control select and a `cap_present` (presence-bit) input to natively support descriptor-style checks and VM page-fault triggers. Updated python verification.
- **Academic Lab Manual Deepening**:
  - `reconstructions/LAB_MANUAL.md`: Expanded Lab Module 3 with two new graduate-level hands-on challenges (Challenge 3B on Lisp dynamic typing and Challenge 3C on Burroughs descriptor page fault recovery).
- **Deepened Spatial & Parallel Excavations**:
  - `excavations/systolic-arrays.md`: Greatly expanded historical specifications of Carnegie Mellon Warp (100 MFLOPS, Weitek FP chips) and Intel-CMU iWarp (1.2-micron CMOS, 20 MFLOPS/node, 320 MB/s links), illustrated detailed Weight-Stationary and Output-Stationary ASCII/Mermaid structures, and discussed Google TPU and GPU Tensor Core design lineages.
  - `excavations/connection-machine.md`: Grounded in Danny Hillis's MIT dissertation, providing specific metrics on CM-1 (65,536 1-bit nodes, 4 MHz, 32 MB RAM), CM-2 (Weitek FPU accelerators, 2.5 GFLOPS peak), and CM-5 (SPARC cores, fat-tree MIMD topology). Mapped dynamic packet routing, the Virtual Processor Ratio (VPR), and processing-in-memory to modern SIMT and wafer-scale architectures.
  - `excavations/transputers.md`: Fully documented INMOS T414 (15 MIPS), T800 (FPU-on-die, 1.5-micron, 250k transistors), and T9000 milestones. Highlighted the microcoded low/high priority hardware multitasking scheduler, internal/external zero-copy channel rendezvous mechanisms, and the elegant occam compiler CSP-to-silicon co-design. Mapped concepts to Go channels, Erlang actors, and modern Networks-on-Chip (NoC).
- **Relational Density & Bidirectional Linking**: Strengthened link intersections from excavations to spatial computing, AI, and FPGA relevance files (`synthesis/return-of-spatial-computing.md`, `patterns/constraint-migration.md`, `modern-relevance/ai.md`, `modern-relevance/fpga.md`, and `synthesis/capability-based-security.md`).
- **Knowledge Graph Synchronization**: Regrouped headings to ensure regular expression compliance, enabling full dynamic extraction of modern relevance paragraphs in `modern-relevance/knowledge_graph.json` without blanking out nodes.
