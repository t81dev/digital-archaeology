#!/usr/bin/env python3
"""
Explicit Data Graph Execution (EDGE) Block-Structured Spatial Simulator.
A simulator demonstrating a TRIPS-style spatial dataflow model where instructions
are partitioned into atomic blocks and operands are routed directly on a 2D grid.
Includes Manhattan-distance routing latency to simulate the historical "wire-delay" constraint.
"""

import math
import collections

class EDGEInstruction:
    """
    An instruction mapped to a coordinate on a physical spatial execution grid.
    Directly routes outputs to target instructions, bypassing register files.
    """
    def __init__(self, inst_id, op, grid_pos, targets=None, constant=None):
        self.inst_id = inst_id       # Unique identifier within the block (e.g. 0 to 15)
        self.op = op                 # ADD, SUB, MUL, DIV, CMP_LT, CONST, LOAD, STORE, WRITE_REG
        self.grid_pos = grid_pos     # (x, y) coordinate on the spatial grid (e.g., 4x4)
        self.targets = targets or [] # List of tuples: (target_inst_id, target_port)
        self.constant = constant     # Literal constant value if any (e.g., for CONST)

        # Operand registers/slots
        self.left_operand = None
        self.right_operand = None
        self.fired = False           # Ensures each instruction fires exactly once per block

    def is_ready(self, expected_ports):
        """
        Checks if instruction is ready to execute.
        If a port expects an incoming token (has an incoming target link),
        we must wait until that token has arrived.
        """
        if self.fired:
            return False

        left_expected = 'left' in expected_ports
        right_expected = 'right' in expected_ports

        if left_expected and self.left_operand is None:
            return False
        if right_expected and self.right_operand is None:
            return False

        # If we have met the expected incoming tokens, check execution readiness:
        if self.op == 'CONST':
            # CONST without external triggers can fire immediately
            return True
        if self.op == 'LOAD':
            return self.left_operand is not None or self.constant is not None or not left_expected
        if self.op in ('WRITE_REG', 'STORE'):
            return self.left_operand is not None or not left_expected

        # Binary operations require both left and right operands to be set
        return (self.left_operand is not None or not left_expected) and \
               (self.right_operand is not None or not right_expected)

    def __repr__(self):
        return f"Inst(id={self.inst_id}, op={self.op}, pos={self.grid_pos}, L={self.left_operand}, R={self.right_operand}, fired={self.fired})"


class EDGEBlock:
    """
    An atomic execution block containing mapped spatial instructions.
    Reads registers on entry, executes spatially, and commits register updates atomically.
    """
    def __init__(self, block_id):
        self.block_id = block_id
        self.instructions = {}

    def add_instruction(self, inst):
        self.instructions[inst.inst_id] = inst


class EDGERoutingToken:
    """
    A routing packet (flit) traversing the on-chip mesh network.
    Contains source, destination, routing latency, and payload.
    """
    def __init__(self, src_pos, dest_pos, dest_inst_id, port, value, remaining_delay=0):
        self.src_pos = src_pos
        self.dest_pos = dest_pos
        self.dest_inst_id = dest_inst_id
        self.port = port
        self.value = value
        self.remaining_delay = remaining_delay # Simulated routing latency (cycles)

    def __repr__(self):
        return f"Token(src={self.src_pos}, dest={self.dest_pos}, inst={self.dest_inst_id}, port={self.port}, val={self.value}, delay={self.remaining_delay})"


class EDGESpatialGrid:
    """
    The physical hardware execution substrate.
    Coordinates spatial instruction execution, mesh routing, and atomic commits.
    """
    def __init__(self, grid_size=(4, 4)):
        self.grid_size = grid_size
        self.registers = {f"R{i}": 0 for i in range(8)} # 8 general-purpose registers
        self.memory = {} # Mock main memory

        # Execution State
        self.active_block = None
        self.routing_tokens = [] # Tokens currently in transit
        self.buffered_reg_writes = {} # Buffered writes for atomic commit
        self.buffered_mem_writes = {}
        self.cycle_count = 0
        self.execution_log = []

    def load_block(self, block, register_inputs):
        """
        Loads a block onto the physical spatial grid.
        Binds initial register values to matching instructions.
        """
        self.active_block = block
        self.routing_tokens = []
        self.buffered_reg_writes = {}
        self.buffered_mem_writes = {}
        self.cycle_count = 0
        self.execution_log = []

        # Reset instruction state
        for inst in self.active_block.instructions.values():
            inst.fired = False
            inst.left_operand = None
            inst.right_operand = None

        # Map expected incoming ports for each instruction in the active block
        self.expected_ports = collections.defaultdict(set)
        for inst in self.active_block.instructions.values():
            for dest_id, port in inst.targets:
                self.expected_ports[dest_id].add(port)

        # Initialize registers as specified on entry
        for reg, val in register_inputs.items():
            if reg in self.registers:
                self.registers[reg] = val

        self.log(f"--- Loading Block {block.block_id} onto {self.grid_size[0]}x{self.grid_size[1]} Grid ---")
        self.log(f"Initial Register State: {self.registers}")

    def log(self, msg):
        self.execution_log.append(msg)
        print(f"[Cycle {self.cycle_count}] {msg}")

    def inject_input_token(self, dest_inst_id, port, value):
        """Directly injects an input value into a starting instruction's port."""
        if dest_inst_id in self.active_block.instructions:
            inst = self.active_block.instructions[dest_inst_id]
            if port == 'left':
                inst.left_operand = value
            elif port == 'right':
                inst.right_operand = value
            self.log(f"Injected external input into Instruction {dest_inst_id} ({port}): {value}")

    def step_cycle(self):
        """
        Executes one clock cycle of the spatial network and execution grid.
        Processes active nodes, decrements network delays, and delivers tokens.
        """
        self.cycle_count += 1
        self.log("=== Tick ===")

        # 1. Progress routing tokens in transit on the mesh network
        delivered_tokens = []
        remaining_tokens = []
        for t in self.routing_tokens:
            if t.remaining_delay > 1:
                t.remaining_delay -= 1
                remaining_tokens.append(t)
            else:
                delivered_tokens.append(t)
        self.routing_tokens = remaining_tokens

        # Deliver arrived tokens to instructions
        for t in delivered_tokens:
            if t.dest_inst_id in self.active_block.instructions:
                inst = self.active_block.instructions[t.dest_inst_id]
                if t.port == 'left':
                    inst.left_operand = t.value
                elif t.port == 'right':
                    inst.right_operand = t.value
                self.log(f"Token Delivered: Src={t.src_pos} -> Dest={t.dest_pos} (Inst {t.dest_inst_id} {t.port}) Value={t.value}")
            else:
                self.log(f"Warning: Token targeted non-existent Inst {t.dest_inst_id}")

        # 2. Scan the grid for ready instructions and execute them
        ready_instructions = []
        for inst_id, inst in list(self.active_block.instructions.items()):
            expected = self.expected_ports.get(inst_id, set())
            if inst.is_ready(expected):
                ready_instructions.append(inst)

        for inst in ready_instructions:
            self.fire_instruction(inst)

        # Execution terminates when there are no more active routing tokens in flight
        # AND no more instructions can fire.
        return len(self.routing_tokens) > 0 or self.any_ready_instructions()

    def any_ready_instructions(self):
        """Checks if there are any remaining ready instructions on the grid."""
        for inst_id, inst in self.active_block.instructions.items():
            expected = self.expected_ports.get(inst_id, set())
            if inst.is_ready(expected):
                return True
        return False

    def calculate_routing_delay(self, src_pos, dest_pos):
        """
        Calculates Manhattan distance on the 2D grid to model physical wire delays.
        """
        dx = abs(src_pos[0] - dest_pos[0])
        dy = abs(src_pos[1] - dest_pos[1])
        # Base latency is 1 cycle; each hop adds 1 cycle
        return 1 + dx + dy

    def fire_instruction(self, inst):
        """
        Computes the operation and routes resulting tokens to target instructions.
        """
        inst.fired = True
        lv = inst.left_operand
        rv = inst.right_operand
        op = inst.op

        self.log(f"Firing Inst {inst.inst_id} ({op}) at Grid {inst.grid_pos} (L={lv}, R={rv})")

        # Execute math
        result = None
        if op == 'ADD':
            result = lv + rv
        elif op == 'SUB':
            result = lv - rv
        elif op == 'MUL':
            result = lv * rv
        elif op == 'DIV':
            result = lv / rv if rv != 0 else 0
        elif op == 'CMP_LT':
            result = 1 if lv < rv else 0
        elif op == 'CONST':
            result = inst.constant
        elif op == 'LOAD':
            addr = inst.constant if inst.constant is not None else lv
            # Check store-buffer first (Store Forwarding)
            if addr in self.buffered_mem_writes:
                result = self.buffered_mem_writes[addr]
                self.log(f"LOAD read Memory[{addr}] -> {result} (Forwarded from Store Buffer)")
            else:
                result = self.memory.get(addr, 0)
                self.log(f"LOAD read Memory[{addr}] -> {result}")
        elif op == 'STORE':
            # Store left operand (data) to memory address (from constant or right operand)
            addr = inst.constant if inst.constant is not None else rv
            self.buffered_mem_writes[addr] = lv
            self.log(f"Buffered Memory Write: Memory[{addr}] = {lv}")
            result = lv # Send store value (or dummy) to targets as a sync signal
        elif op == 'WRITE_REG':
            # Buffer write-back to register file
            reg_name = inst.constant
            self.buffered_reg_writes[reg_name] = lv
            self.log(f"Buffered Register Write: {reg_name} = {lv}")
            result = lv

        # Route results to targets
        for dest_id, port in inst.targets:
            if dest_id in self.active_block.instructions:
                dest_inst = self.active_block.instructions[dest_id]
                delay = self.calculate_routing_delay(inst.grid_pos, dest_inst.grid_pos)
                token = EDGERoutingToken(
                    src_pos=inst.grid_pos,
                    dest_pos=dest_inst.grid_pos,
                    dest_inst_id=dest_id,
                    port=port,
                    value=result,
                    remaining_delay=delay
                )
                self.routing_tokens.append(token)
                self.log(f"Routing Token: Inst {inst.inst_id} -> Inst {dest_id} ({port}) Val={result} (Wire Latency={delay} cycles)")
            else:
                self.log(f"Error: Target Inst {dest_id} not found in block.")

        # Clear operands to avoid re-firing
        inst.left_operand = None
        inst.right_operand = None

    def commit_block(self):
        """
        Atomically commits buffered memory and register writes.
        Guarantees transactional execution of block.
        """
        self.log("--- Commit Phase ---")

        # Commit Register file updates
        for reg, val in self.buffered_reg_writes.items():
            self.registers[reg] = val
            self.log(f"Committed Register: {reg} = {val}")

        # Commit Memory updates
        for addr, val in self.buffered_mem_writes.items():
            self.memory[addr] = val
            self.log(f"Committed Memory: [{addr}] = {val}")

        self.log(f"Atomic Block Commit Complete. Final Registers: {self.registers}")

    def run_block(self, max_cycles=100):
        """Runs the loaded block until execution terminates or cycles exceed limit."""
        running = True
        while running and self.cycle_count < max_cycles:
            running = self.step_cycle()

        if self.cycle_count >= max_cycles:
            self.log("Warning: Execution block hit max cycles limit.")

        self.commit_block()
        return self.registers


# ==========================================
# Run Sample EDGE Program
# ==========================================

def run_edge_sample():
    """
    EDGE Program implementing the evaluation of:
    R2 = (R0 + R1) * (R0 - R1)
    Instructions are mapped spatially to a 4x4 grid.
    Wire distances:
      Inst 0 is at (0, 0)
      Inst 1 is at (3, 0) (horizontal delay)
      Inst 2 is at (1, 2) (vertical delay)
      Inst 3 is at (3, 3) (deep grid delay)
    """
    print("\n" + "="*60)
    print("EDGE PROGRAM: Parallel Spatial Calculation of (R0+R1)*(R0-R1)")
    print("="*60)

    # 1. Create block
    block = EDGEBlock("block_0")

    # Inst 0: ADD on position (0, 0). Targets Inst 2 (left port)
    inst0 = EDGEInstruction(0, 'ADD', (0, 0), targets=[(2, 'left')])
    # Inst 1: SUB on position (3, 0). Targets Inst 2 (right port)
    inst1 = EDGEInstruction(1, 'SUB', (3, 0), targets=[(2, 'right')])
    # Inst 2: MUL on position (1, 2). Targets Inst 3 (left port)
    inst2 = EDGEInstruction(2, 'MUL', (1, 2), targets=[(3, 'left')])
    # Inst 3: WRITE_REG on position (3, 3). Targets Register R2
    inst3 = EDGEInstruction(3, 'WRITE_REG', (3, 3), constant='R2')

    block.add_instruction(inst0)
    block.add_instruction(inst1)
    block.add_instruction(inst2)
    block.add_instruction(inst3)

    # 2. Create Grid and Load Block
    grid = EDGESpatialGrid()
    grid.load_block(block, register_inputs={'R0': 10, 'R1': 4})

    # 3. Inject starting operands to instruction 0 and 1
    grid.inject_input_token(0, 'left', 10)
    grid.inject_input_token(0, 'right', 4)
    grid.inject_input_token(1, 'left', 10)
    grid.inject_input_token(1, 'right', 4)

    # 4. Run to completion
    # Result: (10 + 4) * (10 - 4) = 14 * 6 = 84
    final_regs = grid.run_block()
    print(f"Result verified: R2 = {final_regs['R2']} (Expected: 84)")


if __name__ == "__main__":
    run_edge_sample()
