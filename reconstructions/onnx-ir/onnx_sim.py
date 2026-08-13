#!/usr/bin/env python3
"""
ONNX (Open Neural Network Exchange) Core Abstractions Simulator.
Demonstrates the following key concepts:
1. Portable Graph-based Intermediate Representation (Model/Graph/Node Proto structures).
2. Versioned Operator Sets (Opsets) - specifically modeling the 'Add' broadcasting rules
   transition from Opset 6 (strict axis/broadcast attributes) to Opset 7+ (numpy-style automatic broadcasting).
3. The "Conversion Tax" boundary - illustrating how dynamic Python frameworks suffer
   from tracing fidelity loss (missing branches) or symbolic export exceptions for unsupported operations.
4. Graph Optimizations - implementing Level-1 Constant Folding and Level-2 Operator Fusion
   (fusing Gemm + Add + Relu into a single optimized virtual node).
5. Pluggable Execution Providers (EP) - modeling dynamic runtime partitioning, querying
   capabilities of alternate backends (GPU, CPU Fallback), and topological graph execution with
   reference-counted memory recycling.
"""

from typing import List, Dict, Any, Tuple, Optional
import math

# =====================================================================
# 1. Standard Intermediate Representation (IR) Data Structures
# =====================================================================

class Tensor:
    """Simulates a multi-dimensional tensor with shape, data type, and values."""
    def __init__(self, shape: List[int], dtype: str, data: List[Any]):
        self.shape = shape
        self.dtype = dtype
        self.data = data

    def __repr__(self) -> str:
        return f"Tensor(shape={self.shape}, dtype={self.dtype}, data_len={len(self.data)})"

class NodeProto:
    """Represents a computational node in the dataflow graph."""
    def __init__(self, op_type: str, inputs: List[str], outputs: List[str], attributes: Dict[str, Any] = None):
        self.op_type = op_type
        self.inputs = inputs
        self.outputs = outputs
        self.attributes = attributes or {}

    def __repr__(self) -> str:
        return f"NodeProto(op={self.op_type}, inputs={self.inputs}, outputs={self.outputs}, attrs={list(self.attributes.keys())})"

class ValueInfoProto:
    """Represents metadata for a tensor (input, output, or intermediate state)."""
    def __init__(self, name: str, shape: List[Optional[int]], dtype: str):
        self.name = name
        self.shape = shape  # None in shape indicates dynamic dimension
        self.dtype = dtype

    def __repr__(self) -> str:
        return f"ValueInfoProto(name='{self.name}', shape={self.shape}, dtype='{self.dtype}')"

class GraphProto:
    """Represents the complete computational directed acyclic graph (DAG)."""
    def __init__(self, name: str, nodes: List[NodeProto], inputs: List[ValueInfoProto], outputs: List[ValueInfoProto], initializers: Dict[str, Tensor]):
        self.name = name
        self.nodes = nodes
        self.inputs = inputs
        self.outputs = outputs
        self.initializers = initializers  # Static weights/constants

class ModelProto:
    """The root container for an ONNX model, defining metadata and the graph."""
    def __init__(self, graph: GraphProto, opset_version: int, producer_name: str = "PolyGraph-Compiler"):
        self.graph = graph
        self.opset_version = opset_version
        self.producer_name = producer_name


# =====================================================================
# 2. Versioned Operator Sets (Opsets) Semantic Implementations
# =====================================================================

class OpsetRegistry:
    """
    Simulates the mathematically rigorous execution semantics across different Opset versions.
    We model the historical transition of the 'Add' operator:
      - Opset 6: Required 'broadcast' and 'axis' attributes to align shapes if they differ.
      - Opset 7+: Implements full, dynamic Numpy-style automatic broadcasting.
    """

    @staticmethod
    def broadcast_opset_6(a: Tensor, b: Tensor, attributes: Dict[str, Any]) -> Tensor:
        """
        Broadcasting under Opset 6 rules:
        Requires 'broadcast=1' attribute, and 'axis' to tell where to align.
        If broadcast attribute is missing or 0, shapes must match exactly.
        """
        broadcast = attributes.get("broadcast", 0)
        axis = attributes.get("axis", -1)

        if a.shape == b.shape:
            # Standard element-wise addition
            result_data = [x + y for x, y in zip(a.data, b.data)]
            return Tensor(shape=a.shape, dtype=a.dtype, data=result_data)

        if not broadcast:
            raise ValueError(f"[Opset 6] Shapes {a.shape} and {b.shape} mismatch and broadcast attribute is disabled.")

        # In Opset 6, B shape must be a contiguous subset of A, starting at 'axis'
        # e.g., A = [2, 3], B = [3], axis = 1.
        if axis == -1:
            # Match trailing dimensions if axis not defined
            axis = len(a.shape) - len(b.shape)

        # Validate that B shape matches the subset of A starting at axis
        for i, dim_b in enumerate(b.shape):
            if a.shape[axis + i] != dim_b:
                raise ValueError(f"[Opset 6] Shape alignment failed at axis {axis}. A_dim={a.shape[axis+i]} != B_dim={dim_b}")

        # Compute broadcasted stride and expand B values
        # Simplification: we only model common broadcasting of 2D + 1D (e.g., [M, N] + [N])
        if len(a.shape) == 2 and len(b.shape) == 1 and axis == 1:
            m, n = a.shape
            result_data = []
            for r in range(m):
                for c in range(n):
                    idx_a = r * n + c
                    idx_b = c
                    result_data.append(a.data[idx_a] + b.data[idx_b])
            return Tensor(shape=a.shape, dtype=a.dtype, data=result_data)
        else:
            raise NotImplementedError("[Opset 6 Simulator] Unsupported complex multidimensional broadcast configuration.")

    @staticmethod
    def broadcast_opset_7(a: Tensor, b: Tensor) -> Tensor:
        """
        Broadcasting under Opset 7+ rules:
        Implements automatic, dynamic multidimensional broadcasting.
        No axis or broadcast attributes allowed or parsed.
        """
        # Simplification for demo: Support (2D + 1D), (2D + Scalar), and identical shapes
        if a.shape == b.shape:
            result_data = [x + y for x, y in zip(a.data, b.data)]
            return Tensor(shape=a.shape, dtype=a.dtype, data=result_data)

        # Scalar broadcasting: shape = [] or [1]
        if len(b.data) == 1:
            val = b.data[0]
            result_data = [x + val for x in a.data]
            return Tensor(shape=a.shape, dtype=a.dtype, data=result_data)

        # A=[M, N], B=[N] automatic broadcasting (aligning from trailing dims)
        if len(a.shape) == 2 and len(b.shape) == 1:
            m, n = a.shape
            if b.shape[0] == n:
                result_data = []
                for r in range(m):
                    for c in range(n):
                        result_data.append(a.data[r * n + c] + b.data[c])
                return Tensor(shape=a.shape, dtype=a.dtype, data=result_data)

        raise ValueError(f"[Opset 7+] Dynamic automatic broadcasting failed for shapes {a.shape} and {b.shape}")

    @classmethod
    def execute_node(cls, op_type: str, inputs: List[Tensor], attributes: Dict[str, Any], opset_version: int) -> Tensor:
        """Dynamic dispatch layer resolving operator semantics based on Opset version bounds."""
        if op_type == "Add":
            if len(inputs) != 2:
                raise ValueError("Add operator requires exactly 2 inputs.")
            if opset_version < 7:
                return cls.broadcast_opset_6(inputs[0], inputs[1], attributes)
            else:
                return cls.broadcast_opset_7(inputs[0], inputs[1])

        elif op_type == "Gemm":
            # Gemm formula: alpha * (A x B) + beta * C
            a, b, bias = inputs
            alpha = attributes.get("alpha", 1.0)
            beta = attributes.get("beta", 1.0)
            transA = attributes.get("transA", 0)
            transB = attributes.get("transB", 0)

            # Simple 2D matrix multiplication
            # Shape check
            m_a, k_a = a.shape if not transA else (a.shape[1], a.shape[0])
            k_b, n_b = b.shape if not transB else (b.shape[1], b.shape[0])

            if k_a != k_b:
                raise ValueError(f"Gemm shape mismatch: matrix multiplication of [{m_a}x{k_a}] and [{k_b}x{n_b}] is invalid.")

            # Helper functions for transpose indexing
            def get_a(r, c):
                return a.data[c * m_a + r] if transA else a.data[r * k_a + c]

            def get_b(r, c):
                return b.data[c * k_b + r] if transB else b.data[r * n_b + c]

            res_data = []
            for r in range(m_a):
                for col in range(n_b):
                    dot_product = sum(get_a(r, i) * get_b(i, col) for i in range(k_a))
                    # Add bias
                    # Bias can be broadcasted
                    bias_idx = col if len(bias.data) == n_b else 0
                    bias_val = bias.data[bias_idx]

                    val = alpha * dot_product + beta * bias_val
                    res_data.append(val)

            return Tensor(shape=[m_a, n_b], dtype=a.dtype, data=res_data)

        elif op_type == "Relu":
            x = inputs[0]
            result_data = [max(0.0, val) for val in x.data]
            return Tensor(shape=x.shape, dtype=x.dtype, data=result_data)

        elif op_type == "Constant":
            # Constant op generates an output tensor defined inside attributes
            tensor_val = attributes.get("value")
            if not tensor_val:
                raise ValueError("Constant node requires a 'value' attribute.")
            return tensor_val

        else:
            raise NotImplementedError(f"Operator '{op_type}' is not registered under standard Opset {opset_version}.")


# =====================================================================
# 3. Exporter, Tracing, and the "Conversion Tax" Boundary
# =====================================================================

class MockFrameworkModel:
    """
    Implements a simple PyTorch-like dynamic Python framework model.
    Contains:
      - Static weights (W, B)
      - A dynamic condition (if inputs sum > 0 execute branch A, else branch B).
      - An unsupported custom C++ operation (e.g., dynamic hardware call).
    """
    def __init__(self, supports_custom_op: bool = False):
        self.W = Tensor(shape=[2, 2], dtype="float32", data=[1.0, 2.0, 3.0, 4.0])
        self.B = Tensor(shape=[2], dtype="float32", data=[0.5, 0.5])
        self.supports_custom_op = supports_custom_op

    def forward(self, x: Tensor) -> Tensor:
        """Dynamic runtime forward pass."""
        # Simple Gemm: x * W + B
        m, k = x.shape
        out_data = []
        for r in range(m):
            for c in range(2):
                dot = x.data[r*k + 0] * self.W.data[0*2 + c] + x.data[r*k + 1] * self.W.data[1*2 + c]
                out_data.append(dot + self.B.data[c])
        out = Tensor(shape=[m, 2], dtype="float32", data=out_data)

        # Dynamic branching:
        if sum(x.data) > 0:
            # Branch A: Relu
            res = Tensor(shape=out.shape, dtype=out.dtype, data=[max(0.0, v) for v in out.data])
        else:
            # Branch B: Linear scaling (multiply by -1.5)
            res = Tensor(shape=out.shape, dtype=out.dtype, data=[v * -1.5 for v in out.data])

        # Unsupported Custom Hardware Op
        if self.supports_custom_op:
            res = Tensor(shape=res.shape, dtype=res.dtype, data=[v + 9.9 for v in res.data])

        return res


class ExporterCompiler:
    """
    Simulates standard framework exporter compilers (like PyTorch export).
    Exposes the two primary export paradigms and their limitations.
    """

    @staticmethod
    def export_via_tracing(model: MockFrameworkModel, mock_input: Tensor) -> ModelProto:
        """
        Tracing Exporter: Runs a dummy input, intercepts standard operations,
        and serializes them.
        CRITICAL FAILURE: Misses inactive conditional branches completely.
        """
        x_sum = sum(mock_input.data)

        # We trace which operations were touched:
        # Step 1: Gemm always happens
        node_1 = NodeProto(op_type="Gemm", inputs=["X", "W", "B"], outputs=["gemm_out"], attributes={"alpha": 1.0, "beta": 1.0})

        # Step 2: Conditional Trace
        if x_sum > 0:
            # Tracer only registers the execution of branch A (Relu)
            node_2 = NodeProto(op_type="Relu", inputs=["gemm_out"], outputs=["Y"])
        else:
            # Tracer registers multiplication by constant -1.5 (modeled as scale Add)
            node_2 = NodeProto(op_type="Add", inputs=["gemm_out", "Scale_Const"], outputs=["Y"])

        initializers = {
            "W": model.W,
            "B": model.B
        }
        if x_sum <= 0:
            initializers["Scale_Const"] = Tensor(shape=[1], dtype="float32", data=[-1.5])

        inputs = [ValueInfoProto("X", shape=[-1, 2], dtype="float32")]
        outputs = [ValueInfoProto("Y", shape=[-1, 2], dtype="float32")]

        graph = GraphProto(
            name="traced_graph",
            nodes=[node_1, node_2],
            inputs=inputs,
            outputs=outputs,
            initializers=initializers
        )
        return ModelProto(graph, opset_version=15)

    @staticmethod
    def export_via_symbolic(model: MockFrameworkModel) -> ModelProto:
        """
        Symbolic AST parser: Reads model structure without executing a mock input.
        CRITICAL FAILURE: Fails with compile exception if model contains unsupported custom ops
        """
        if model.supports_custom_op:
            raise TypeError("[Symbolic Compiler] Export failed: Custom dynamic C++ operator 'HardwareOp' is not registered in the targeted ONNX schema.")

        # Properly translates conditional structures into an ONNX 'If' node containing subgraphs
        node_1 = NodeProto(op_type="Gemm", inputs=["X", "W", "B"], outputs=["gemm_out"])
        node_cond_check = NodeProto(op_type="Add", inputs=["X", "Zero_Const"], outputs=["cond_out"])
        node_if = NodeProto(
            op_type="If",
            inputs=["cond_out"],
            outputs=["Y"],
            attributes={
                "then_branch": "SubGraph_A_Relu",
                "else_branch": "SubGraph_B_Scale"
            }
        )

        graph = GraphProto(
            name="symbolic_graph",
            nodes=[node_1, node_cond_check, node_if],
            inputs=[ValueInfoProto("X", shape=[-1, 2], dtype="float32")],
            outputs=[ValueInfoProto("Y", shape=[-1, 2], dtype="float32")],
            initializers={"W": model.W, "B": model.B, "Zero_Const": Tensor(shape=[1], dtype="float32", data=[0.0])}
        )
        return ModelProto(graph, opset_version=15)


# =====================================================================
# 4. Optimization Engine (Level-1 & Level-2 Graph Rewriting)
# =====================================================================

class GraphOptimizer:
    """
    Performs compiler rewriting on the intermediate representation.
    """

    @staticmethod
    def constant_folding(graph: GraphProto, opset_version: int) -> GraphProto:
        """
        Level-1 Optimization: Constant Folding.
        First registers all 'Constant' nodes into 'initializers' dictionary,
        and then evaluates mathematical operations where all inputs are initializers.
        These folded nodes are discarded, and replaced with static initializers.
        """
        optimized_nodes = []
        initializers = dict(graph.initializers)

        # Step 1: Pre-populate initializers with Constant node values
        for node in graph.nodes:
            if node.op_type == "Constant":
                initializers[node.outputs[0]] = node.attributes["value"]

        # Step 2: Traverse and fold dependent nodes
        for node in graph.nodes:
            if node.op_type == "Constant":
                # Constant node is fully represented in initializers now, discard
                continue
            elif node.op_type in ["Add", "Gemm"] and all(inp in initializers for inp in node.inputs):
                inputs_data = [initializers[inp] for inp in node.inputs]
                folded_tensor = OpsetRegistry.execute_node(node.op_type, inputs_data, node.attributes, opset_version)

                # Register output as a new folded initializer
                out_name = node.outputs[0]
                initializers[out_name] = folded_tensor
                print(f"[Optimizer] Constant folded node: '{node.op_type}' producing '{out_name}'.")
            else:
                optimized_nodes.append(node)

        return GraphProto(graph.name, optimized_nodes, graph.inputs, graph.outputs, initializers)

    @staticmethod
    def node_fusion(graph: GraphProto) -> GraphProto:
        """
        Level-2 Optimization: Operator Fusion.
        Fuses a Gemm node followed directly by a Relu node into a single virtual 'FusedGemmRelu' node.
        This optimizes hardware cache boundaries and prevents temporary CPU/GPU memory writes.
        """
        fused_nodes = []
        i = 0
        while i < len(graph.nodes):
            if i < len(graph.nodes) - 1:
                curr_node = graph.nodes[i]
                next_node = graph.nodes[i+1]

                # Check for Gemm -> Relu pattern
                if curr_node.op_type == "Gemm" and next_node.op_type == "Relu":
                    # Output of Gemm must match Input of Relu, and not be consumed elsewhere
                    if curr_node.outputs[0] == next_node.inputs[0]:
                        fused_node = NodeProto(
                            op_type="FusedGemmRelu",
                            inputs=curr_node.inputs,
                            outputs=next_node.outputs,
                            attributes=curr_node.attributes
                        )
                        fused_nodes.append(fused_node)
                        print(f"[Optimizer] Fused Gemm + Relu into unified kernel '{fused_node.outputs[0]}'.")
                        i += 2
                        continue

            fused_nodes.append(graph.nodes[i])
            i += 1

        return GraphProto(graph.name, fused_nodes, graph.inputs, graph.outputs, graph.initializers)


# =====================================================================
# 5. Pluggable Execution Providers & Runtime Engine
# =====================================================================

class ExecutionProvider:
    """Base interface for hardware execution backends."""
    def __init__(self, name: str):
        self.name = name

    def is_supported(self, op_type: str) -> bool:
        raise NotImplementedError()

    def execute(self, op_type: str, inputs: List[Tensor], attributes: Dict[str, Any], opset: int) -> Tensor:
        raise NotImplementedError()


class MockTensorRTExecutionProvider(ExecutionProvider):
    """A mock high-performance NVIDIA GPU compiler engine."""
    def __init__(self):
        super().__init__("TensorRTEP")
        self.supported_ops = {"Gemm", "FusedGemmRelu"}

    def is_supported(self, op_type: str) -> bool:
        return op_type in self.supported_ops

    def execute(self, op_type: str, inputs: List[Tensor], attributes: Dict[str, Any], opset: int) -> Tensor:
        if op_type == "Gemm":
            print("[TensorRT GPU] Launching parallel GEMM CUDA kernel.")
            return OpsetRegistry.execute_node(op_type, inputs, attributes, opset)
        elif op_type == "FusedGemmRelu":
            print("[TensorRT GPU] Launching ultra-high-throughput Fused Gemm + Relu Tensor Core CUDA kernel.")
            gemm_res = OpsetRegistry.execute_node("Gemm", inputs, attributes, opset)
            return OpsetRegistry.execute_node("Relu", [gemm_res], {}, opset)
        else:
            raise ValueError(f"TensorRT EP cannot execute operator '{op_type}'.")


class MockCPUExecutionProvider(ExecutionProvider):
    """A standard CPU fallback runner implementing all base operators."""
    def __init__(self):
        super().__init__("CPU_EP")

    def is_supported(self, op_type: str) -> bool:
        return True

    def execute(self, op_type: str, inputs: List[Tensor], attributes: Dict[str, Any], opset: int) -> Tensor:
        if op_type == "FusedGemmRelu":
            print("[CPU Fallback] Executing fused Gemm+Relu kernel sequentially.")
            gemm_res = OpsetRegistry.execute_node("Gemm", inputs, attributes, opset)
            return OpsetRegistry.execute_node("Relu", [gemm_res], {}, opset)
        print(f"[CPU Fallback] Executing general operator '{op_type}' on host threads.")
        return OpsetRegistry.execute_node(op_type, inputs, attributes, opset)


class InferenceSession:
    """
    The core virtual machine state engine managing model orchestration,
    dynamic graph partitioning across active providers, and execution loops.
    """
    def __init__(self, model: ModelProto, execution_providers: List[ExecutionProvider]):
        self.model = model
        self.opset_version = model.opset_version
        self.providers = execution_providers
        self.graph = model.graph

        # Step 1: Execute graph optimizations
        self._optimize_graph()

        # Step 2: Compile execution plan & partition graph
        self.execution_plan: List[Tuple[NodeProto, ExecutionProvider]] = []
        self._partition_graph()

    def _optimize_graph(self):
        """Compulsory level-1 and level-2 optimizations."""
        print(f"\n--- Initializing Inference Session optimizations (Opset {self.opset_version}) ---")
        self.graph = GraphOptimizer.constant_folding(self.graph, self.opset_version)
        self.graph = GraphOptimizer.node_fusion(self.graph)

    def _partition_graph(self):
        """
        VFS-style Partitioning:
        Query registered execution providers sequentially. Assign nodes to the highest
        priority provider that supports them. Fallback to CPU_EP.
        """
        print("\n--- Compiling Execution Partition Plan ---")
        for node in self.graph.nodes:
            assigned_ep = None
            # Scan EPs in order of priority (first in list has highest priority)
            for ep in self.providers:
                if ep.is_supported(node.op_type):
                    assigned_ep = ep
                    break

            if not assigned_ep:
                raise RuntimeError(f"Fatal execution plan compilation: No registered execution provider supports '{node.op_type}'.")

            self.execution_plan.append((node, assigned_ep))
            print(f"Node '{node.outputs[0]}' ({node.op_type}) delegated to -> {assigned_ep.name}")

    def run(self, inputs: Dict[str, Tensor]) -> Dict[str, Tensor]:
        """
        Topologically schedules and executes nodes.
        Implements dynamic reference-count memory tracking and buffer recycling.
        """
        print("\n--- Executing Inference Run ---")
        # Initialize memory registers with inputs and static weights (initializers)
        memory_pool: Dict[str, Tensor] = {**inputs, **self.graph.initializers}

        # Reference tracking to simulate memory planning
        ref_counts = self._calculate_reference_counts()
        peak_allocated_tensors = 0

        for node, ep in self.execution_plan:
            # Gather inputs from memory registers
            node_inputs = []
            for inp_name in node.inputs:
                if inp_name not in memory_pool:
                    raise KeyError(f"Runtime execution error: Expected input buffer '{inp_name}' for node outputting '{node.outputs[0]}' is missing.")
                node_inputs.append(memory_pool[inp_name])

            # Delegate to specialized Execution Provider
            out_tensor = ep.execute(node.op_type, node_inputs, node.attributes, self.opset_version)

            # Save outputs to memory registers
            out_name = node.outputs[0]
            memory_pool[out_name] = out_tensor

            # Dynamic Reference Decrement and Buffer Recycling simulation
            for inp_name in node.inputs:
                # Do not delete input models or static weights
                if inp_name in inputs or inp_name in self.graph.initializers:
                    continue
                if inp_name not in ref_counts:
                    continue
                ref_counts[inp_name] -= 1
                if ref_counts[inp_name] == 0:
                    del memory_pool[inp_name]
                    print(f"[Memory Planner] Deallocated intermediate buffer '{inp_name}' to recycle memory.")

            peak_allocated_tensors = max(peak_allocated_tensors, len(memory_pool))

        print(f"[Memory Planner] Execution completed. Peak in-flight buffers: {peak_allocated_tensors}")

        # Retrieve final output tensors
        final_outputs = {}
        for out_info in self.graph.outputs:
            final_outputs[out_info.name] = memory_pool[out_info.name]

        return final_outputs

    def _calculate_reference_counts(self) -> Dict[str, int]:
        """Calculates how many times each intermediate output is read across the graph."""
        counts = {}
        for node in self.graph.nodes:
            for inp_name in node.inputs:
                if inp_name not in counts:
                    counts[inp_name] = 0
                counts[inp_name] += 1
        return counts


# =====================================================================
# 6. Demonstration Entry Point
# =====================================================================

def run_onnx_paradigms_demo():
    print("=================================================================")
    print("   ONNX COMPLETED ARCHAEOLOGICAL RECONSTRUCTION SIMULATOR        ")
    print("=================================================================\n")

    # Paradigm A: Opset Versioning Skew
    print("--- 1. Testing Opset Versioning Broadcast Rules ---")
    a = Tensor(shape=[2, 3], dtype="float32", data=[1, 2, 3, 4, 5, 6])
    b = Tensor(shape=[3], dtype="float32", data=[10, 20, 30])

    # Under Opset 6: Required strict axis/broadcast attributes
    try:
        print("Executing Opset 6 Add (no attributes):")
        OpsetRegistry.execute_node("Add", [a, b], {}, opset_version=6)
    except ValueError as e:
        print(f"Expected Opset 6 Failure: {e}")

    print("\nExecuting Opset 6 Add (correct broadcast attributes):")
    res_6 = OpsetRegistry.execute_node("Add", [a, b], {"broadcast": 1, "axis": 1}, opset_version=6)
    print(f"Opset 6 output: {res_6.data}")

    # Under Opset 7+: Automatic Numpy-style broadcasting (attributes ignored/unnecessary)
    print("\nExecuting Opset 15 Add (no broadcast attributes, automatic alignment):")
    res_15 = OpsetRegistry.execute_node("Add", [a, b], {}, opset_version=15)
    print(f"Opset 15 output: {res_15.data}")

    # Paradigm B: Exporter Conversion Tax & Tracing Fidelity Loss
    print("\n--- 2. Testing Exporter Conversion Tax ---")
    framework_model = MockFrameworkModel()

    # Test Tracer with mock input that triggers branch A (sum > 0)
    pos_input = Tensor(shape=[1, 2], dtype="float32", data=[1.0, 1.0])
    traced_model_pos = ExporterCompiler.export_via_tracing(framework_model, pos_input)
    print(f"Traced Model with positive input contains nodes: {[n.op_type for n in traced_model_pos.graph.nodes]}")

    # Run tracing-derived session over positive and NEGATIVE inputs
    session_pos = InferenceSession(traced_model_pos, [MockCPUExecutionProvider()])

    out_pos = session_pos.run({"X": pos_input})
    print(f"Expected positive forward: {framework_model.forward(pos_input).data}")
    print(f"Session execution output:  {out_pos['Y'].data}")

    # Run the positive-traced model on negative input
    neg_input = Tensor(shape=[1, 2], dtype="float32", data=[-2.0, -2.0])
    try:
        # CRITICAL FIDELITY LOSS: Traced model has Relu statically hardcoded,
        # missing the native dynamic scale branch!
        out_neg_traced = session_pos.run({"X": neg_input})
        print(f"\nExpected native dynamic negative forward: {framework_model.forward(neg_input).data}")
        print(f"Session with positive-traced model on negative input: {out_neg_traced['Y'].data}")
        print("WARNING: Output mismatch! The traced model failed to adapt to dynamic conditional branch.")
    except Exception as e:
        print(f"Exception during run: {e}")

    # Paradigm C: Graph Optimization and pluggable EP Execution Routing
    print("\n--- 3. Testing Optimization & EP Scheduling ---")
    # Build a standard static Model graph: Gemm -> Relu -> Add (scale constant)
    gemm_node = NodeProto("Gemm", ["X", "W", "B"], ["gemm_out"], {"alpha": 1.0, "beta": 1.0})
    relu_node = NodeProto("Relu", ["gemm_out"], ["relu_out"])

    # Add a node that will fold (Add of constants)
    const_node_1 = NodeProto("Constant", [], ["const_1"], {"value": Tensor([1], "float32", [5.0])})
    const_node_2 = NodeProto("Constant", [], ["const_2"], {"value": Tensor([1], "float32", [10.0])})
    add_const_node = NodeProto("Add", ["const_1", "const_2"], ["folded_bias"])

    final_add = NodeProto("Add", ["relu_out", "folded_bias"], ["Y"])

    inputs = [ValueInfoProto("X", [-1, 2], "float32")]
    outputs = [ValueInfoProto("Y", [-1, 2], "float32")]

    graph = GraphProto(
        name="complex_optimization_graph",
        nodes=[gemm_node, relu_node, const_node_1, const_node_2, add_const_node, final_add],
        inputs=inputs,
        outputs=outputs,
        initializers={"W": framework_model.W, "B": framework_model.B}
    )

    model_proto = ModelProto(graph, opset_version=15)

    # Load session with specialized TensorRT EP + Fallback CPU EP
    session = InferenceSession(
        model_proto,
        [MockTensorRTExecutionProvider(), MockCPUExecutionProvider()]
    )

    # Run the session
    run_input = Tensor(shape=[1, 2], dtype="float32", data=[1.0, 2.0])
    session_out = session.run({"X": run_input})
    print(f"Inference Session final Y output values: {session_out['Y'].data}")


if __name__ == "__main__":
    run_onnx_paradigms_demo()
