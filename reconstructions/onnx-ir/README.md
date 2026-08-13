# ONNX Core Abstractions Simulator

An executable pedagogical simulator reconstructing the core architectures of **ONNX (Open Neural Network Exchange)**.

This simulator models the intermediate representation structure, versioned operator sets, exporter lowering and tracing boundaries ("conversion tax"), level-1 and level-2 graph optimizations, and multi-backend execution-provider scheduling.

---

## Architectural Features Modeled

### 1. Standard Graph-Based IR (`ModelProto`, `GraphProto`, `NodeProto`, `Tensor`)
A standard representation of a neural network as a platform-neutral Directed Acyclic Graph (DAG) using unified data structures. It decouples weights (initializers) and static schema shapes (`ValueInfoProto`) from runtime execution states.

### 2. Versioned Operator Sets (Opsets)
We model the strict mathematical semantics of operator drift across version boundaries by implementing the `Add` operator's historical transition:
- **Opset 6**: Requires strict and manual `broadcast` and `axis` attributes to align mismatched shapes.
- **Opset 7+**: Automatically implements dynamic Numpy-style broadcasting (attributes are obsolete and ignored).

### 3. Exporter "Conversion Tax" Boundary
Exposes the two primary framework lowering mechanisms and their real-world failures:
- **Tracing**: Runs a dummy tensor and records executed nodes. Demonstrates *fidelity loss* where dynamic conditional branches are completely missed if they are inactive during the tracing run.
- **Symbolic AST Export**: Inspects code structure without execution. Throws compilation exceptions when encountering unsupported custom hardware operations.

### 4. Graph Optimizations
Includes a compiler middle-end that performs transformations on the graph:
- **Level-1 (Constant Folding)**: Pre-populates `Constant` node values into static `initializers`, evaluates dependent static mathematics at initialization, and prunes folded nodes.
- **Level-2 (Node Fusion)**: Rewrites the graph statically, fusing sequential pattern nodes (such as a contiguous `Gemm` + `Relu` chain) into a single optimized `FusedGemmRelu` virtual node.

### 5. Pluggable Execution Providers (EP) & Memory Planner
Models the dynamic graph-partitioning pipeline inside ONNX Runtime:
- Registers multiple providers with differing priorities and capabilities (e.g., `MockTensorRTExecutionProvider` for high-performance fused GPU subgraphs, and `MockCPUExecutionProvider` for host fallbacks).
- Partitions nodes dynamically to the highest-priority provider supporting them (VFS-style delegation).
- Sequentially executes the scheduled plan, utilizing a reference-counting memory planner that immediately deallocates intermediate tensor buffers once their consumer nodes finish executing.

---

## Files

- `onnx_sim.py`: The core simulator engine, including data structures, Opset registry, exporter compiler, graph optimizer, execution providers, and inference session runner. Includes a CLI demonstration output.
- `test_onnx_sim.py`: Comprehensive pytest suite validating broadcasting skew, tracing fidelity loss, symbolic export exceptions, constant folding, and Execution Provider partitioning plans.

---

## Execution

To run the interactive CLI demonstration of the simulator's capabilities:

```bash
python3 reconstructions/onnx-ir/onnx_sim.py
```

To run the automated verification test suite:

```bash
pytest reconstructions/onnx-ir/test_onnx_sim.py
```
