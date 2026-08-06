# Changelog

All notable changes to the Digital Archaeology repository will be documented in this file.

## [Unreleased] - August 2026

### Added
- **Multi-Trit Balanced Ternary Instruction Set ALU**: Implemented `TernaryALU` in `reconstructions/mixed-radix-sim/ternary_sim.py` simulating standard register operations (`LOAD`, `ADD`, `SUB`, `MUL`, `NEG`, `NOT`, `AND`, `OR`, `SHL`, `SHR`) with natural rounded-to-nearest right-shifts. Added extensive verification tests in `test_ternary_sim.py`.
- **Parallel Dataflow Benchmark Suite**: Integrated fully parallel vector dot-product (`run_vector_dot_product`) and 2x2 matrix multiplication (`run_matrix_multiply_2x2`) benchmarks into `reconstructions/dataflow-engine/dataflow_sim.py`, complete with cycle and token-matching performance counters and unit test validation.
- **Advanced Capability Safety Scenarios**: Developed Scenario 4 (Confused Deputy Attack vs. POLA Capability Defense) and Scenario 5 (Fine-grained Privilege Attenuation and Revocation via Gates) inside `reconstructions/capability-security/capability_sim.py`. Added corresponding unit tests in `test_capability_sim.py` covering hardware performance counters and revocation.

### Improved
- **Primary-Source Grounding of Excavations**:
  - `excavations/capability-systems.md`: Emphasized Dennis & Van Horn (1966), Cambridge CAP Computer, CMU Hydra, KeyKOS, EROS, and CHERI architectural metrics, complete with relative links and a visual ASCII capability register representation.
  - `excavations/dataflow-computing.md`: Detailed MIT Tagged-Token dynamic token matching, the Manchester Dataflow Machine pipeline ring, and mapped the historical dataflow lineage to modern spatial AI hardware (Cerebras, SambaNova, Google TPU, Graphcore).
  - `excavations/balanced-ternary.md`: Elaborated on Nikolay Brusentsov's 1958 Setun computer specifications (ferrite core magnetic amplifiers, 18-trit word equivalent to 28.5 binary bits, 100 kHz clock, gate reductions) and current Multiple-Valued Logic nanoscale routing wall mitigation.
- **Knowledge Graph Synchronization**: Regrouped headings to ensure regular expression compliance, enabling full dynamic extraction of modern relevance paragraphs in `modern-relevance/knowledge_graph.json` without blanking out nodes.
