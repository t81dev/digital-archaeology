#!/usr/bin/env python3
"""
Dynamic Token-Matching Dataflow Engine
A simulator demonstrating a non-von Neumann data-driven parallel execution model.
"""

import collections

class Token:
    """
    A data token carrying a value through the dataflow graph.
    """
    def __init__(self, value, dest_node, port='left', tag=0):
        self.value = value
        self.dest_node = dest_node
        self.port = port  # 'left', 'right', or 'unconditional'
        self.tag = tag    # context/iteration tag for dynamic dataflow

    def __repr__(self):
        return f"Token(val={self.value}, dest={self.dest_node}, port={self.port}, tag={self.tag})"


class Node:
    """
    An execution node (instruction) in the dataflow graph.
    """
    def __init__(self, node_id, op, destinations=None, constant_val=None):
        self.node_id = node_id
        self.op = op  # ADD, SUB, MUL, DIV, CMP_LE, COND, MERGE, DUP, CONST, INC_TAG, OUTPUT
        # destinations is a list of (dest_node_id, port) or dict for COND
        self.destinations = destinations or []
        self.constant_val = constant_val

    def __repr__(self):
        return f"Node(id={self.node_id}, op={self.op})"


class DataflowEngine:
    """
    The main execution engine that houses nodes, matches tokens, and executes instructions.
    """
    def __init__(self):
        self.nodes = {}
        self.token_queue = collections.deque()
        # Key: (node_id, tag, port) for 2-input matching, or (node_id, tag) if matching any port
        # In tagged-token dataflow, left and right inputs for the same (node, tag) must match.
        self.matching_store = {}
        self.execution_log = []
        self.step_count = 0

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def inject_token(self, token):
        self.token_queue.append(token)

    def step(self) -> bool:
        """
        Processes a single token from the queue.
        Returns True if a token was processed, False if queue is empty.
        """
        if not self.token_queue:
            return False

        self.step_count += 1
        token = self.token_queue.popleft()
        node_id = token.dest_node
        tag = token.tag

        if node_id not in self.nodes:
            # Reached a external/output sink or undefined node
            self.execution_log.append(f"[Step {self.step_count}] Token {token} arrived at Sink.")
            return True

        node = self.nodes[node_id]

        # Unary operations fire immediately
        unary_ops = {'DUP', 'CONST', 'INC_TAG', 'OUTPUT'}

        if node.op in unary_ops:
            self.execution_log.append(f"[Step {self.step_count}] Unary Node {node_id} ({node.op}) fired with {token}")
            self.fire_unary(node, token)
        elif node.op == 'MERGE':
            # MERGE propagates whichever input arrives
            self.execution_log.append(f"[Step {self.step_count}] MERGE Node {node_id} fired with {token}")
            self.route_output(node, token.value, token.tag)
        else:
            # 2-input operations require matching left and right tokens
            match_key = (node_id, tag)
            if match_key in self.matching_store:
                # Found a partner!
                partner = self.matching_store.pop(match_key)

                # Determine which is left and which is right
                if token.port == 'left' and partner.port == 'right':
                    left, right = token, partner
                elif token.port == 'right' and partner.port == 'left':
                    left, right = partner, token
                else:
                    # Fallback if ports aren't specified cleanly
                    left, right = token, partner

                self.execution_log.append(f"[Step {self.step_count}] Binary Node {node_id} ({node.op}) matched and fired: Left={left.value}, Right={right.value} (Tag={tag})")
                self.fire_binary(node, left, right)
            else:
                # No partner yet, store it
                self.matching_store[match_key] = token
                self.execution_log.append(f"[Step {self.step_count}] Token {token} stored in Matching Store. Waiting for partner.")

        return True

    def fire_unary(self, node, token):
        val = token.value
        tag = token.tag

        if node.op == 'DUP':
            self.route_output(node, val, tag)
        elif node.op == 'CONST':
            # Trigger token triggers injection of constant
            self.route_output(node, node.constant_val, tag)
        elif node.op == 'INC_TAG':
            # Increments the iteration/context tag
            self.route_output(node, val, tag + 1)
        elif node.op == 'OUTPUT':
            print(f">>> [OUTPUT NODE {node.node_id}] Result: {val} (Tag: {tag})")
            self.execution_log.append(f"*** FINAL OUTPUT: {val} at Node {node.node_id} (Tag: {tag}) ***")

    def fire_binary(self, node, left, right):
        lv = left.value
        rv = right.value
        tag = left.tag # tag is identical

        if node.op == 'ADD':
            res = lv + rv
            self.route_output(node, res, tag)
        elif node.op == 'SUB':
            res = lv - rv
            self.route_output(node, res, tag)
        elif node.op == 'MUL':
            res = lv * rv
            self.route_output(node, res, tag)
        elif node.op == 'DIV':
            res = lv / rv
            self.route_output(node, res, tag)
        elif node.op == 'CMP_LE':
            res = lv <= rv
            self.route_output(node, res, tag)
        elif node.op == 'COND':
            # COND takes data on 'left' and boolean control on 'right'
            # routes data to 'true' or 'false' branch destinations
            cond_val = bool(rv)
            dest_key = 'true' if cond_val else 'false'

            if isinstance(node.destinations, dict):
                dests = node.destinations.get(dest_key, [])
                if not isinstance(dests, list):
                    dests = [dests]
                for d_id, d_port in dests:
                    self.inject_token(Token(lv, d_id, d_port, tag))
            else:
                self.execution_log.append(f"  [Error] COND Node {node.node_id} destinations must be a dictionary")

    def route_output(self, node, value, tag):
        """
        Routes the output value to all specified destinations.
        """
        if isinstance(node.destinations, list):
            for dest_id, dest_port in node.destinations:
                self.inject_token(Token(value, dest_id, dest_port, tag))

    def run_until_empty(self, limit=500):
        """Runs the simulation engine until token queue is empty or limit is reached."""
        while self.token_queue and self.step_count < limit:
            self.step()
        if self.step_count >= limit:
            print(f"Simulation execution limit reached ({limit} steps). Suspected infinite loop.")


# ==========================================
# Test Programs Setup
# ==========================================

def run_parallel_quadratic():
    """
    Computes (x^2 + y^2) * (x - y) in parallel.
    Shows simultaneous left-branch and right-branch activations.
    """
    print("\n" + "="*50)
    print("Program 1: Parallel Evaluation of (x^2 + y^2) * (x - y)")
    print("="*50)

    engine = DataflowEngine()

    # 1. Duplicate X to x^2 and (x - y)
    engine.add_node(Node(node_id=10, op='DUP', destinations=[(1, 'left'), (1, 'right'), (3, 'left')]))
    # 2. Duplicate Y to y^2 and (x - y)
    engine.add_node(Node(node_id=11, op='DUP', destinations=[(2, 'left'), (2, 'right'), (3, 'right')]))

    # 3. Arithmetic operations
    engine.add_node(Node(node_id=1, op='MUL', destinations=[(5, 'left')]))  # x * x
    engine.add_node(Node(node_id=2, op='MUL', destinations=[(5, 'right')])) # y * y
    engine.add_node(Node(node_id=3, op='SUB', destinations=[(6, 'right')])) # x - y

    # 4. Add x^2 + y^2
    engine.add_node(Node(node_id=5, op='ADD', destinations=[(6, 'left')]))  # (x^2 + y^2)

    # 5. Multiply (x^2 + y^2) * (x - y)
    engine.add_node(Node(node_id=6, op='MUL', destinations=[(7, 'unconditional')]))

    # 6. Output Node
    engine.add_node(Node(node_id=7, op='OUTPUT'))

    # Inject inputs: x=4, y=2
    # Expect: (4^2 + 2^2) * (4 - 2) = (16 + 4) * 2 = 20 * 2 = 40
    print("Injecting inputs: x = 4, y = 2")
    engine.inject_token(Token(value=4, dest_node=10, port='unconditional'))
    engine.inject_token(Token(value=2, dest_node=11, port='unconditional'))

    engine.run_until_empty()

    print("\nExecution Step Log:")
    for log in engine.execution_log:
        print(f"  {log}")


def run_iterative_factorial(n_val=5):
    """
    Computes factorial of N using a pipelined dataflow loop.
    Demonstrates context tags (Tag k -> Tag k+1).
    """
    print("\n" + "="*50)
    print(f"Program 2: Iterative Factorial loop of N = {n_val}")
    print("="*50)

    engine = DataflowEngine()

    # Node 1: Loop counter comparison. Compares 'i' (left) and 'N' (right)
    # Outputs boolean token to switches
    engine.add_node(Node(node_id=20, op='CMP_LE', destinations=[(21, 'right'), (22, 'right')]))

    # Node 21: Switch for 'i'. If true, goes to loop body. If false, discarded.
    engine.add_node(Node(node_id=21, op='COND', destinations={
        'true': [(23, 'left'), (24, 'left')],  # to loop body MULT and ADD
        'false': []                            # discard
    }))

    # Node 22: Switch for 'acc'. If true, goes to loop body. If false, goes to Output!
    engine.add_node(Node(node_id=22, op='COND', destinations={
        'true': [(23, 'right')],               # to loop body MULT
        'false': [(30, 'unconditional')]       # to final Output!
    }))

    # Node 23: Loop Body Mult (acc * i)
    engine.add_node(Node(node_id=23, op='MUL', destinations=[(25, 'unconditional')]))

    # Node 24: Loop Body Add (i + 1)
    # Since we need to add 1, we use a CONST node triggered by 'i' arrival
    engine.add_node(Node(node_id=24, op='ADD', destinations=[(26, 'unconditional')]))
    engine.add_node(Node(node_id=40, op='CONST', destinations=[(24, 'right')], constant_val=1))

    # Tag Incrementers to move to the next iteration (Tag k -> Tag k+1)
    engine.add_node(Node(node_id=25, op='INC_TAG', destinations=[(22, 'left')])) # loop acc back
    engine.add_node(Node(node_id=26, op='INC_TAG', destinations=[(21, 'left')])) # loop i back

    # Node 30: Final Output
    engine.add_node(Node(node_id=30, op='OUTPUT'))

    # Inject initial inputs with Tag 0
    # i = 1
    # acc = 1
    # N = n_val (routed directly as right operand to Node 20)
    # We also need to duplicate N for all tag iterations, but to keep the model clean,
    # we duplicate N to the comparator of ALL iterations by having N bypassed or constant-like.
    # In a dynamic dataflow, N is typically stored in a constant register or duplicated.
    # We will simulate the constant nature of N by injecting N for each tag or making the comparator use a constant.
    # Let's make Node 20 CMP_LE use a constant N = n_val for simplicity or route it!
    # Let's route N to Node 20 (right input) for multiple tags manually when CMP_LE fires,
    # or let's implement Node 20 as CMP_LE with N hardcoded as a constant_val!
    # Hardcoding N in Node 20 is super clean for simulation:
    engine.add_node(Node(node_id=20, op='CMP_LE', destinations=[(21, 'right'), (22, 'right')]))
    # Let's just feed N as a second token. For simplicity of matching, we'll route a CONST N token
    # or just let Node 20's right side match a dynamically supplied N.
    # Let's supply N dynamically with a DUP loop or just make Node 20 compare against N constant!
    # Let's modify DataflowEngine binary CMP_LE to use constant_val if right operand is missing, or just pass N along.
    # Actually, a brilliant way is to inject N tokens for tags 0, 1, 2, 3, 4, 5, etc.
    # Let's do that! We'll inject N tokens for all iterations up to N+1:
    for t in range(n_val + 2):
        engine.inject_token(Token(value=n_val, dest_node=20, port='right', tag=t))

    # Inject i=1 and acc=1 at tag 0
    engine.inject_token(Token(value=1, dest_node=21, port='left', tag=0))
    engine.inject_token(Token(value=1, dest_node=22, port='left', tag=0))

    # We also need to feed the initial 'i' to comparison node 20
    engine.inject_token(Token(value=1, dest_node=20, port='left', tag=0))

    # Since loop body updates 'i', we must route the incremented 'i' back to comparison node 20 as well!
    # So Node 26 (INC_TAG for 'i') should duplicate its output to BOTH Node 21 (left) and Node 20 (left)!
    engine.add_node(Node(node_id=26, op='INC_TAG', destinations=[(21, 'left'), (20, 'left')]))

    # Node 21 (COND) routes 'i' to Node 23 (left) and Node 24 (left) and Node 40 (left - trigger for CONST 1)
    engine.add_node(Node(node_id=21, op='COND', destinations={
        'true': [(23, 'left'), (24, 'left'), (40, 'left')],
        'false': []
    }))

    print(f"Executing factorial loop up to {n_val}")
    engine.run_until_empty()

    print("\nExecution Step Log Summary (First 40 steps):")
    for log in list(engine.execution_log)[:40]:
        print(f"  {log}")
    if len(engine.execution_log) > 40:
        print(f"  ... [truncated {len(engine.execution_log) - 40} steps] ...")


def main():
    run_parallel_quadratic()
    run_iterative_factorial(5)

if __name__ == "__main__":
    main()
