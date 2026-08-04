# Modern Reconstructions & Simulators

> *Active software reconstructions and executable models translating historical computing paradigms into modern, runnable environments.*

---

## Overview

Welcome to the **Digital Archaeology Reconstructions & Simulators** directory. While Phase I (Excavations) focused on historical research and Phase II (Synthesis) mapped conceptual connections, **Phase III** moves from theory to execution.

Each subdirectory here contains an interactive, fully-functional simulator or emulator written in Python. These software models are designed to be educational, self-contained, and interactive—allowing you to experiment directly with the core abstractions that defined these historical paradigms.

---

## Table of Reconstructions

### 1. [Balanced Ternary & Mixed-Radix Simulator](mixed-radix-sim/)
* **Focus**: Alternative arithmetic, non-binary logic.
* **Paradigm**: [Balanced Ternary](../excavations/balanced-ternary.md) (Setun-style).
* **What it does**: Implements trit-level balanced ternary logic, multi-trit addition, and multiplication. Demonstrates why signed representation without a sign bit simplifies arithmetic and why ternary has a higher radix economy than binary.
* **Entry point**: `reconstructions/mixed-radix-sim/ternary_sim.py`

### 2. [Dynamic Token-Matching Dataflow Engine](dataflow-engine/)
* **Focus**: Asynchronous spatial execution, non-von Neumann control flow.
* **Paradigm**: [Dataflow Computing](../excavations/dataflow-computing.md) (MIT Tagged-Token style).
* **What it does**: Implements a parallel token-matching execution engine. Nodes fire asynchronously when their inputs (tokens with matching destination and context tags) arrive. Demonstrates out-of-order execution, fine-grained concurrency, and loop pipelining.
* **Entry point**: `reconstructions/dataflow-engine/dataflow_sim.py`

### 3. [Capability-Based Memory Protection Emulator](capability-security/)
* **Focus**: Hardware-enforced object capabilities and micro-segmentation.
* **Paradigm**: [Capability Systems](../excavations/capability-systems.md) (Burroughs, Intel iAPX 432, CHERI-style).
* **What it does**: Simulates a CPU and RAM utilizing "tagged memory." Normal data words are distinguished from unforgeable Capability words. Simulates memory bounds checking, read/write/execute rights enforcement, and secure cross-domain method calls (domain transitions).
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

---

## Running the Simulators

All simulators are written in pure Python 3 without external dependencies, making them fully portable and easy to run in any terminal.

### Quick Start

To run any of the simulators, navigate to the respective directory and execute the Python file:

```bash
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
```

Each simulator includes built-in interactive menus, step-by-step traces, or test programs that print detailed execution paths to the console.

---

## Why Code-Based Archaeology?

Reconstructing these architectures in software provides three crucial insights:

1. **Abstractions vs. Constraints**: By removing the physical manufacturing limits of the 1960s–1980s (e.g., discrete transistors, magnetic core memory, packaging wire limits), we can isolate the core *logical elegance* of the design.
2. **Modern Tooling Integration**: We can explore how easily these historical concepts map to modern high-level languages, compilers, and async execution models.
3. **Execution Clarity**: Step-by-step traces make abstract concepts—such as token-matching in dataflow or domain transitions in capability hardware—immediately tangible.
