# test_sfq_sim.py
# Unit tests for the Cryogenic Superconducting & SFQ Simulator

import pytest
from sfq_sim import DFlipFlop, SFQAndGate, CryogenicEnergyModel, SFQSimulator, PHI_0

def test_dff_nominal():
    """Verify that a DFF correctly stores flux state and emits on CLK."""
    dff = DFlipFlop("DFF_Test", setup_time=3.0, prop_delay=5.0)
    assert dff.state == 0

    # Send D pulse at 10 ps
    dff.process_pulse_d(10.0)
    assert dff.state == 1

    # Send CLK pulse at 20 ps (clean separation)
    fired, q_t, warnings = dff.process_pulse_clk(20.0, jitter=0.0)
    assert fired is True
    assert q_t == 25.0
    assert dff.state == 0
    assert len(warnings) == 0

    # CLK again should not fire
    fired2, _, _ = dff.process_pulse_clk(30.0, jitter=0.0)
    assert fired2 is False


def test_dff_setup_violation():
    """Verify setup-time warning triggers and state falls to 0 under metastability."""
    dff = DFlipFlop("DFF_Test", setup_time=3.0, prop_delay=5.0)

    # D at 53.5 ps, CLK at 55.0 ps (difference of 1.5 ps < 3.0 ps setup_time)
    dff.process_pulse_d(53.5)
    fired, q_t, warnings = dff.process_pulse_clk(55.0, jitter=0.0)

    assert fired is False
    assert dff.state == 0
    assert len(warnings) == 1
    assert "Setup-time violation" in warnings[0]


def test_and_gate_nominal():
    """Verify stateful coincidence behavior of RSFQ AND gate."""
    and_gate = SFQAndGate("AND_Test", prop_delay=6.0)
    assert and_gate.state_a == 0
    assert and_gate.state_b == 0

    # Only input A pulses
    and_gate.process_pulse_a(10.0)
    assert and_gate.state_a == 1
    assert and_gate.state_b == 0

    fired, _, _ = and_gate.process_pulse_clk(20.0)
    assert fired is False
    # States should reset on CLK
    assert and_gate.state_a == 0
    assert and_gate.state_b == 0

    # Both pulse
    and_gate.process_pulse_a(30.0)
    and_gate.process_pulse_b(31.0)
    fired2, q_t, _ = and_gate.process_pulse_clk(40.0)
    assert fired2 is True
    assert q_t == 46.0


def test_energy_model():
    """Verify thermodynamic calculation of critical energy and cooling penalties."""
    # Critical Current 100 uA
    model = CryogenicEnergyModel(temp_cold=4.2, temp_warm=300.0, critical_current=1e-4, pct_carnot_efficiency=0.01)

    # E_s = 100 uA * Phi_0 = 100 uA * 2.0678e-15 Wb = 2.0678e-19 Joules
    expected_es = 1e-4 * PHI_0
    assert model.get_switching_energy() == pytest.approx(expected_es)

    # Static Power = num_lines * (V_bias^2 / R_bias)
    # lines = 10, V = 1 mV, R = 10 Ohm -> 10 * (1e-6 / 10) = 1e-6 W
    model.v_bias = 1e-3
    model.r_bias = 10.0
    assert model.get_static_power(num_bias_lines=10, ersfq_mode=False) == pytest.approx(1e-6)
    assert model.get_static_power(num_bias_lines=10, ersfq_mode=True) == 0.0

    # Carnot COP at 4.2 K = 4.2 / (300 - 4.2) = 4.2 / 295.8 = 0.01419878
    # COP actual = 0.01419878 * 0.01 (1%) = 0.0001419878
    # cooling penalty = 1 / 0.0001419878 = 7042.857
    assert model.get_refrigeration_penalty() == pytest.approx(7042.857, rel=1e-3)


def test_simulator_pipeline():
    """Verify the high-level simulator schedules D and CLK streams."""
    sim = SFQSimulator(temp_kelvin=4.2)

    # 3 pairs of clean pulses
    d_times = [10.0, 40.0, 70.0]
    clk_times = [20.0, 50.0, 80.0]

    res = sim.simulate_dff_pipeline(d_times, clk_times)
    assert len(res["q_pulses"]) == 3
    assert len(res["warnings"]) == 0

    # Calculate timing jitter at room temp vs 4.2 K
    j_4k = [sim.calculate_jitter() for _ in range(100)]
    sim.temp = 300.0
    j_300k = [sim.calculate_jitter() for _ in range(100)]

    # Standard deviation at 300 K should be larger than 4.2 K
    var_4k = sum(x**2 for x in j_4k) / 100
    var_300k = sum(x**2 for x in j_300k) / 100
    assert var_300k > var_4k
