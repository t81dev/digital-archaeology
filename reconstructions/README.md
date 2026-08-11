# Modern Reconstructions & Simulators

> *Active software reconstructions, synthesizable hardware blueprints, and executable models translating historical computing paradigms into modern, runnable environments.*

---

## Overview

Welcome to the **Digital Archaeology Reconstructions & Simulators** directory. While Phase I (Excavations) focused on historical research and Phase II (Synthesis) mapped conceptual connections, **Phase III** moved from theory to execution. Continuing into Phase V, we expanded this footprint to multi-paradigm simulators and compiled them to WebAssembly.

In **Phase VI**, we successfully mapped these software-defined simulators to synthesizable RTL hardware blocks, designed multi-paradigm co-simulation fabrics, and built browser-native interactive playgrounds using WebAssembly/Pyodide, supported by an academic lab manual.

Each subdirectory here contains an interactive, fully-functional simulator, synthesizable hardware module, or orchestrator.

---

## Table of Reconstructions & Hardware Blueprints

### 1. [Balanced Ternary & Mixed-Radix Simulator](mixed-radix-sim/)
* **Focus**: Alternative arithmetic, non-binary logic.
* **Paradigm**: [Balanced Ternary](../excavations/balanced-ternary.md) (Setun-style).
* **What it does**: Implements trit-level [balanced ternary](../excavations/balanced-ternary.md) logic, multi-trit addition, and multiplication. Demonstrates why signed representation without a sign bit simplifies arithmetic and why ternary has a higher [radix economy](../GLOSSARY.md) than binary.
* **Entry point**: `reconstructions/mixed-radix-sim/ternary_sim.py`

### 2. [Dynamic Token-Matching Dataflow Engine](dataflow-engine/)
* **Focus**: Asynchronous spatial execution, non-von Neumann control flow.
* **Paradigm**: [Dataflow Computing](../excavations/dataflow-computing.md) (MIT Tagged-Token style).
* **What it does**: Implements a parallel token-matching execution engine. Nodes fire asynchronously when their inputs (tokens with matching destination and context tags) arrive. Demonstrates out-of-order execution, fine-grained concurrency, and loop pipelining.
* **Entry point**: `reconstructions/dataflow-engine/dataflow_sim.py`

### 3. [Capability-Based Memory Protection Emulator](capability-security/)
* **Focus**: Hardware-enforced object capabilities and micro-segmentation.
* **Paradigm**: [Capability Systems](../excavations/capability-systems.md) (Burroughs, [Intel iAPX 432](../excavations/intel-iapx-432.md), CHERI-style).
* **What it does**: Simulates a CPU and RAM utilizing "[tagged memory](../GLOSSARY.md)." Normal data words are distinguished from unforgeable Capability words. Simulates memory bounds checking, read/write/execute rights enforcement, and secure cross-domain method calls (domain transitions).
* **Entry point**: `reconstructions/capability-security/capability_sim.py`

### 4. [Neuro-Symbolic Logic Inference Solver](neuro-symbolic/)
* **Focus**: Hybrid AI, structured reasoning under uncertainty.
* **Paradigm**: [Symbolic AI](../excavations/symbolic-ai.md) & [Symbolic Computing](../modern-relevance/symbolic-computing.md) paired with Neural Perception.
* **What it does**: Connects a statistical classifier (mocked with confidence scores) with a formal forward-chaining symbolic engine. Demonstrates how to compile probabilistic inputs into logical propositions, execute deterministic rules, and produce explainable, guardrailed decisions.
* **Entry point**: `reconstructions/neuro-symbolic/neuro_symbolic_sim.py`

### 5. [CSP Synchronous Messaging Simulator](csp-messaging/)
* **Focus**: Rendezvous communication, ALT-based multiplexing, deadlock detection.
* **Paradigm**: [Occam](../excavations/occam.md) & [Transputers](../excavations/transputers.md).
* **What it does**: Implements a cooperative scheduler running parallel processes communicating over synchronous unbuffered channels. Demonstrates rendezvous-based concurrency, alternative channel selection (ALT), and real-time structural deadlock analysis.
* **Entry point**: `reconstructions/csp-messaging/csp_sim.py`

### 6. [Continuous Analog & Optical Wave Accelerator Simulator](analog-optical/)
* **Focus**: Continuous-physical computation, matrix-vector multiplication via wave interference, op-amp differential solver.
* **Paradigm**: [Analog Computing](../excavations/analog-computing.md) & [Optical Computing](../excavations/optical-computing.md).
* **What it does**: Models a continuous physical electronic op-amp computer (solving mass-spring-damper dynamics with noise, drift, and saturation) alongside a Mach-Zehnder Interferometer (MZI) photonic tensor core performing coherent wave propagation and matrix-vector multiplication.
* **Entry point**: `reconstructions/analog-optical/analog_optical_sim.py`

### 7. [Synthesizable Hardware IP Core Blueprints](synthesizable-hardware/) (New in Phase VI)
* **Focus**: Synthesizable soft-cores and hardware-enforced microarchitectural security.
* **Paradigm**: [Balanced Ternary](../excavations/balanced-ternary.md) and [Capability Systems](../excavations/capability-systems.md).
* **What it does**: Contains synthesizable SystemVerilog models: a 3-trit [Balanced Ternary](../excavations/balanced-ternary.md) ALU (`ternary_alu.sv`) and an inline Tagged RAM Capability Bounds Checker (`capability_bounds_checker.sv`), complete with golden functional tests.
* **Entry point**: `reconstructions/synthesizable-hardware/`

### 8. [Multi-Architecture Co-Simulation & Interoperability Fabric](co-simulation/) (New in Phase VI)
* **Focus**: Cross-paradigm sandbox routing and multi-architecture co-simulation.
* **Paradigm**: Concurrent actor messaging (CSP), Spatial Dataflow, and Hybrid AI.
* **What it does**: Implements a pipeline that routes raw statistical neural inputs to a symbolic logic decision solver, schedules incident alerts over synchronous CSP concurrent processes, and triggers parallel dataflow graphs.
* **Entry point**: `reconstructions/co-simulation/orchestrator.py`

### 9. [Linda Tuple Space Simulator](tuple-space/)
* **Focus**: Coordinate-free parallel coordination, [generative communication](../GLOSSARY.md).
* **Paradigm**: [Linda Tuple Spaces](../excavations/linda-tuple-spaces.md).
* **What it does**: Implements a thread-safe, associative [Tuple Space](../GLOSSARY.md) supporting blocking/non-blocking out, in, rd, and active process evaluation (eval). Demonstrates coordinate-free master-worker task allocation.
* **Entry point**: `reconstructions/tuple-space/tuple_space_sim.py`

### 10. [Constraint Migration Predictive Hypothesis Engine](predictive-hypothesis/)
* **Focus**: [Constraint migration](../patterns/constraint-migration.md) forecasting, custom post-CMOS architectural projection.
* **Paradigm**: [Constraint Migration](../patterns/constraint-migration.md) & [Recurring Ideas](../patterns/recurring-ideas.md).
* **What it does**: Models how shifting physical, technological, and security constraints influence alternative computing lineages, predicting their revival potential and generating targeted research hypotheses.
* **Entry point**: `reconstructions/predictive-hypothesis/predictive_engine.py`

---

## Interactive Playgrounds & Academic Materials

### 🖥️ [Interactive WebAssembly & Pyodide Playground](../playground.html)
A browser-native IDE and terminal console executing all python simulators, allowing you to edit scripts, inject hardware faults, and evaluate security exceptions instantly in your browser.

### 📚 [Academic Lab Manual & Pedagogical Sandboxes](LAB_MANUAL.md)
A curated academic manual hosting four university-level computer systems architecture labs, exercises, and clean-slate design challenges.

---

## Running the Simulators

All simulators are written in pure Python 3 without external dependencies, making them fully portable and easy to run in any terminal.

```bash
# Run the Multi-Architecture Co-Simulation Orchestrator
python3 reconstructions/co-simulation/orchestrator.py

# Run the Balanced Ternary Simulator
python3 reconstructions/mixed-radix-sim/ternary_sim.py

# Run the Dataflow Engine
python3 reconstructions/dataflow-engine/dataflow_sim.py

# Run the Capability Security Emulator
python3 reconstructions/capability-security/capability_sim.py

# Run the Neuro-Symbolic Solver
python3 reconstructions/neuro-symbolic/neuro_symbolic_sim.py

# Run the CSP Synchronous Messaging Simulator
python3 reconstructions/csp-messaging/csp_sim.py

# Run the Continuous Analog & Optical Wave Accelerator Simulator
python3 reconstructions/analog-optical/analog_optical_sim.py

# Run the Linda Tuple Space Simulator
python3 reconstructions/tuple-space/tuple_space_sim.py

# Run the Constraint Migration Predictive Hypothesis Engine
python3 reconstructions/predictive-hypothesis/predictive_engine.py
```
