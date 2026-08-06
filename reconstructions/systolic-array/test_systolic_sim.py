# test_systolic_sim.py
# Pytest suite for Systolic Array Cycle & Energy Proxy Simulator

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from systolic_sim import SystolicArraySimulator

def test_systolic_array_dimensions_and_reset():
    sim = SystolicArraySimulator(4, 4)
    assert sim.rows == 4
    assert sim.cols == 4

    # Set custom value to check reset
    sim.grid[0][0].weight = 5.0
    sim.grid[1][1].accumulator = 10.0
    sim.cycles = 15

    sim.reset_array()
    assert sim.grid[0][0].weight == 0.0
    assert sim.grid[1][1].accumulator == 0.0
    assert sim.cycles == 0

def test_systolic_matrix_multiplication_correctness():
    # 3x2 * 2x3 -> 3x3
    A = [
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0]
    ]
    B = [
        [7.0, 8.0, 9.0],
        [1.0, 2.0, 3.0]
    ]

    expected = [
        [9.0, 12.0, 15.0],
        [25.0, 32.0, 39.0],
        [41.0, 52.0, 63.0]
    ]

    sim = SystolicArraySimulator(4, 4)

    # Weight-Stationary
    res_ws = sim.simulate_weight_stationary(A, B)
    # Check only up to active 3x3 output
    for r in range(3):
        for c in range(3):
            assert abs(res_ws[r][c] - expected[r][c]) < 1e-5

    # Output-Stationary
    res_os = sim.simulate_output_stationary(A, B)
    for r in range(3):
        for c in range(3):
            assert abs(res_os[r][c] - expected[r][c]) < 1e-5

def test_systolic_dimension_validation():
    sim = SystolicArraySimulator(2, 2)

    # For WS: K=3 exceeds rows=2
    A_ws = [
        [1.0, 2.0, 3.0]
    ]
    B_ws = [
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0]
    ]

    with pytest.raises(ValueError):
        sim.simulate_weight_stationary(A_ws, B_ws)

    # For OS: M=3 exceeds rows=2
    A_os = [
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0]
    ]
    B_os = [
        [1.0, 2.0],
        [3.0, 4.0]
    ]
    with pytest.raises(ValueError):
        sim.simulate_output_stationary(A_os, B_os)

def test_energy_metrics_and_proxies():
    A = [[2.0]]
    B = [[3.0]]

    sim = SystolicArraySimulator(2, 2)
    sim.simulate_weight_stationary(A, B)
    metrics = sim.get_energy_metrics()

    assert metrics["cycles"] > 0
    assert metrics["mac_operations"] == 1
    assert metrics["sram_reads"] == 2 # 1 weight + 1 input
    assert metrics["sram_writes"] == 1 # 1 output C[0][0]
    assert metrics["total_energy_proxy"] > 0.0
