import pytest
from dataflow_sim import (
    DataflowEngine,
    Node,
    Token,
    run_vector_dot_product,
    run_matrix_multiply_2x2,
)

def test_token_creation():
    t = Token(value=42, dest_node=5, port='left', tag=1)
    assert t.value == 42
    assert t.dest_node == 5
    assert t.port == 'left'
    assert t.tag == 1

def test_unary_operations():
    engine = DataflowEngine()
    engine.add_node(Node(node_id=1, op='DUP', destinations=[(2, 'left'), (3, 'right')]))
    engine.add_node(Node(node_id=2, op='OUTPUT'))
    engine.add_node(Node(node_id=3, op='OUTPUT'))

    engine.inject_token(Token(value=10, dest_node=1, tag=0))
    engine.run_until_empty()

    # Verify that the value was duplicated to both outputs
    # We should have a step count > 0 and final output execution log items
    assert engine.step_count > 0
    assert any("FINAL OUTPUT: 10 at Node 2" in log for log in engine.execution_log)
    assert any("FINAL OUTPUT: 10 at Node 3" in log for log in engine.execution_log)

def test_binary_operations():
    engine = DataflowEngine()
    engine.add_node(Node(node_id=1, op='ADD', destinations=[(3, 'unconditional')]))
    engine.add_node(Node(node_id=2, op='MUL', destinations=[(4, 'unconditional')]))
    engine.add_node(Node(node_id=3, op='OUTPUT'))
    engine.add_node(Node(node_id=4, op='OUTPUT'))

    # ADD operation: inject left and right inputs
    engine.inject_token(Token(value=5, dest_node=1, port='left', tag=0))
    engine.inject_token(Token(value=7, dest_node=1, port='right', tag=0))

    # MUL operation: inject left and right inputs
    engine.inject_token(Token(value=3, dest_node=2, port='left', tag=0))
    engine.inject_token(Token(value=4, dest_node=2, port='right', tag=0))

    engine.run_until_empty()

    assert any("FINAL OUTPUT: 12 at Node 3" in log for log in engine.execution_log)
    assert any("FINAL OUTPUT: 12 at Node 4" in log for log in engine.execution_log)

def test_conditional_switching():
    engine = DataflowEngine()
    # COND Node: takes data on left, boolean control on right
    engine.add_node(Node(node_id=1, op='COND', destinations={
        'true': [(2, 'unconditional')],
        'false': [(3, 'unconditional')]
    }))
    engine.add_node(Node(node_id=2, op='OUTPUT'))
    engine.add_node(Node(node_id=3, op='OUTPUT'))

    # Inject data=99, condition=True
    engine.inject_token(Token(value=99, dest_node=1, port='left', tag=0))
    engine.inject_token(Token(value=True, dest_node=1, port='right', tag=0))
    engine.run_until_empty()

    assert any("FINAL OUTPUT: 99 at Node 2" in log for log in engine.execution_log)
    assert not any("FINAL OUTPUT: 99 at Node 3" in log for log in engine.execution_log)

    # Inject data=100, condition=False
    engine.matching_store.clear()
    engine.execution_log.clear()
    engine.step_count = 0

    engine.inject_token(Token(value=100, dest_node=1, port='left', tag=0))
    engine.inject_token(Token(value=False, dest_node=1, port='right', tag=0))
    engine.run_until_empty()

    assert any("FINAL OUTPUT: 100 at Node 3" in log for log in engine.execution_log)
    assert not any("FINAL OUTPUT: 100 at Node 2" in log for log in engine.execution_log)

def test_tag_incrementing():
    engine = DataflowEngine()
    engine.add_node(Node(node_id=1, op='INC_TAG', destinations=[(2, 'unconditional')]))
    engine.add_node(Node(node_id=2, op='OUTPUT'))

    engine.inject_token(Token(value=123, dest_node=1, tag=5))
    engine.run_until_empty()

    assert any("FINAL OUTPUT: 123 at Node 2 (Tag: 6)" in log for log in engine.execution_log)


# ==========================================
# Benchmark tests
# ==========================================

def test_vector_dot_product_benchmark():
    v1 = [1, 2, 3]
    v2 = [4, 5, 6]
    # Expected: 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
    res, stats = run_vector_dot_product(v1, v2)
    assert res == 32
    assert stats["tokens_injected"] == 11 # 6 inputs + 3 (MUL outputs) + 2 (ADD outputs)
    assert stats["tokens_matched"] == 5   # 3 MUL nodes matched, 2 ADD nodes matched


def test_matrix_multiply_2x2_benchmark():
    m1 = [[2, 3], [4, 5]]
    m2 = [[1, 2], [3, 4]]
    # Expected:
    # r00 = 2*1 + 3*3 = 11
    # r01 = 2*2 + 3*4 = 16
    # r10 = 4*1 + 5*3 = 19
    # r11 = 4*2 + 5*4 = 28
    res, stats = run_matrix_multiply_2x2(m1, m2)
    assert res == [[11, 16], [19, 28]]
    assert stats["tokens_matched"] == 12  # 8 multiplications + 4 additions matched
    assert stats["cycles_steps"] > 0
