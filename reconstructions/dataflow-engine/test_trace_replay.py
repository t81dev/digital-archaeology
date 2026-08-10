import os
import sys
import pytest

# Ensure parents can be loaded
DF_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DF_DIR)

from trace_replay import TraceReplayEngine

def test_trace_replay_simple_math():
    """Verify loading and replaying a simple math trace: (5 * 4) + (2 - 1) = 21."""
    # Define trace operations
    trace = [
        # Node 1: Multiplies 5 * 4, routes to Node 3 (left input)
        {
            "id": 1,
            "op": "MUL",
            "inputs": [5, 4],
            "dests": [(3, "left")]
        },
        # Node 2: Subtracts 2 - 1, routes to Node 3 (right input)
        {
            "id": 2,
            "op": "SUB",
            "inputs": [2, 1],
            "dests": [(3, "right")]
        },
        # Node 3: Adds left and right, routes to Node 4 (output)
        {
            "id": 3,
            "op": "ADD",
            "dests": [(4, "unconditional")]
        },
        # Node 4: Output node
        {
            "id": 4,
            "op": "OUTPUT"
        }
    ]

    replay = TraceReplayEngine(verbose=False)
    replay.load_trace(trace)
    results = replay.run_replay()

    # The final output is 21 at Node 4
    assert 4 in results["outputs"]
    assert results["outputs"][4] == [21]
    assert results["steps"] > 0
    assert results["tokens_matched"] == 3 # 3 binary operations (Node 1, Node 2, Node 3 matched left and right)
