#!/usr/bin/env python3
"""
Unit tests for the Stochastic Computing (SC) Simulator.
Verified under pytest.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from stochastic_sim import (
    LFSR,
    StochasticGenerator,
    StochasticDecoder,
    StochasticArithmetic,
    StochasticFSM,
    StochasticNeuron,
    StochasticSignalFilter
)

def test_lfsr_basic():
    """Verify basic LFSR functionality, seed boundaries, and pseudo-random output range."""
    lfsr = LFSR(seed=42, width=8)
    assert lfsr.state == 42

    # Run for multiple steps, verify values are in range
    states = []
    for _ in range(255):
        val = lfsr.next_val()
        assert 0 <= val < 256
        states.append(val)

    # An 8-bit LFSR has a period of 2^8 - 1 = 255.
    # Verify that it does not return 0, and has generated unique states
    assert 0 not in states
    assert len(set(states)) == 255

    # Test lock-up state avoidance (seed=0 becomes 1)
    lfsr_zero = LFSR(seed=0, width=8)
    assert lfsr_zero.state == 1


def test_stochastic_generator_boundaries():
    """Verify that values outside [0, 1] for unipolar or [-1, 1] for bipolar are safely clamped."""
    # Unipolar boundaries
    stream_low = StochasticGenerator.to_unipolar(-0.5, 100)
    assert all(bit == 0 for bit in stream_low)

    stream_high = StochasticGenerator.to_unipolar(1.5, 100)
    assert all(bit == 1 for bit in stream_high)

    # Bipolar boundaries
    stream_bip_low = StochasticGenerator.to_bipolar(-2.0, 100)
    assert all(bit == 0 for bit in stream_bip_low) # target prob = (-2+1)/2 = -0.5 -> clamped to 0 -> all 0s

    stream_bip_high = StochasticGenerator.to_bipolar(2.0, 100)
    assert all(bit == 1 for bit in stream_bip_high) # target prob = (2+1)/2 = 1.5 -> clamped to 1 -> all 1s


def test_unipolar_generation_and_decoding():
    """Verify unipolar conversion and decoding with pseudo-random streams."""
    lfsr = LFSR(seed=55, width=16)
    target = 0.70
    length = 2048

    stream = StochasticGenerator.to_unipolar(target, length, lfsr)
    decoded = StochasticDecoder.decode_unipolar(stream)

    # With a length of 2048, the decoded value should be close to 0.70
    assert abs(decoded - target) < 0.05


def test_bipolar_generation_and_decoding():
    """Verify bipolar conversion and decoding with pseudo-random streams."""
    lfsr = LFSR(seed=999, width=16)
    target = -0.40
    length = 2048

    stream = StochasticGenerator.to_bipolar(target, length, lfsr)
    decoded = StochasticDecoder.decode_bipolar(stream)

    assert abs(decoded - target) < 0.05


def test_multiply_unipolar():
    """Test AND-gate multiplication with explicit inputs."""
    stream_a = [1, 0, 1, 1, 0]
    stream_b = [0, 1, 1, 0, 0]
    expected = [0, 0, 1, 0, 0]

    result = StochasticArithmetic.multiply_unipolar(stream_a, stream_b)
    assert result == expected


def test_multiply_bipolar():
    """Test XNOR-gate multiplication with explicit inputs."""
    stream_a = [1, 0, 1, 1, 0]
    stream_b = [1, 1, 0, 1, 0]
    # XNOR: 1==1 -> 1, 0==1 -> 0, 1==0 -> 0, 1==1 -> 1, 0==0 -> 1
    expected = [1, 0, 0, 1, 1]

    result = StochasticArithmetic.multiply_bipolar(stream_a, stream_b)
    assert result == expected


def test_add_weighted():
    """Test MUX-based weighted addition with explicit inputs."""
    stream_a =   [1, 1, 1, 1, 1]
    stream_b =   [0, 0, 0, 0, 0]
    stream_sel = [1, 0, 1, 0, 1] # select A on bits 0, 2, 4 and B on bits 1, 3
    expected =   [1, 0, 1, 0, 1]

    result = StochasticArithmetic.add_weighted(stream_a, stream_b, stream_sel)
    assert result == expected


def test_fsm_tanh():
    """Verify the Saturating Finite State Machine behavior for Tanh execution."""
    # Test high saturation
    fsm_up = StochasticFSM(states=8)
    # Stream of all 1s should force the state to saturation (+4)
    stream_ones = [1] * 20
    out_ones = fsm_up.process_bipolar_tanh(stream_ones)
    assert fsm_up.state == 4
    # All output bits should be 1
    assert all(bit == 1 for bit in out_ones)

    # Test low saturation
    fsm_down = StochasticFSM(states=8)
    # Stream of all 0s should force state to -4
    stream_zeros = [0] * 20
    out_zeros = fsm_down.process_bipolar_tanh(stream_zeros)
    assert fsm_down.state == -4
    # Output bits should be 0 (except potentially first couple depending on initial state, but over 20 steps, mostly 0)
    assert out_zeros[-10:] == [0] * 10


def test_stochastic_neuron():
    """Verify the functional execution of a Stochastic Artificial Neuron workload."""
    weights = [0.5, -0.2]
    inputs = [0.8, 0.4]

    neuron = StochasticNeuron(weights, states=8)
    decoded, expected = neuron.evaluate(inputs, length=1024)

    # Assert output is mathematically sensible
    assert -1.0 <= decoded <= 1.0
    assert abs(decoded - expected) < 0.25


def test_stochastic_signal_filter():
    """Verify 1D moving average signal smoothing in the stochastic domain."""
    signal = [0.1, 0.9, 0.8, 0.2]
    filtered = StochasticSignalFilter.filter_signal(signal, kernel_width=3, length=512)

    assert len(filtered) == len(signal)
    assert all(0.0 <= x <= 1.0 for x in filtered)
    # The smoothed version of 0.9 in the middle of 0.1 and 0.8 should decrease
    assert filtered[1] < 0.9
