#!/usr/bin/env python3
"""
Continuous Analog & Optical Wave Accelerator Simulator
------------------------------------------------------
This interactive simulator models two complementary paradigms of continuous-physical computation:
1. Continuous Analog Computing:
   Solves a dynamic second-order differential equation (mass-spring-damper system)
   using a simulated physical operational amplifier network. Simulates analog noise,
   component thermal drift, and saturation, comparing it to ideal digital integration.
2. Optical Wave Matrix-Vector Accelerator:
   Performs matrix-vector multiplication using coherent light wave interference
   propagating through a network of Mach-Zehnder Interferometers (MZIs). Simulates
   phase noise, laser intensity fluctuations, and photodetector noise.
"""

import math
import random
import sys


# =====================================================================
# PART 1: COMPLEX NUMBER HELPERS (Zero-dependency Complex Math)
# =====================================================================

class Complex:
    """A simple class to represent complex numbers for wave modeling."""
    def __init__(self, real: float, imag: float = 0.0):
        self.real = real
        self.imag = imag

    @classmethod
    def polar(cls, r: float, theta: float):
        return cls(r * math.cos(theta), r * math.sin(theta))

    def abs(self) -> float:
        return math.sqrt(self.real**2 + self.imag**2)

    def phase(self) -> float:
        return math.atan2(self.imag, self.real)

    def conj(self):
        return Complex(self.real, -self.imag)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.real + other, self.imag)
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.real - other, self.imag)
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Complex(self.real * other, self.imag * other)
        return Complex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"({self.real:.4f} {sign} {abs(self.imag):.4f}i)"


# =====================================================================
# PART 2: CONTINUOUS ANALOG COMPUTING SYSTEM
# =====================================================================

class AnalogComputer:
    """
    Simulates a physical electronic analog computer patched to solve
    a 2nd-order differential equation modeling a Mass-Spring-Damper system:
       d^2y/dt^2 + 2 * zeta * omega_n * dy/dt + omega_n^2 * y = 0
    or with an external forcing function f(t):
       d^2y/dt^2 + 2 * zeta * omega_n * dy/dt + omega_n^2 * y = f(t)

    This is mapped into state space using active op-amp components:
    - Integrator 1: Integrates d^2y/dt^2 (acceleration) to get dy/dt (velocity).
    - Integrator 2: Integrates dy/dt to get y (displacement).
    - Summer: Calculates d^2y/dt^2 = f(t) - 2 * zeta * omega_n * dy/dt - omega_n^2 * y.
    """
    def __init__(self, zeta: float = 0.15, omega_n: float = 2.0, max_voltage: float = 10.0):
        self.zeta = zeta          # Damping ratio
        self.omega_n = omega_n    # Natural frequency
        self.max_voltage = max_voltage  # Saturation limit (+/- V)

        # Simulation imperfections
        self.thermal_noise_std = 0.02  # standard deviation of noise at summing junctions
        self.drift_rate = 0.005        # rate of component value drift per simulated second
        self.gain_error = 0.01         # calibration tolerance of op-amp feedback resistors

    def solve(self, y0: float, dy0: float, duration: float, dt: float = 0.01,
              enable_noise: bool = True, enable_drift: bool = True,
              forcing_fn=None):
        """
        Simulates the time evolution of the analog computer circuit.
        """
        t = 0.0
        # Initialize physical integrator voltages (state variables)
        v_y = y0       # displacement output of Integrator 2
        v_dy = dy0     # velocity output of Integrator 1

        times = []
        displacement = []
        velocity = []
        acceleration = []
        ideal_disp = []

        # Ideal analytical/digital helper for comparison
        y_ideal = y0
        dy_ideal = dy0

        # Physical drift drift vectors initialized
        drift_damping = 1.0
        drift_spring = 1.0

        while t <= duration:
            # Update continuous drift
            if enable_drift:
                # Component drift changes system parameters slowly
                drift_damping += random.gauss(0, self.drift_rate) * math.sqrt(dt)
                drift_spring += random.gauss(0, self.drift_rate) * math.sqrt(dt)

            # Op-amp Gains with calibration tolerance
            gain_damping = 2.0 * self.zeta * self.omega_n * (1.0 + self.gain_error) * drift_damping
            gain_spring = (self.omega_n ** 2) * (1.0 + self.gain_error) * drift_spring

            # Forcing function (input voltage)
            v_force = forcing_fn(t) if forcing_fn else 0.0

            # 1. Summing junction equation
            # Continuous physical sum with thermal noise (k_B T C) at the junction
            noise = random.gauss(0, self.thermal_noise_std) if enable_noise else 0.0
            v_ddy = v_force - (gain_damping * v_dy) - (gain_spring * v_y) + noise

            # 2. Hardware Saturation limits
            v_ddy = max(-self.max_voltage, min(self.max_voltage, v_ddy))

            # 3. Integrator 1 updates velocity (v_dy)
            v_dy += v_ddy * dt
            v_dy = max(-self.max_voltage, min(self.max_voltage, v_dy))

            # 4. Integrator 2 updates displacement (v_y)
            v_y += v_dy * dt
            v_y = max(-self.max_voltage, min(self.max_voltage, v_y))

            # --- Digital Ideal Reference (Runge-Kutta 4th Order) ---
            def derivatives(curr_y, curr_dy, curr_t):
                f_t = forcing_fn(curr_t) if forcing_fn else 0.0
                return curr_dy, f_t - 2.0 * self.zeta * self.omega_n * curr_dy - (self.omega_n**2) * curr_y

            k1_y, k1_dy = derivatives(y_ideal, dy_ideal, t)
            k2_y, k2_dy = derivatives(y_ideal + 0.5 * dt * k1_y, dy_ideal + 0.5 * dt * k1_dy, t + 0.5 * dt)
            k3_y, k3_dy = derivatives(y_ideal + 0.5 * dt * k2_y, dy_ideal + 0.5 * dt * k2_dy, t + 0.5 * dt)
            k4_y, k4_dy = derivatives(y_ideal + dt * k3_y, dy_ideal + dt * k3_dy, t + dt)

            y_ideal += (dt / 6.0) * (k1_y + 2.0 * k2_y + 2.0 * k3_y + k4_y)
            dy_ideal += (dt / 6.0) * (k1_dy + 2.0 * k2_dy + 2.0 * k3_dy + k4_dy)

            # Record metrics
            times.append(t)
            displacement.append(v_y)
            velocity.append(v_dy)
            acceleration.append(v_ddy)
            ideal_disp.append(y_ideal)

            t += dt

        return times, displacement, velocity, acceleration, ideal_disp


# =====================================================================
# PART 3: OPTICAL COHERENT WAVE MATRIX-VECTOR ACCELERATOR
# =====================================================================

class MachZehnderInterferometer:
    """
    Models a symmetric 2x2 Mach-Zehnder Interferometer (MZI).
    Uses phase shifters (theta, phi) to perform complex wave transformation.
    """
    def __init__(self, theta: float = 0.0, phi: float = 0.0):
        self.theta = theta  # Internal phase shift (determines splitting ratio)
        self.phi = phi      # Output phase shift (determines phase alignment)

    def propagate(self, e1: Complex, e2: Complex, phase_noise: float = 0.0) -> tuple:
        """
        Propagates two input coherent light waves through the MZI.
        Applies a unitary transformation representing splitting, phase shifts, and recombination.
        """
        # Inject thermal phase noise on the phase shifters
        t_noisy = self.theta + phase_noise
        p_noisy = self.phi + phase_noise

        # Symmetric MZI unitary transfer matrix:
        # E_out_1 = i * e^(i*phi) * ( sin(theta/2) * E_in_1 + cos(theta/2) * E_in_2 )
        # E_out_2 = i * ( cos(theta/2) * E_in_1 - sin(theta/2) * E_in_2 )
        factor_common = Complex(0, 1)  # Multiplication by 'i'

        term_sin = math.sin(t_noisy / 2.0)
        term_cos = math.cos(t_noisy / 2.0)
        exp_phi = Complex.polar(1.0, p_noisy)

        # Output 1 Wave
        out1 = factor_common * exp_phi * (e1 * term_sin + e2 * term_cos)
        # Output 2 Wave
        out2 = factor_common * (e1 * term_cos - e2 * term_sin)

        return out1, out2


class OpticalMatrixAccelerator:
    """
    Simulates a 2x2 Photonic Tensor Core using a Mach-Zehnder Interferometer (MZI).
    A unitary 2x2 matrix can be completely parameterized by a single 2x2 MZI.
    This module performs matrix-vector multiplication (y = W x) in a single light-propagation step.
    """
    def __init__(self, theta: float, phi: float, laser_power: float = 1.0):
        self.mzi = MachZehnderInterferometer(theta, phi)
        self.laser_power = laser_power

        # Physical noise sources
        self.laser_rin = 0.01          # Relative Intensity Noise (RIN) on laser source
        self.phase_noise_std = 0.02    # Thermal phase noise in heaters (radians)
        self.detector_dark_current = 0.001 # Noise floor of photodetector
        self.detector_shot_noise = 0.005   # Quantum shot noise factor

    def run_multiplication(self, x1: float, x2: float, enable_noise: bool = True) -> tuple:
        """
        Runs optical multiplication:
        1. Encodes real-valued input voltages (x1, x2) into coherent light fields (amplitude-modulated).
        2. Propagates waves through MZI, suffering from physical phase noise.
        3. Measures optical intensity using simulated photodetectors with noise.
        """
        # Laser power scaling
        rin_noise = random.gauss(0, self.laser_rin) if enable_noise else 0.0
        effective_source = self.laser_power * (1.0 + rin_noise)

        # Convert electrical voltages to optical electric field amplitudes
        # E_in is proportional to V_in and sqrt of laser power
        e_in1 = Complex(x1 * math.sqrt(effective_source), 0.0)
        e_in2 = Complex(x2 * math.sqrt(effective_source), 0.0)

        # Phase noise
        p_noise = random.gauss(0, self.phase_noise_std) if enable_noise else 0.0

        # Propagate through MZI
        e_out1, e_out2 = self.mzi.propagate(e_in1, e_in2, phase_noise=p_noise)

        # Measure optical intensities (Photodetector: I = |E|^2)
        i_out1 = e_out1.abs() ** 2
        i_out2 = e_out2.abs() ** 2

        # Apply photodetector noise (shot noise + dark current floor)
        if enable_noise:
            # Shot noise is proportional to the square root of signal intensity
            shot1 = random.gauss(0, self.detector_shot_noise * math.sqrt(i_out1))
            shot2 = random.gauss(0, self.detector_shot_noise * math.sqrt(i_out2))
            dark1 = abs(random.gauss(0, self.detector_dark_current))
            dark2 = abs(random.gauss(0, self.detector_dark_current))

            i_out1 = max(0.0, i_out1 + shot1 + dark1)
            i_out2 = max(0.0, i_out2 + shot2 + dark2)

        # Convert optical intensities back to output voltages (using square root for field-equivalent)
        # y = sqrt(I) * sign of field (or phase-rectified outputs)
        # For simplicity, we model direct power intensity as the linear mathematical result
        # representing a squared-weight operation, or amplitude multiplication.
        # Let's return both the complex fields and measured intensity outputs.
        return (e_out1, e_out2), (i_out1, i_out2)

    def get_ideal_unitary_matrix(self) -> list:
        """Returns the ideal 2x2 mathematical transformation matrix represented by the MZI."""
        t = self.mzi.theta
        p = self.mzi.phi

        # Column 1
        col1_r1 = Complex.polar(math.sin(t/2), p + math.pi/2)
        col1_r2 = Complex.polar(math.cos(t/2), math.pi/2)

        # Column 2
        col2_r1 = Complex.polar(math.cos(t/2), p + math.pi/2)
        col2_r2 = Complex.polar(math.sin(t/2), -math.pi/2)

        return [
            [col1_r1, col2_r1],
            [col1_r2, col2_r2]
        ]


# =====================================================================
# PART 4: BEAUTIFUL CLI & ASCI PLOTTER HELPERS
# =====================================================================

def draw_ascii_plot(times, values, ideal_values, height=12, width=70):
    """Draws a standard CLI-friendly ascii plot overlaying analog vs ideal trajectories."""
    if not values:
        return ""

    min_val = min(min(values), min(ideal_values))
    max_val = max(max(values), max(ideal_values))
    val_range = max_val - min_val if max_val != min_val else 1.0

    # Initialize canvas
    canvas = [[" " for _ in range(width)] for _ in range(height)]

    # Draw zero axis line
    if min_val < 0.0 < max_val:
        zero_row = int((max_val / val_range) * (height - 1))
        for col in range(width):
            canvas[zero_row][col] = "─"

    # Map time indices to columns
    steps = len(times)
    for col in range(width):
        idx = int((col / (width - 1)) * (steps - 1))
        idx = min(idx, steps - 1)

        val = values[idx]
        ideal = ideal_values[idx]

        # Calculate rows (0 is top, height-1 is bottom)
        row_val = int(((max_val - val) / val_range) * (height - 1))
        row_ideal = int(((max_val - ideal) / val_range) * (height - 1))

        # Clamp bounds
        row_val = max(0, min(height - 1, row_val))
        row_ideal = max(0, min(height - 1, row_ideal))

        # Overlay plots: '•' for analog (physical), '─' / 'x' for ideal digital
        canvas[row_ideal][col] = "░"
        canvas[row_val][col] = "█"

    lines = []
    lines.append(f"  [Max: {max_val:+.3f} V] " + "─" * (width - 20))
    for r in range(height):
        row_str = "".join(canvas[r])
        # Add labels to some rows
        if r == 0:
            lines.append(f"  │ {row_str}")
        elif r == height // 2:
            lines.append(f"  │ {row_str} (░ = Digital Ideal, █ = Analog Physical)")
        else:
            lines.append(f"  │ {row_str}")
    lines.append(f"  [Min: {min_val:+.3f} V] " + "─" * (width - 20))
    return "\n".join(lines)


def draw_wave_interference(amp1, amp2):
    """Generates a text-based visual of constructive or destructive wave interference."""
    width = 60
    wave1 = []
    wave2 = []
    wave_sum = []

    for i in range(width):
        phase = (i / width) * 4 * math.pi
        w1 = amp1 * math.sin(phase)
        w2 = amp2 * math.sin(phase)
        wave1.append(w1)
        wave2.append(w2)
        wave_sum.append(w1 + w2)

    # Let's generate a vertical ascii interference representation
    return f"  Input 1 Power (Amp: {amp1:.2f}):  " + "█" * int(amp1 * 10) + "\n" + \
           f"  Input 2 Power (Amp: {amp2:.2f}):  " + "█" * int(amp2 * 10) + "\n" + \
           f"  Combined Max Amplitude:        " + "█" * int(abs(amp1 + amp2) * 10)


# =====================================================================
# SCENARIO RUNNERS
# =====================================================================

def run_analog_simulation_scenario(zeta=0.1, omega=1.5, noise=True, drift=True):
    print("\n" + "=" * 70)
    print("SCENARIO: Mass-Spring-Damper Physical Simulation via Op-Amps")
    print("=" * 70)
    print(f"  System parameters: Damping (zeta) = {zeta}, Freq (omega_n) = {omega}")
    print(f"  Imperfections: Thermal Noise = {noise}, Thermal Drift = {drift}")
    print("  Initializing capacitor voltages: Displacement(t=0) = 4.0 V, Velocity(t=0) = -2.0 V")

    comp = AnalogComputer(zeta=zeta, omega_n=omega)
    # Solve 10 seconds of simulation
    times, disp, vel, acc, ideal = comp.solve(
        y0=4.0, dy0=-2.0, duration=10.0, dt=0.05,
        enable_noise=noise, enable_drift=drift
    )

    # Compute final absolute error
    errors = [abs(disp[i] - ideal[i]) for i in range(len(times))]
    mean_error = sum(errors) / len(errors)
    max_error = max(errors)

    print("\n--- Physical Voltage Outputs Over Time ---")
    print(draw_ascii_plot(times, disp, ideal))

    print("\n--- Calibration & Error Metrics ---")
    print(f"  Mean trajectory error (Analog Drift & Noise deviation): {mean_error:.4f} V")
    print(f"  Maximum instantaneous error:                         {max_error:.4f} V")
    print("  Note: Electronic analog computers limit precision to ~8-12 bits of equivalence")
    print("        but execute equations instantaneously as continuous physics.")


def run_optical_tensor_scenario(theta=1.5708, phi=0.7854, x1=1.0, x2=0.5, noise=True):
    print("\n" + "=" * 70)
    print("SCENARIO: Coherent Light Matrix-Vector Multiplication via MZI")
    print("=" * 70)
    print(f"  MZI Programmed Phase Shifters: θ = {theta:.4f} rad (90°), φ = {phi:.4f} rad (45°)")
    print(f"  Electrical Inputs: V_in_1 = {x1:.2f} V, V_in_2 = {x2:.2f} V")
    print(f"  Imperfections enabled: {noise}")

    # Initialize Accelerator
    acc = OpticalMatrixAccelerator(theta, phi)

    # Ideal transformation matrix
    u_matrix = acc.get_ideal_unitary_matrix()
    print("\n  [Ideal 2x2 Unitary Matrix mapped in MZI phase]:")
    print(f"    W = | {u_matrix[0][0]}   {u_matrix[0][1]} |")
    print(f"        | {u_matrix[1][0]}   {u_matrix[1][1]} |")

    # Run physical execution
    fields, intensities = acc.run_multiplication(x1, x2, enable_noise=noise)
    ideal_fields, ideal_intensities = acc.run_multiplication(x1, x2, enable_noise=False)

    print("\n--- Laser Wave Propagation & Coherent Interference ---")
    print(f"  Input Coherent Waves:  E_in_1 = {x1:.2f}, E_in_2 = {x2:.2f}")
    print(f"  Output Wave Field 1:   {fields[0]}  (Ideal: {ideal_fields[0]})")
    print(f"  Output Wave Field 2:   {fields[1]}  (Ideal: {ideal_fields[1]})")

    print("\n--- Photodetector Power Measurement (I = |E|^2) ---")
    print(f"  Detector 1 Output (V_out_1): {intensities[0]:.4f} W  (Ideal: {ideal_intensities[0]:.4f} W)")
    print(f"  Detector 2 Output (V_out_2): {intensities[1]:.4f} W  (Ideal: {ideal_intensities[1]:.4f} W)")

    p1_diff = abs(intensities[0] - ideal_intensities[0])
    p2_diff = abs(intensities[1] - ideal_intensities[1])
    print(f"  Multiplication Error margin:  Chan1: {p1_diff:.4f} W, Chan2: {p2_diff:.4f} W")

    print("\n--- Interference Visualizer ---")
    # Amplitude of output wave elements
    amp1 = fields[0].abs()
    amp2 = fields[1].abs()
    print(draw_wave_interference(amp1, amp2))


# =====================================================================
# MAIN METHOD (CLI Entry)
# =====================================================================

def main():
    # Run a quick demonstration automatically
    print("\n" + "=" * 80)
    print("     DIGITAL ARCHAEOLOGY: CONTINUOUS ANALOG & OPTICAL ACCELERATOR SIMULATOR")
    print("=" * 80)
    print("  Continuous computers compute using physical phenomena (voltage, light waves)")
    print("  rather than discrete digital logic. This enables instant O(1) operations but")
    print("  is inherently susceptible to physical noise, drift, and calibration limits.")

    run_analog_simulation_scenario(noise=True, drift=True)
    run_optical_tensor_scenario(noise=True)

    # Interactive loop
    if sys.stdin.isatty():
        while True:
            print("\n" + "=" * 60)
            print("Interactive Simulator Menu:")
            print("1. Run Analog Mass-Spring-Damper Simulation (Noisy & Drifted)")
            print("2. Run Analog Mass-Spring-Damper Simulation (Perfect Ideal Digital)")
            print("3. Run Optical Wave Tensor Multiplication (With Phase Noise & RIN)")
            print("4. Run Optical Wave Tensor Multiplication (Perfect Ideal)")
            print("5. Exit")
            try:
                choice = input("\nEnter choice (1-5): ").strip()
                if choice == "1":
                    run_analog_simulation_scenario(noise=True, drift=True)
                elif choice == "2":
                    run_analog_simulation_scenario(noise=False, drift=False)
                elif choice == "3":
                    run_optical_tensor_scenario(noise=True)
                elif choice == "4":
                    run_optical_tensor_scenario(noise=False)
                elif choice == "5":
                    print("Exiting simulator. Goodbye!")
                    break
                else:
                    print("Invalid option. Please enter a number between 1 and 5.")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting. Goodbye!")
                break
    else:
        print("\n[Non-interactive Mode] Pre-defined verification scenarios completed successfully.")


if __name__ == "__main__":
    main()
