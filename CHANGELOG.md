# Changelog

All notable changes to the Digital Archaeology repository will be documented in this file.

## [Phase X: [Constraint Migration](patterns/constraint-migration.md) Predictive Hypothesis Engine & Alternative Hardware Forecasting] - August 2026

### Added
- **Predictive Hypothesis Engine**: Implemented a stateful, zero-dependency Python forecaster under `reconstructions/predictive-hypothesis/predictive_engine.py` mapping emerging nanoscale physical bottlenecks to our 6 core lineages.
- **Dynamic Research Hypotheses Generation**: Added rules for generating rigorous, academic-grade resurrection briefs linking specific physical constraint shifts (e.g., copper resistance scaling, subthreshold gate leakage, security exposure) to [forgotten abstractions](patterns/forgotten-abstractions.md).
- **Argparse CLI Console & JSON Interface**: Created a fully interactive command-line interface with detailed tabular text formatting, star ratings, and standardized JSON export.
- **Pytest Verification Suite**: Added 6 comprehensive unit tests under `reconstructions/predictive-hypothesis/test_predictive_engine.py` validating prediction bounds clamping, input sensitivities, and JSON schema compatibility.

## [Phase IX: Cross-Paradigm Sandbox Verification & Soft-Core Hardening] - August 2026

### Added
- **Runnable Multi-Paradigm Sandbox Experiments**: Developed a comprehensive integration driver and execution script `reconstructions/co-simulation/experiments.py` implementing three high-impact cross-paradigm experiments proposed in the State of Revival synthesis:
  - *Experiment 1: Heterogeneous Cryogenic Systolic Coprocessor*: Wires the cycle-accurate [systolic array](GLOSSARY.md) activity & interconnect metrics directly to Josephson junction switching events and cryogenic refrigeration models at 4.2 K, demonstrating up to a $140\times$ efficiency gain over standard 5 GHz CMOS GPU tiles.
  - *Experiment 2: Reversible Uncomputation in Cryogenic Storage Loops*: Combines adiabatic charge recovery with the cryogenic cooling penalty model to demonstrate absolute Landauer heat erasure avoidance, saving over $3.6\times10^4 \text{ fJ}$ of utility grid power per uncomputed bit at cryogenic scale.
  - *Experiment 3: 9P Sandboxed Execution for Autonomous LLM Agents*: Integrates the [Plan 9](excavations/plan-9.md)/9P private resource namespace server with inline hardware-level Burroughs segmented memory descriptors, validating the block of OOB prompt-injection attacks and triggering proper page faults.
- **Focused Multi-Paradigm Unit Tests**: Added a complete Pytest test suite `reconstructions/co-simulation/test_experiments.py` to continuously verify the correctness, metrics, and security guarantees of all three sandbox experiments.
- **Formal Verification Assertions for Soft-Cores**: Appended inline, SystemVerilog Assertions (SVA) compatible specifications inside `ternary_alu.sv`, `capability_bounds_checker.sv`, `reversible_gates.sv`, and `stochastic_multiplier.sv` representing core physical and safety invariants (reset state, zero-element addition, bounds safety, information conservation, and non-zero LFSR state propagation).
- **Hardened Golden Model Testing**: Added targeted alignment tests to `test_synthesizable.py` mapping reversible uncomputation sequences and segmented virtual memory page fault triggers to physical experiment conditions, and introduced CLI execution test coverage to `test_experiments.py`.

### Improved
- **Single-Command CLI Experiment Runner**: Re-implemented `experiments.py` with an `argparse` CLI supporting `--all` and `--experiment <idx>` parameters. Added customized high-contrast banners, precise metrics tables, and concise, descriptive `[PASS / observed behavior]` summaries for external visitors.
- **Verification Status Disclosure**: Added a dedicated "Verification Status" subsection to `reconstructions/synthesizable-hardware/README.md` identifying test coverage limits, inline assertion structures, and the concrete paths to SymbiYosys formal verification or iCE40 FPGA flashing.
- **Prominent Navigation & Discoverability**:
  - Rewrote the top of `synthesis/state-of-revival.md` to cleanly integrate the three multi-paradigm experiments and reference the executable experiments driver.
  - Added the dynamic experiments to `README.md` and `modern-relevance/using-this-repo.md` as prominent entry points for computer architects and security researchers.
  - Updated `INDEX.md` and rebuilt `modern-relevance/knowledge_graph.json` so that the newly written experiments and academic synthesis modules are indexed as first-class, highly-connected taxonomy nodes.
- **Synthesizable Soft-Core Documentation**:
  - Polished module headers, asynchronous active-low reset styles, and port signal declarations in `capability_bounds_checker.sv`, `ternary_alu.sv`, `reversible_gates.sv`, and `stochastic_multiplier.sv` for clean synthesis in Lattice iCE40 FPGAs and OpenLane ASIC compiler suites.

---

## [Phase VIII: Academic Credibility & Soft-Core Hardening] - August 2026

### Added
- **Academic Research Overview**: Authored `synthesis/digital-archaeology-overview.md` compiling the project's definition, the six core lineages with one-sentence characterizations, core methodological claims ([constraint migration](patterns/constraint-migration.md) and explanatory density), and a BibTeX citation record.
- **Microarchitectural Integration Notes**: Added a detailed section to `reconstructions/synthesizable-hardware/README.md` guiding designers on FPGA/ASIC wrappers, clock/reset inputs, and minimal testbench structures for all four cores.
- **Advanced Golden-Model Tests**: Added 8 advanced, zero-dependency validation tests in `test_synthesizable.py`, verifying the maximal-period properties of the 8-bit LFSR, unipolar stochastic output ratios, exhaustive 1-trit multiplier logic, addition/subtraction overflow conditions, and reversible gate bijectivity.

### Improved
- **Soft-Core Hardening**:
  - `stochastic_multiplier.sv`: Fixed a backtick compiler glitch and added extensive, standard-compliant interface comments.
  - `ternary_alu.sv`, `capability_bounds_checker.sv`, and `reversible_gates.sv`: Standardized interface comments, port signals, and reset/clocking styles.
- **Prominent Navigation & Discoverability**:
  - Linked the Academic Overview prominently in `README.md` (via a dedicated callout and navigation link) and `modern-relevance/using-this-repo.md`.
  - Added the Academic Overview to the navigation panel of `mkdocs.yml`.
  - Audited and updated `INDEX.md` with the new overview and the previously omitted `cryogenic-superconducting` and `neuromorphic-spiking` simulators, ensuring all 14 simulator engines are fully discoverable.
  - Regenerated the machine-readable database `modern-relevance/knowledge_graph.json` to map all new nodes and lineages.
- **Contribution Guidelines**: Lightly updated `CONTRIBUTING.md` with a high-leverage "Highest-value contribution areas" list to guide researchers on formal verification (SVA), physical FPGA bitstream synthesis, and real-world benchmarks.

## [Neuromorphic & Stochastic Deepening] - August 2026

### Added
- **Neuromorphic Spiking SNN Simulator**: Developed a stateful, zero-dependency, event-driven spiking neural network simulator under `reconstructions/neuromorphic-spiking/spiking_sim.py`. Models Leaky Integrate-and-Fire (LIF) neural dynamics, Address-Event Representation (AER) packet logging, and Spike-Timing-Dependent Plasticity (STDP) learning rules.
- **Synthesizable Stochastic Multiplier soft-core**: Added a synthesizable, sequential registered `stochastic_multiplier.sv` SystemVerilog module combining an 8-bit LFSR pseudo-random bit source, comparator-based unipolar generation, and 1-gate AND multiplication.
- **Pedagogical Spiking & Stochastic Lab**: Integrated **Lab Module 7** to `reconstructions/LAB_MANUAL.md` covering LIF neural integration challenges and unipolar multiplier precision/latency trade-offs.

### Improved
- **[Stochastic Computing](excavations/stochastic-computing.md) Simulator Expansion**: Upgraded `reconstructions/stochastic-computing/stochastic_sim.py` with multi-input stochastic artificial neuron and 1-D moving-average smoothing filter workloads. Added a quantitative accuracy-vs-energy proxy (active CMOS logic gate transitions) trade-off evaluation comparing stochastic multipliers with standard 8-bit binary multipliers.
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
Now that the major physical and systems lineages are fully covered, mapped, and scored, the highest-value remaining gaps for the next iteration of the Digital Archaeology initiative include:
1. **Formal Verification of Soft-Cores**: Extending our synthesizable SystemVerilog verification suite with formal mathematical induction and model checking proofs (e.g., using SymbiYosys) to rigorously guarantee security boundaries on our capability and bounds checker RTL.
2. **Autonomous Multi-Agent Sandbox Demos**: Constructing a complete, runnable agent federation demo in the playground where multiple simulated LLM agents cooperate via union-mounted Plan 9 9P private directory channels, protected by inline hardware capability registers.
3. **External Contributor Onboarding Guide**: Structuring a modular, step-by-step contribution guideline and templated automated test harness to streamline onboarding for academic and industry research experts looking to contribute custom simulators.
4. **Lightweight Predictive Hypothesis Engine**: Designing a Python-based forecasting tool that maps historically sidelined architectural failures to emerging post-CMOS physics, predicting which forgotten abstractions will gain the highest-value revival potential within the next 10 years.

---

## [Unreleased] - August 2026

### Added
- **Superconducting & Cryogenic Pulse Simulator**: Developed a zero-dependency, picosecond-accurate simulator under `reconstructions/cryogenic-superconducting/sfq_sim.py` modeling stateful Rapid Single Flux Quantum (RSFQ) logic (including D-Flip-Flop and AND cells), timing jitter, setup violations, and thermal noise. Features a detailed thermodynamic energy model comparing standard RSFQ bias resistors to ERSFQ zero-static loops and high-temperature superconductors, including cryocooler Carnot cooling penalties. Fully unit tested in `test_sfq_sim.py`.
- **State of Revival Architectural Synthesis**: Authored `synthesis/state-of-revival.md` evaluating the six computer architecture lineages under modern physical, security, and AI constraints, proposing three concrete, runnable sandbox experiments.
- **Pedagogical Superconducting Lab**: Integrated **Lab Module 8** to `reconstructions/LAB_MANUAL.md` covering RSFQ timing budgets, setup margins, and cryogenic refrigeration coefficient of performance calculations, complete with an executable model solution.
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
- **Deepened Superconducting & Cryogenic Excavation**: Heavily expanded `excavations/superconducting-cryogenic.md` to include comprehensive historical context (latching vs non-latching logic), detailed ASCII diagrams of Josephson junction mechanics and D-Flip-Flop loops, primary-source citations, and clean separation between verified historical facts and forward-looking system projections.
- **Relational Density, Indexes, & Navigation**:
  - Integrated "Superconducting & Cryogenic" as the 6th scored lineage inside `modern-relevance/revival-readiness.md` and registered its corresponding physical/thermodynamic lineage under `COMPARATIVE_INDEX.md`.
  - Rebuilt the complete `modern-relevance/knowledge_graph.json` using updated parser definitions for the new simulator and synthesis essay.
  - Redesigned `README.md`, `modern-relevance/using-this-repo.md`, `patterns/constraint-migration.md`, and `modern-relevance/ai.md` with deep links and entry points referencing superconducting / cryogenic coprocessors.
  - Added navigation references to `mkdocs.yml` for the new `state-of-revival.md` essay.
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
  - `excavations/transputers.md`: Fully documented INMOS T414 (15 MIPS), T800 (FPU-on-die, 1.5-micron, 250k transistors), and T9000 milestones. Highlighted the microcoded low/high priority hardware multitasking scheduler, internal/external zero-copy channel rendezvous mechanisms, and the elegant [occam](excavations/occam.md) compiler CSP-to-silicon co-design. Mapped concepts to Go channels, Erlang actors, and modern Networks-on-Chip (NoC).
- **Relational Density & Bidirectional Linking**: Strengthened link intersections from excavations to spatial computing, AI, and FPGA relevance files (`synthesis/return-of-spatial-computing.md`, `patterns/constraint-migration.md`, `modern-relevance/ai.md`, `modern-relevance/fpga.md`, and `synthesis/capability-based-security.md`).
- **Knowledge Graph Synchronization**: Regrouped headings to ensure regular expression compliance, enabling full dynamic extraction of modern relevance paragraphs in `modern-relevance/knowledge_graph.json` without blanking out nodes.
