# [Dynamic Token-Matching](../../GLOSSARY.md) Dataflow Engine

> *An executable model of a non-von Neumann dataflow execution processor with dynamic token-tag matching.*

---

## Background

In the traditional **von Neumann architecture**, execution is guided by a **Program Counter (PC)**, which sequentially fetches and executes instructions. This model enforces a strict, serialized ordering of operations, introducing major hardware bottlenecks (the "[von Neumann bottleneck](../../GLOSSARY.md)" and "memory wall") when scaling to massively parallel workloads.

**[Dataflow Computing](../../excavations/dataflow-computing.md)** abandons the Program Counter entirely. Instead of fetching instructions, execution is entirely **data-driven**. An instruction (or "node" in a dataflow graph) is triggered and executed automatically as soon as all its input operands (represented as "tokens") become available.

### Dynamic Tagged-Token Dataflow

Early static dataflow architectures had a limitation: a node could not receive a new token until its previous token was consumed.

The **Tagged-Token Dataflow** model (pioneered by MIT and the University of Manchester) solved this by tagging every data token with a unique context/iteration tag. This allows multiple concurrent activations of the same instruction (e.g., inside loops or recursive function calls) to execute simultaneously and asynchronously on the same hardware.

A node "fires" when two tokens with matching:
1. `node_id` (destination instruction)
2. `tag` (execution context/iteration ID)

arrive at the left and right inputs of the node.

---

## Features of This Simulator

This simulator implements a [dynamic token-matching](../../GLOSSARY.md) execution engine:
1. **Dynamic Token Queue**: Houses active tokens waiting to be processed or matched.
2. **Token Matcher**: A hardware-like memory unit that matches left and right tokens by destination `node_id` and context `tag`.
3. **Instruction Set**: Includes operators:
   - Arithmetic: `ADD`, `SUB`, `MUL`, `DIV`
   - Control: `COND` (conditional routing) and `MERGE` (merging control paths)
   - Constants: `CONST` (injects a constant token when a trigger arrives)
4. **Execution Log & Visual Trace**: Shows step-by-step parallel token matching, firing events, and result routing.
5. **Sample Programs**:
   - **Parallel Quadratic Formula**: Computes `(x^2 + y^2) * (x - y)` in parallel.
   - **Iterative Factorial**: A fully-pipelined dataflow loop demonstrating dynamic tagging for loop iterations.

---

## How to Run

Execute the script from the repository root:

```bash
python3 reconstructions/dataflow-engine/dataflow_sim.py
```

The script runs the sample programs and prints detailed step-by-step asynchronous execution traces.
