import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
import math
from analog_optical_sim import Complex, AnalogComputer, OpticalMatrixAccelerator, ReversibleSimulator

def test_complex_math():
    """Verify standard operations on our zero-dependency complex number class."""
    c1 = Complex(3.0, 4.0)
    c2 = Complex(1.0, -2.0)

    # Abs / magnitude
    assert math.isclose(c1.abs(), 5.0)

    # Addition
    c3 = c1 + c2
    assert c3.real == 4.0
    assert c3.imag == 2.0

    # Subtraction
    c4 = c1 - c2
    assert c4.real == 2.0
    assert c4.imag == 6.0

    # Multiplication
    c5 = c1 * c2
    # (3 + 4i)(1 - 2i) = 3 - 6i + 4i - 8i^2 = 3 - 2i + 8 = 11 - 2i
    assert c5.real == 11.0
    assert c5.imag == -2.0

    # Scalar multiplication
    c6 = 2.0 * c1
    assert c6.real == 6.0
    assert c6.imag == 8.0

    # Polar creation
    c_p = Complex.polar(2.0, math.pi / 2.0)
    assert math.isclose(c_p.real, 0.0, abs_tol=1e-7)
    assert math.isclose(c_p.imag, 2.0)


def test_analog_computer_simulation():
    """Verify that the analog computer simulates 2nd-order system and saturates properly."""
    # Underdamped system
    comp = AnalogComputer(zeta=0.1, omega_n=2.0)

    # Perfect digital run vs analog run with no noise/drift
    times, disp, vel, acc, ideal = comp.solve(
        y0=2.0, dy0=0.0, duration=2.0, dt=0.01,
        enable_noise=False, enable_drift=False
    )

    # Check length
    assert len(times) > 100
    assert len(disp) == len(ideal)

    # Without noise or drift, physical model should track ideal mathematical trajectory closely
    for d, i in zip(disp, ideal):
        assert abs(d - i) < 0.1  # small difference due to integration scheme/calibration tolerances

    # Test saturation limits
    comp_sat = AnalogComputer(zeta=0.1, omega_n=10.0, max_voltage=1.0)
    _, disp_sat, _, _, _ = comp_sat.solve(
        y0=5.0, dy0=5.0, duration=1.0, dt=0.01,
        enable_noise=False, enable_drift=False
    )
    for val in disp_sat:
        assert abs(val) <= 1.0


def test_optical_wave_accelerator():
    """Verify unitary matrix transformations and coherent wave interference."""
    # Create an accelerator representing standard unitary mapping
    # theta = pi/2, phi = 0
    acc = OpticalMatrixAccelerator(theta=math.pi / 2.0, phi=0.0, laser_power=1.0)

    # Ideal transfer matrix checking
    u_matrix = acc.get_ideal_unitary_matrix()
    assert len(u_matrix) == 2
    assert len(u_matrix[0]) == 2

    # Check unitary property: W_dagger * W = I
    w00 = u_matrix[0][0]
    w01 = u_matrix[0][1]
    w10 = u_matrix[1][0]
    w11 = u_matrix[1][1]

    w00_c = w00.conj()
    w01_c = w01.conj()
    w10_c = w10.conj()
    w11_c = w11.conj()

    norm_col1 = (w00_c * w00).real + (w10_c * w10).real
    assert math.isclose(norm_col1, 1.0)

    off_diag = (w00_c * w01) + (w10_c * w11)
    assert math.isclose(off_diag.real, 0.0, abs_tol=1e-7)
    assert math.isclose(off_diag.imag, 0.0, abs_tol=1e-7)

    # Propagate waves through multiplier without noise
    fields, intensities = acc.run_multiplication(x1=1.0, x2=0.0, enable_noise=False)

    # Outputs
    assert len(fields) == 2
    assert len(intensities) == 2

    # Verify constructive / destructive wave power measurements
    input_power = 1.0**2 + 0.0**2
    output_power = intensities[0] + intensities[1]
    assert math.isclose(input_power, output_power)


def test_reversible_and_adiabatic_simulation():
    """Verify standard gates, Bennett uncomputation, and adiabatic vs standard CMOS limits."""
    # Room temp simulation (300K)
    sim = ReversibleSimulator(temp_kelvin=300.0)

    # Standard gates verification
    assert sim.gate_not(1) == 0
    assert sim.gate_not(0) == 1

    assert sim.gate_cnot(1, 0) == (1, 1)
    assert sim.gate_cnot(0, 1) == (0, 1)

    assert sim.gate_toffoli(1, 1, 0) == (1, 1, 1)
    assert sim.gate_toffoli(1, 0, 1) == (1, 0, 1)

    assert sim.gate_fredkin(1, 1, 0) == (1, 0, 1)
    assert sim.gate_fredkin(0, 1, 0) == (0, 1, 0)

    # Landauer limit math validation
    # E_limit = kB * T * ln(2)
    expected_limit = 1.380649e-23 * 300.0 * math.log(2.0)
    assert math.isclose(sim.landauer_limit(), expected_limit)

    # Cryogenic temperature verification (4.0 K)
    sim_cryo = ReversibleSimulator(temp_kelvin=4.0)
    expected_cryo_limit = 1.380649e-23 * 4.0 * math.log(2.0)
    assert math.isclose(sim_cryo.landauer_limit(), expected_cryo_limit)

    # Bennett's Uncomputation Pipeline transitions checking
    pipeline_states = sim.simulate_bennett_uncomputation(x=1)
    assert len(pipeline_states) == 5

    # Check that in Phase 3 (Reversible Uncompute), garbage is restored to 0 and energy cost is 0.0
    phase3 = pipeline_states[3]
    assert phase3["phase"] == "3. Reversible Uncompute"
    assert phase3["regs"]["garbage_G"] == 0
    assert phase3["regs"]["copy_Y"] == 0  # NOT 1 = 0
    assert phase3["landauer_energy"] == 0.0

    # Check that comparative irreversible phase 4 shows positive energy cost equal to Landauer limit
    phase4 = pipeline_states[4]
    assert phase4["phase"] == "4. Irreversible Overwrite (Destructive)"
    assert phase4["landauer_energy"] == expected_limit

    # Adiabatic dynamic scaling math verification
    # E_adi = (R * C / T_ramp) * C * V^2
    # E_conv = 0.5 * C * V^2
    r = 1000.0
    c = 1e-12
    v = 2.0
    t_ramp = 10 * r * c

    e_adi, e_conv = sim.simulate_adiabatic_dissipation(r, c, v, t_ramp)
    expected_conv = 0.5 * c * (v**2)
    expected_adi = (r * c / t_ramp) * c * (v**2)

    assert math.isclose(e_conv, expected_conv)
    assert math.isclose(e_adi, expected_adi)
    assert math.isclose(e_adi, 0.2 * expected_conv)  # 5x energy reduction relative to conventional limits because T_ramp = 10 * RC
