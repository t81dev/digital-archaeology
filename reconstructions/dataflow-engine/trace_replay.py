#!/usr/bin/env python3
"""
Trace-Driven Replay Engine for the Tagged-Token Dataflow Simulator.
Reads dynamic execution traces (e.g. sequences of arithmetic and routing ops),
compiles them into active dataflow graphs, injects input tokens, and replays
the step-by-step parallel firing and token-matching in real-time.
"""

from dataflow_sim import DataflowEngine, Node, Token

class TraceReplayEngine:
    """
    Translates static/dynamic execution traces into executable dataflow graphs
    and manages step-by-step replay logic to demonstrate functional divergence.
    """
    def __init__(self, verbose=True):
        self.engine = DataflowEngine()
        self.verbose = verbose
        self.trace_log = []

    def log(self, msg: str):
        self.trace_log.append(msg)
        if self.verbose:
            print(f"[TraceReplay] {msg}")

    def load_trace(self, trace_ops: list):
        """
        Loads a list of trace operations.
        Each operation is a dict:
          {
            "id": int,
            "op": str (e.g. ADD, MUL, SUB, CONST, DUP, OUTPUT),
            "inputs": list of values,
            "dests": list of (int_node_id, str_port) tuples or dictionary for COND,
            "constant_val": optional value
          }
        """
        self.log(f"Loading trace containing {len(trace_ops)} execution blocks.")

        # 1. Create and register nodes
        for op in trace_ops:
            node_id = op["id"]
            operation = op["op"]
            dests = op.get("dests", [])
            const_val = op.get("constant_val", None)

            # Map COND destinations if they are a dict
            node = Node(node_id, operation, destinations=dests, constant_val=const_val)
            self.engine.add_node(node)
            self.log(f"  Compiled node {node_id}: {operation} -> destinations {dests}")

        # 2. Inject initial tokens from static inputs
        for op in trace_ops:
            node_id = op["id"]
            inputs = op.get("inputs", [])
            operation = op["op"]

            # If inputs are provided, we map them to the node's ports
            if inputs:
                if len(inputs) == 1:
                    # Unconditional input for 1-input unary node
                    tok = Token(inputs[0], node_id, port='unconditional')
                    self.engine.inject_token(tok)
                    self.log(f"  Injected input token: {tok}")
                elif len(inputs) == 2:
                    # Left and right inputs for binary node
                    tok_left = Token(inputs[0], node_id, port='left')
                    tok_right = Token(inputs[1], node_id, port='right')
                    self.engine.inject_token(tok_left)
                    self.engine.inject_token(tok_right)
                    self.log(f"  Injected binary input tokens: {tok_left} and {tok_right}")

    def replay_step(self) -> bool:
        """Executes a single instruction firing step of the replay."""
        return self.engine.step()

    def run_replay(self, step_limit=100) -> dict:
        """Runs the entire loaded trace to completion or step limit, returning outputs."""
        self.log("Starting step-by-step trace-driven replay execution...")
        steps = 0
        while self.engine.token_queue and steps < step_limit:
            self.replay_step()
            steps += 1

        self.log(f"Replay complete after {self.engine.step_count} engine cycles.")

        # Format output values
        outputs_harvested = {}
        for node_id, val_list in self.engine.outputs.items():
            outputs_harvested[node_id] = [val for val, tag in val_list]

        return {
            "steps": self.engine.step_count,
            "tokens_matched": self.engine.tokens_matched,
            "outputs": outputs_harvested,
            "logs": self.engine.execution_log
        }
