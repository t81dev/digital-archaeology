# Digital Archaeology: An Open-Source Research Framework and Simulation Suite for Sidelined Computing Paradigms

> **An academic overview and citation reference for researchers, computer architects, and systems historians studying constraint migration, alternative execution models, and physical-security hardware revival.**

---

## 1. Project Definition

**Digital Archaeology** is an open-source research initiative, taxonomical ontology, and executable simulation sandbox dedicated to the rediscovery, microarchitectural modeling, and hardware-reconstruction of historically sidelined computing paradigms. By systematically excavating alternative execution, memory protection, and concurrent coordination models abandoned during the era of rapid planar silicon scaling, the project provides modern computer architects and systems researchers with the conceptual tools and verified, zero-dependency software/hardware codebases necessary to design post-von Neumann domain-specific accelerators, hardware-enforced security processors, and decentralized runtimes.

---

## 2. The Six Architectural Lineages

The framework categorizes non-canonical computing paradigms into six major architectural lineages. Each represents an alternative trajectory of systems development:

```
               DIGITAL ARCHAEOLOGY TAXONOMICAL TAXES

       [Execution & Math]               [Memory & Safety]             [Concurrency & Network]
    ┌──────────┴──────────┐          ┌──────────┴──────────┐          ┌──────────┴──────────┐
    ▼                     ▼          ▼                     ▼          ▼                     ▼
 Spatial &             Neuro-     Capability &          Physical &   Distributed &         Superconducting
Data-Parallel        Stochastic    Descriptor           Adiabatic     9P Namespace          & Cryogenic
  (Grid)               (SNN)       (CHERI)               (Wave)       (Tuple/9P)            (SFQ Pulse)
```

1. **Spatial & Data-Parallel**: Homogeneous spatial processing grids that bypass global instruction fetch and bus bottlenecks through localized, data-driven cell routing.
   - *Key Excavations*: [Systolic Arrays](../excavations/systolic-arrays.md) • [Dataflow Computing](../excavations/dataflow-computing.md) • [EDGE](../excavations/edge-architecture.md) • [Transputers](../excavations/transputers.md)
   - *Simulators*: [Systolic Array Simulator](../reconstructions/systolic-array/) • [Token-Matching Dataflow Engine](../reconstructions/dataflow-engine/)
2. **Neuromorphic & Stochastic**: Event-driven temporal spike propagation and probabilistic bitstream arithmetic that trade logical precision for ultra-low area, fault tolerance, and synapse-level energy efficiency.
   - *Key Excavations*: [Neuromorphic Hardware](../excavations/neuromorphic-hardware.md) • [Stochastic Computing](../excavations/stochastic-computing.md) • [Associative Processors](../excavations/associative-processors.md)
   - *Simulators*: [Event-driven SNN Simulator](../reconstructions/neuromorphic-spiking/) • [Stochastic Computing Simulator](../reconstructions/stochastic-computing/) • [Stochastic Multiplier SV Core](../reconstructions/synthesizable-hardware/)
3. **Capability & Descriptor**: Fine-grained, hardware-enforced security boundaries that bind pointer authorization and segment access checks directly to CPU registers and unforgeable memory tags.
   - *Key Excavations*: [Capability Systems](../excavations/capability-systems.md) • [Burroughs Large Systems](../excavations/burroughs-large-systems.md) • [Lisp Machines](../excavations/lisp-machines.md)
   - *Simulators*: [Capability Memory Protection Emulator](../reconstructions/capability-security/) • [Capability Bounds Checker SV Core](../reconstructions/synthesizable-hardware/)
4. **Physical, Optical & Reversible**: Exploiting continuous physical phenomena (wave interference, adiabatic charge recovery, and memristive state changes) to compute at sub-nanosecond speeds or below the Landauer thermodynamic limit.
   - *Key Excavations*: [Analog Computing](../excavations/analog-computing.md) • [Optical Computing](../excavations/optical-computing.md) • [Reversible Computing](../excavations/reversible-computing.md)
   - *Simulators*: [Analog & Optical Wave Accelerator](../reconstructions/analog-optical/) • [Reversible Logic Gates Block SV Core](../reconstructions/synthesizable-hardware/)
5. **Distributed Systems & Single-Level-Store OS**: Location-transparent communication and dynamic, process-private file-system namespaces that unify local and network-remote IPC resources under a single protocol.
   - *Key Excavations*: [Plan 9](../excavations/plan-9.md) • [Linda Tuple Spaces](../excavations/linda-tuple-spaces.md) • [Multics](../excavations/multics.md) • [Inferno](../excavations/inferno.md)
   - *Simulators*: [Plan 9 9P Protocol Simulator](../reconstructions/plan9-9p/) • [Linda Tuple Space Simulator](../reconstructions/tuple-space/)
6. **Superconducting & Cryogenic**: Picosecond-wide magnetic flux pulse propagation in niobium Josephson junctions that enables high-frequency, sub-attojoule logic trees operating at 100+ GHz.
   - *Key Excavations*: [Superconducting/Cryogenic](../excavations/superconducting-cryogenic.md)
   - *Simulators*: [Cryogenic SFQ Pulse Simulator](../reconstructions/cryogenic-superconducting/)

---

## 3. Core Methodological Claims

The research methodology of Digital Archaeology rests on two core claims:

### A. Constraint Migration
Computer architectures are selected not by absolute conceptual superiority, but by the physical, economic, and ecosystem constraints of their original era. When physical boundaries migrate—for example, as the end of Dennard scaling freezes single-core frequencies or the "Von Neumann memory wall" makes data transfer $100\times$ more expensive than arithmetic—previously sidelined paradigms undergo a *heterogeneous revival*. Abstractions originally deemed unviable (e.g., spatial dataflow or analog crossbars) emerge as highly efficient domain-specific coprocessors when mapped onto modern sub-5nm silicon or post-CMOS substrates.

### B. Explanatory Density
The utility of a computing history repository is proportional to its relational density rather than its sheer bulk. Computing history is non-linear and cyclical. By constructing a dense, machine-readable multidimensional network (`knowledge_graph.json`) mapping 35 distinct excavations across a unified Abstraction Taxonomy (Execution, Memory, Concurrency), the framework demonstrates that "extinct" paradigms represent recurring architectural options.

---

## 4. Analytical Tools: Readiness Scores and Synthesis

Researchers can leverage two primary analytical assets within this repository:

* **Modern Revival Readiness Scorecard (`modern-relevance/revival-readiness.md`)**: A quantitative, multidimensional framework scoring the six lineages on *Constraint Migration Status (CMS)*, *Silicon Readiness (SR)*, *Software Friction (SF)*, *Energy Advantage (EA)*, and *AI Synergy (AIS)*. This scorecard evaluates which architectures are ready for immediate production-line integration vs. those requiring specialized ASIC fabrication.
* **Architectural Synthesis (`synthesis/state-of-revival.md`)**: A deep evaluation of ready-for-revival abstractions under modern physical limits. It outlines concrete, cross-paradigm experiments—such as a cryogenic systolic matrix-multiplier or 9P-sandboxed LLM agent execution—using the included executable simulators and synthesizable SystemVerilog soft-cores.

---

## 5. License & Research Citation

All materials, simulators, and hardware blueprints in this repository are distributed under the open-source **MIT License**. Researchers utilizing this framework in academic publications are requested to cite this work as follows:

```bibtex
@software{digital_archaeology_2026,
  author       = {{Digital Archaeology Initiative}},
  title        = {Digital Archaeology: An Open-Source Research Framework and Simulation Suite for Sidelined Computing Paradigms},
  month        = aug,
  year         = 2026,
  publisher    = {GitHub},
  version      = {1.1.0},
  url          = {https://github.com/t81dev/digital-archaeology}
}
```
