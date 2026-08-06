#!/usr/bin/env python3
"""
Unit tests for the Neuromorphic Spiking Simulator.
Verified under pytest.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from spiking_sim import SpikingNeuron, Synapse, SpikingNetwork

def test_lif_neuron_leak_and_fire():
    """Verify standard LIF neuron exponential leak, threshold firing, and refractory cycle dynamics."""
    neuron = SpikingNeuron(0, v_rest=0.0, v_th=1.0, tau_m=5.0, v_reset=0.0, refractory_cycles=2)

    # 1. No inputs - should leak to v_rest (0.0)
    neuron.v = 0.5
    spike = neuron.step(0, 0.0)
    assert spike == 0
    assert neuron.v < 0.5 # Leaked down towards 0.0

    # 2. Large inputs - should fire
    spike = neuron.step(1, 1.5)
    assert spike == 1 # Fired!
    assert neuron.v == 0.0 # Reset
    assert neuron.refractory_timer == 2

    # 3. In refractory period - should remain clamped to v_reset despite input stimulus
    spike_ref = neuron.step(2, 2.0)
    assert spike_ref == 0
    assert neuron.v == 0.0


def test_stdp_synapse():
    """Verify Spike-Timing-Dependent Plasticity (STDP) weight potentiation and depression."""
    syn = Synapse(0, 1, initial_weight=1.0, max_weight=2.0, w_min=0.1)

    # Pre fired before Post -> Potentiation
    syn.apply_stdp(pre_spike_time=10, post_spike_time=15, pre_fired=True, post_fired=True)
    assert syn.weight > 1.0

    # Post fired before Pre -> Depression
    syn_dep = Synapse(0, 1, initial_weight=1.0, max_weight=2.0, w_min=0.1)
    syn_dep.apply_stdp(pre_spike_time=20, post_spike_time=15, pre_fired=True, post_fired=True)
    assert syn_dep.weight < 1.0


def test_spiking_network():
    """Verify multi-neuron networks and AER spike log propagation."""
    net = SpikingNetwork()
    net.add_neuron(SpikingNeuron(0, tau_m=5.0))
    net.add_neuron(SpikingNeuron(1, tau_m=10.0))
    net.add_synapse(0, 1, weight=1.0)

    # Inject stimulus to neuron 0 to fire on step 0
    stim = {
        0: [1.2, 0.0, 0.0, 0.0],
        1: [0.0, 0.0, 0.0, 0.0]
    }

    net.run_simulation(steps=4, external_stimuli=stim)

    # Pre-synaptic spike should occur at step 0
    assert len(net.aer_log) >= 1
    # Check that AER event for neuron 0 is logged
    has_zero_spiked = any(nid == 0 for t, nid in net.aer_log)
    assert has_zero_spiked
