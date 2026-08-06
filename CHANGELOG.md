# Changelog

All notable changes to the Digital Archaeology repository will be documented in this file.

## [Unreleased] - August 2026

### Added
- **Dynamic Type Checked Lisp Word Simulator**: Added `LispWord` to `reconstructions/capability-security/capability_sim.py` supporting dynamic type tags (`Fixnum`, `Flonum`, `Symbol`) and CDR-coding sequential list traversals, enabling realistic simulation of Lisp Machine hardware architectures.
- **Burroughs B5000-Style Descriptor Memory Checks**: Added `DescriptorWord` and presence-bit checking to `reconstructions/capability-security/capability_sim.py`, simulating virtual memory page faults, write-protection, and descriptor-mediated bounds verification.
- **Systolic Array Cycle-Accurate Simulator**: Added a zero-dependency spatial simulation engine at `reconstructions/systolic-array/systolic_sim.py` supporting both Weight-Stationary and Output-Stationary execution dataflows. Features cycle-by-cycle logic execution, interconnect hop counting, and customizable CMOS energy proxy reporting. Complete with full unit test coverage in `test_systolic_sim.py`.
- **Multi-Trit Balanced Ternary Instruction Set ALU**: Implemented `TernaryALU` in `reconstructions/mixed-radix-sim/ternary_sim.py` simulating standard register operations (`LOAD`, `ADD`, `SUB`, `MUL`, `NEG`, `NOT`, `AND`, `OR`, `SHL`, `SHR`) with natural rounded-to-nearest right-shifts. Added extensive verification tests in `test_ternary_sim.py`.
- **Parallel Dataflow Benchmark Suite**: Integrated fully parallel vector dot-product (`run_vector_dot_product`) and 2x2 matrix multiplication (`run_matrix_multiply_2x2`) benchmarks into `reconstructions/dataflow-engine/dataflow_sim.py`, complete with cycle and token-matching performance counters and unit test validation.
- **Advanced Capability Safety Scenarios**: Developed Scenario 4 (Confused Deputy Attack vs. POLA Capability Defense) and Scenario 5 (Fine-grained Privilege Attenuation and Revocation via Gates) inside `reconstructions/capability-security/capability_sim.py`. Added corresponding unit tests in `test_capability_sim.py` covering hardware performance counters and revocation.

### Improved
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
