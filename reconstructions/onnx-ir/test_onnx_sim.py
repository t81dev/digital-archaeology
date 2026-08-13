import importlib.util
import os
import sys
import pytest

# Dynamic load
current_dir = os.path.dirname(os.path.abspath(__file__))
onnx_sim_path = os.path.join(current_dir, "onnx_sim.py")

spec = importlib.util.spec_from_file_location("onnx_sim", onnx_sim_path)
onnx_sim = importlib.util.module_from_spec(spec)
sys.modules["onnx_sim"] = onnx_sim
spec.loader.exec_module(onnx_sim)

Tensor = onnx_sim.Tensor
NodeProto = onnx_sim.NodeProto
ValueInfoProto = onnx_sim.ValueInfoProto
GraphProto = onnx_sim.GraphProto
ModelProto = onnx_sim.ModelProto
OpsetRegistry = onnx_sim.OpsetRegistry
MockFrameworkModel = onnx_sim.MockFrameworkModel
ExporterCompiler = onnx_sim.ExporterCompiler
GraphOptimizer = onnx_sim.GraphOptimizer
MockTensorRTExecutionProvider = onnx_sim.MockTensorRTExecutionProvider
MockCPUExecutionProvider = onnx_sim.MockCPUExecutionProvider
InferenceSession = onnx_sim.InferenceSession

def test_opset_broadcasting():
    # Test tensor shapes [2, 3] and [3]
    a = Tensor(shape=[2, 3], dtype="float32", data=[1, 2, 3, 4, 5, 6])
    b = Tensor(shape=[3], dtype="float32", data=[10, 20, 30])

    # Opset 6 should fail without attributes
    with pytest.raises(ValueError, match="broadcast attribute is disabled"):
        OpsetRegistry.execute_node("Add", [a, b], {}, opset_version=6)

    # Opset 6 should succeed with correct attributes
    res_6 = OpsetRegistry.execute_node("Add", [a, b], {"broadcast": 1, "axis": 1}, opset_version=6)
    assert res_6.data == [11, 22, 33, 14, 25, 36]

    # Opset 15 should succeed automatically
    res_15 = OpsetRegistry.execute_node("Add", [a, b], {}, opset_version=15)
    assert res_15.data == [11, 22, 33, 14, 25, 36]

def test_conversion_tax_tracing():
    model = MockFrameworkModel()
    pos_input = Tensor(shape=[1, 2], dtype="float32", data=[2.0, 2.0])

    # Trace with positive input
    traced_model = ExporterCompiler.export_via_tracing(model, pos_input)
    assert len(traced_model.graph.nodes) == 2
    assert traced_model.graph.nodes[0].op_type == "Gemm"
    assert traced_model.graph.nodes[1].op_type == "Relu" # traced active branch

    session = InferenceSession(traced_model, [MockCPUExecutionProvider()])

    # Run with positive input -> matches framework exactly
    out_pos = session.run({"X": pos_input})
    expected_pos = model.forward(pos_input)
    assert out_pos["Y"].data == expected_pos.data

    # Run with negative input -> tracing mismatch (fidelity loss)
    neg_input = Tensor(shape=[1, 2], dtype="float32", data=[-2.0, -2.0])
    out_neg = session.run({"X": neg_input})
    expected_neg = model.forward(neg_input)

    # The traced model has static Relu, which clamps negative outputs to 0.0
    # but the framework-native has dynamic scaling branch resulting in positive values!
    assert out_neg["Y"].data == [0.0, 0.0]
    assert expected_neg.data == [11.25, 17.25] # non-zero expected, proving the mismatch!

def test_conversion_tax_symbolic_unsupported_op():
    # Symbolic compile should raise compilation exception on custom unsupported hardware operations
    unsupported_model = MockFrameworkModel(supports_custom_op=True)

    with pytest.raises(TypeError, match="operator 'HardwareOp' is not registered"):
        ExporterCompiler.export_via_symbolic(unsupported_model)

def test_graph_optimization_constant_folding():
    # Build a graph with folding constant Add nodes
    const_node_1 = NodeProto("Constant", [], ["c1"], {"value": Tensor([1], "float32", [2.0])})
    const_node_2 = NodeProto("Constant", [], ["c2"], {"value": Tensor([1], "float32", [3.0])})
    add_node = NodeProto("Add", ["c1", "c2"], ["folded"])
    dummy_input = ValueInfoProto("dummy", [1], "float32")
    dummy_output = ValueInfoProto("folded", [1], "float32")

    graph = GraphProto(
        name="folding_graph",
        nodes=[const_node_1, const_node_2, add_node],
        inputs=[dummy_input],
        outputs=[dummy_output],
        initializers={}
    )

    # Folding on Opset 15
    folded_graph = GraphOptimizer.constant_folding(graph, opset_version=15)

    # All Constant nodes and the dependent Add node are folded away into initializers!
    assert len(folded_graph.nodes) == 0
    assert "folded" in folded_graph.initializers
    assert folded_graph.initializers["folded"].data == [5.0]

def test_graph_optimization_node_fusion():
    # Build a graph with Gemm -> Relu pattern
    gemm_node = NodeProto("Gemm", ["X", "W", "B"], ["gemm_out"])
    relu_node = NodeProto("Relu", ["gemm_out"], ["Y"])

    graph = GraphProto(
        name="fusion_graph",
        nodes=[gemm_node, relu_node],
        inputs=[ValueInfoProto("X", [1, 2], "float32")],
        outputs=[ValueInfoProto("Y", [1, 2], "float32")],
        initializers={"W": Tensor([2, 2], "float32", [1, 0, 0, 1]), "B": Tensor([2], "float32", [0, 0])}
    )

    fused_graph = GraphOptimizer.node_fusion(graph)
    assert len(fused_graph.nodes) == 1
    assert fused_graph.nodes[0].op_type == "FusedGemmRelu"
    assert fused_graph.nodes[0].inputs == ["X", "W", "B"]
    assert fused_graph.nodes[0].outputs == ["Y"]

def test_inference_session_execution_and_partitioning():
    # Test a combined network of Fused Gemm + Relu and a constant addition
    framework_model = MockFrameworkModel()
    gemm_node = NodeProto("Gemm", ["X", "W", "B"], ["gemm_out"], {"alpha": 1.0, "beta": 1.0})
    relu_node = NodeProto("Relu", ["gemm_out"], ["relu_out"])
    const_node = NodeProto("Constant", [], ["c1"], {"value": Tensor([1], "float32", [10.0])})
    add_node = NodeProto("Add", ["relu_out", "c1"], ["Y"])

    graph = GraphProto(
        name="full_session_graph",
        nodes=[gemm_node, relu_node, const_node, add_node],
        inputs=[ValueInfoProto("X", [-1, 2], "float32")],
        outputs=[ValueInfoProto("Y", [-1, 2], "float32")],
        initializers={"W": framework_model.W, "B": framework_model.B}
    )

    model = ModelProto(graph, opset_version=15)

    # Priority list: MockTensorRTEP executes FusedGemmRelu, MockCPUEP does fallback Constant and Add
    trt_ep = MockTensorRTExecutionProvider()
    cpu_ep = MockCPUExecutionProvider()

    session = InferenceSession(model, [trt_ep, cpu_ep])

    # Check partitioning plan:
    # Constant 'c1' is folded away into initializers during Session init,
    # Gemm + Relu are fused into 'FusedGemmRelu'.
    # This leaves exactly 2 nodes in the active graph:
    # 1. 'relu_out' (FusedGemmRelu) assigned to TensorRTEP
    # 2. 'Y' (Add) assigned to CPU_EP
    assert len(session.execution_plan) == 2

    first_node, assigned_ep = session.execution_plan[0]
    assert first_node.op_type == "FusedGemmRelu"
    assert assigned_ep.name == "TensorRTEP"

    last_node, assigned_ep = session.execution_plan[-1]
    assert last_node.op_type == "Add"
    assert assigned_ep.name == "CPU_EP"

    # Run session
    x_input = Tensor(shape=[1, 2], dtype="float32", data=[1.0, 2.0])
    outputs = session.run({"X": x_input})

    # Expected output math:
    # Gemm out = X * W + B
    #   row 0 col 0 = 1*1 + 2*3 + 0.5 = 7.5
    #   row 0 col 1 = 1*2 + 2*4 + 0.5 = 10.5
    # Relu out = [7.5, 10.5]
    # Add c1 (10.0) = [7.5+10, 10.5+10] = [17.5, 20.5]
    assert outputs["Y"].data == [17.5, 20.5]
