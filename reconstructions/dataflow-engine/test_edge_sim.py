#!/usr/bin/env python3
"""
Unit tests for the Explicit Data Graph Execution (EDGE) simulator.
Verifies arithmetic routing delays, atomic commits, and memory loads/stores.
"""

import sys
import os
import pytest

# Add current directory to path to enable clean imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edge_sim import EDGEBlock, EDGEInstruction, EDGESpatialGrid

def test_manhattan_routing_delay():
    """
    Verifies that wire delays are calculated correctly using Manhattan distance.
    Base delay of 1 + abs(dx) + abs(dy).
    """
    grid = EDGESpatialGrid()
    # Identical position: 1 cycle
    assert grid.calculate_routing_delay((1, 1), (1, 1)) == 1
    # 1 cell away: 1 + 1 = 2 cycles
    assert grid.calculate_routing_delay((0, 0), (0, 1)) == 2
    # Diagonal jump: 1 + 2 + 1 = 4 cycles
    assert grid.calculate_routing_delay((0, 0), (2, 1)) == 4


def test_edge_arithmetic_pipeline():
    """
    Tests an arithmetic dataflow chain:
    R3 = (R0 - R1) + CONST(5)
    Values: R0=15, R1=7
    Expected: (15 - 7) + 5 = 13
    """
    block = EDGEBlock("test_arith")

    # Inst 0: SUB on (0, 0). Targets Inst 2 left
    inst0 = EDGEInstruction(0, 'SUB', (0, 0), targets=[(2, 'left')])
    # Inst 1: CONST on (1, 1). Targets Inst 2 right
    inst1 = EDGEInstruction(1, 'CONST', (1, 1), targets=[(2, 'right')], constant=5)
    # Inst 2: ADD on (0, 2). Targets Inst 3 left
    inst2 = EDGEInstruction(2, 'ADD', (0, 2), targets=[(3, 'left')])
    # Inst 3: WRITE_REG on (3, 3) with target register R3
    inst3 = EDGEInstruction(3, 'WRITE_REG', (3, 3), constant='R3')

    block.add_instruction(inst0)
    block.add_instruction(inst1)
    block.add_instruction(inst2)
    block.add_instruction(inst3)

    grid = EDGESpatialGrid()
    grid.load_block(block, register_inputs={'R0': 15, 'R1': 7})

    # Inject operands
    grid.inject_input_token(0, 'left', 15)
    grid.inject_input_token(0, 'right', 7)
    # Trigger CONST instruction
    grid.inject_input_token(1, 'left', 1)

    final_regs = grid.run_block()
    assert final_regs['R3'] == 13


def test_edge_load_store():
    """
    Tests spatial LOAD and STORE sequence:
    Memory[100] = 42
    R4 = Memory[100]

    To avoid the RAW (Read-After-Write) hazard, the STORE targets the LOAD's left_operand
    with a synchronizing trigger signal, ensuring that LOAD fires only AFTER STORE has committed
    its value to memory.
    """
    block = EDGEBlock("test_mem")

    # Inst 0: CONST on (0, 0). Routes value 42 to Inst 1 (STORE) left (data)
    inst0 = EDGEInstruction(0, 'CONST', (0, 0), targets=[(1, 'left')], constant=42)

    # Inst 1: STORE on (0, 2). Stores left operand to address 100.
    # Targets Inst 2 with a synchronization token when complete.
    inst1 = EDGEInstruction(1, 'STORE', (0, 2), targets=[(2, 'left')], constant=100)

    # Inst 2: LOAD on (2, 2). Reads Memory[100]. Targets Inst 3 left.
    # Its activation is guarded by the left_operand signal arriving from STORE (Inst 1).
    inst2 = EDGEInstruction(2, 'LOAD', (2, 2), targets=[(3, 'left')], constant=100)

    # Inst 3: WRITE_REG on (3, 3). Writes to register R4.
    inst3 = EDGEInstruction(3, 'WRITE_REG', (3, 3), constant='R4')

    block.add_instruction(inst0)
    block.add_instruction(inst1)
    block.add_instruction(inst2)
    block.add_instruction(inst3)

    grid = EDGESpatialGrid()
    grid.load_block(block, register_inputs={})

    # Trigger first constant instruction
    grid.inject_input_token(0, 'left', 1)

    final_regs = grid.run_block()

    # Check intermediate memory updates were committed
    assert grid.memory[100] == 42
    assert final_regs['R4'] == 42
