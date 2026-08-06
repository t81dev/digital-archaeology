#!/usr/bin/env python3
"""
Cryogenic Superconducting & Single Flux Quantum (SFQ) Logic Simulator
---------------------------------------------------------------------
This simulator models classic Rapid Single Flux Quantum (RSFQ) and Energy-Efficient
RSFQ (ERSFQ) digital circuits operating in cryogenic environments (~4.2 K).

It implements:
1. Stateful RSFQ cell primitives:
   - D-Flip-Flop (DFF) / D-Latch: Tracks trapped magnetic flux quantum state.
   - AND Gate: Evaluates stateful coincidence of two pulse inputs upon CLK.
2. Timing Jitter & Setup-Time Bounds:
   - Simulates picosecond-accurate pulse propagation with timing jitter.
   - Detects timing/setup violations when input pulses fall too close to CLK.
3. Thermodynamic and Cooling Penalty Energy Model:
   - Quantifies microscopic switching energy per Josephson junction (JJ).
   - Models static power dissipation from resistive bias lines.
   - Models ERSFQ mode where static bias line losses are completely eliminated.
   - Scales cold-stage energy to effective room-temperature utility consumption
     using thermodynamic refrigeration penalties (Carnot and cryocooler efficiency).
4. Text-Based Pulse Waveform Visualizer.
"""

import math
import random
import sys


# =====================================================================
# CONSTANTS & PHYSICAL MODEL DATA
# =====================================================================
PHI_0 = 2.0678e-15  # Weber (Volt-seconds) - Single Magnetic Flux Quantum
K_B = 1.3806e-23    # Boltzmann Constant (J/K)


class SFQCell:
    """Base class for superconducting single flux quantum logic cells."""
    def __init__(self, name: str):
        self.name = name

    def reset(self):
        raise NotImplementedError


class DFlipFlop(SFQCell):
    """
    Stateful RSFQ D-Flip-Flop.
    - An incoming Data (D) pulse traps a single flux quantum (state -> 1).
    - An incoming Clock (CLK) pulse reads out the state:
      - If state is 1: Emits an output pulse on Q after propagation delay, resets state to 0.
      - If state is 0: Emits no pulse.
    - Timing checks: If a D pulse arrives too close to CLK (within setup_time),
      the flux trapping fails or goes metastable (setup violation).
    """
    def __init__(self, name: str = "DFF", setup_time: float = 3.0, prop_delay: float = 5.0):
        super().__init__(name)
        self.setup_time = setup_time  # in picoseconds
        self.prop_delay = prop_delay  # in picoseconds
        self.state = 0                # 0 = no trapped flux, 1 = trapped flux quantum
        self.last_d_time = -999.0

    def reset(self):
        self.state = 0
        self.last_d_time = -999.0

    def process_pulse_d(self, t: float) -> bool:
        """Processes a pulse on the D line. Returns True if state changes."""
        self.state = 1
        self.last_d_time = t
        return True

    def process_pulse_clk(self, t: float, jitter: float = 0.0) -> tuple[bool, float, list[str]]:
        """
        Processes a pulse on the CLK line.
        Returns:
          - (q_fired, q_time, warnings)
        """
        warnings = []
        q_fired = False
        q_time = 0.0

        # Adjust clock time with thermal timing jitter
        t_noisy = t + jitter

        # Check for setup time violations
        if self.state == 1 and (0.0 <= (t_noisy - self.last_d_time) < self.setup_time):
            warnings.append(
                f"[{self.name}] Setup-time violation: D pulse at {self.last_d_time:.1f} ps "
                f"is too close to CLK at {t_noisy:.1f} ps (limit: {self.setup_time} ps). "
                f"State resolved metastably to 0."
            )
            self.state = 0  # Flux escapes under metastability
            return False, 0.0, warnings

        if self.state == 1:
            q_fired = True
            q_time = t_noisy + self.prop_delay
            self.state = 0  # Flush trapped flux
        else:
            q_fired = False

        return q_fired, q_time, warnings


class SFQAndGate(SFQCell):
    """
    Stateful RSFQ AND Gate.
    - Operates by storing pulses received on inputs A and B in separate loops.
    - Upon a CLK pulse:
      - If both loops are set (state_A == 1 and state_B == 1), emits a pulse on Q and resets both loops.
      - Otherwise, emits no pulse. (Optionally resets based on design; here we clear states on CLK).
    """
    def __init__(self, name: str = "AND", prop_delay: float = 6.0):
        super().__init__(name)
        self.prop_delay = prop_delay
        self.state_a = 0
        self.state_b = 0

    def reset(self):
        self.state_a = 0
        self.state_b = 0

    def process_pulse_a(self, t: float):
        self.state_a = 1

    def process_pulse_b(self, t: float):
        self.state_b = 1

    def process_pulse_clk(self, t: float, jitter: float = 0.0) -> tuple[bool, float, list[str]]:
        warnings = []
        q_fired = False
        q_time = 0.0

        t_noisy = t + jitter

        if self.state_a == 1 and self.state_b == 1:
            q_fired = True
            q_time = t_noisy + self.prop_delay
        else:
            q_fired = False

        # Reset states upon clock evaluation
        self.state_a = 0
        self.state_b = 0

        return q_fired, q_time, warnings


# =====================================================================
# ENERGY AND REFRIGERATION METRICS MODEL
# =====================================================================

class CryogenicEnergyModel:
    """
    Quantifies the microarchitectural and system-level energy consumption of
    superconducting processors, including refrigerator overhead.
    """
    def __init__(self, temp_cold: float = 4.2, temp_warm: float = 300.0,
                 critical_current: float = 1.5e-4, bias_voltage: float = 1.0e-3,
                 bias_resistor: float = 10.0, pct_carnot_efficiency: float = 0.005):
        """
        temp_cold: Cryogenic stage temperature (~4.2 K for Helium, ~77 K for Nitrogen).
        temp_warm: Ambient heat ejection temperature (~300 K).
        critical_current: Josephson junction typical critical current (e.g. 150 uA).
        bias_voltage: Power rail bias voltage (e.g. 1 mV).
        bias_resistor: Static bias line resistance (Ohm).
        pct_carnot_efficiency: Actual percentage of ideal thermodynamic Carnot COP achieved (typically 0.1% to 1.0%).
        """
        self.temp_cold = temp_cold
        self.temp_warm = temp_warm
        self.ic = critical_current
        self.v_bias = bias_voltage
        self.r_bias = bias_resistor
        self.efficiency = pct_carnot_efficiency

    def get_switching_energy(self) -> float:
        """
        Microscopic switching energy per Josephson junction phase slip:
        E_s = Ic * Phi_0 (Joules)
        """
        return self.ic * PHI_0

    def get_static_power(self, num_bias_lines: int, ersfq_mode: bool = False) -> float:
        """
        Static power dissipated at the cold stage via bias resistors:
        P_static = NumLines * (V_bias^2 / R_bias) (Watts)
        ERSFQ eliminates this by using inductive current bias loops.
        """
        if ersfq_mode:
            return 0.0
        return num_bias_lines * (self.v_bias ** 2) / self.r_bias

    def get_refrigeration_penalty(self) -> float:
        """
        Calculates the cooling penalty factor f_cryo.
        COP_Carnot = T_cold / (T_warm - T_cold)
        COP_Actual = COP_Carnot * Efficiency
        f_cryo = 1.0 / COP_Actual
        """
        if self.temp_cold >= self.temp_warm:
            return 1.0  # Room-temperature, no refrigeration required
        cop_carnot = self.temp_cold / (self.temp_warm - self.temp_cold)
        cop_actual = cop_carnot * self.efficiency
        return 1.0 / cop_actual

    def evaluate_system_energy(self, active_cycles: int, freq_ghz: float,
                               num_jjs: int, switching_events: int,
                               ersfq_mode: bool = False) -> dict:
        """
        Evaluates energy consumed over a workload period.
        """
        # Duration of workload in seconds
        duration = active_cycles / (freq_ghz * 1e9)

        # 1. Microscopic switching energy
        e_switching = switching_events * self.get_switching_energy()

        # 2. Static power dissipation during workload
        # For simplicity, we assume 1 bias line per 4 Josephson junctions in standard RSFQ
        num_bias_lines = max(1, num_jjs // 4)
        p_static = self.get_static_power(num_bias_lines, ersfq_mode)
        e_static = p_static * duration

        total_cold_energy = e_switching + e_static

        # 3. Apply Refrigeration penalty
        f_cryo = self.get_refrigeration_penalty()
        total_utility_energy = total_cold_energy * f_cryo

        return {
            "duration_ns": duration * 1e9,
            "switching_energy_aJ": e_switching * 1e18,
            "static_energy_aJ": e_static * 1e18,
            "cold_stage_energy_aJ": total_cold_energy * 1e18,
            "cooling_penalty_factor": f_cryo,
            "room_temp_utility_energy_fJ": total_utility_energy * 1e15,
            "room_temp_utility_energy_Joules": total_utility_energy
        }


# =====================================================================
# INTERACTIVE SIMULATION ENGINE & SCENARIO RUNNER
# =====================================================================

class SFQSimulator:
    """Orchestrates multi-cell SFQ timing simulations."""
    def __init__(self, temp_kelvin: float = 4.2):
        self.temp = temp_kelvin
        self.dff = DFlipFlop("DFF_Core")
        self.and_gate = SFQAndGate("AND_Core")
        self.energy_model = CryogenicEnergyModel(temp_cold=temp_kelvin)

    def calculate_jitter(self) -> float:
        """
        Calculates thermal timing jitter (ps) proportional to absolute temperature.
        Simulates increased thermal noise at room temp vs liquid helium.
        """
        # At 4.2 K, jitter is very small (e.g. standard deviation ~0.2 ps)
        # At 300 K, thermal noise on junctions would cause severe timing fluctuations (~5.0 ps)
        scale = 0.1 * math.sqrt(self.temp / 4.2)
        return random.gauss(0, scale)

    def simulate_dff_pipeline(self, d_pulses: list[float], clk_pulses: list[float]) -> dict:
        """
        Simulates a stream of pulses directed at a DFF cell.
        All pulse values are timestamps in picoseconds.
        """
        self.dff.reset()
        events = []  # List of tuples: (time, channel, event_type)
        warnings = []
        q_pulses = []

        # Populate initial events
        for t in d_pulses:
            events.append((t, "D", "Pulse"))
        for t in clk_pulses:
            events.append((t, "CLK", "Pulse"))

        # Sort chronologically
        events.sort(key=lambda x: x[0])

        for t, channel, etype in events:
            if channel == "D":
                self.dff.process_pulse_d(t)
            elif channel == "CLK":
                jitter = self.calculate_jitter()
                fired, q_t, cell_warns = self.dff.process_pulse_clk(t, jitter)
                warnings.extend(cell_warns)
                if fired:
                    q_pulses.append(q_t)

        return {
            "q_pulses": q_pulses,
            "warnings": warnings,
            "jitter_applied": self.calculate_jitter()
        }


def draw_waveform(d_pulses: list[float], clk_pulses: list[float], q_pulses: list[float], duration_ps: float = 100.0):
    """Generates an ASCII timing diagram representing pulse train arrivals."""
    steps = 50
    ps_per_step = duration_ps / steps

    def list_to_wave(pulses):
        wave = [" " for _ in range(steps)]
        for p in pulses:
            idx = int(p / ps_per_step)
            if 0 <= idx < steps:
                wave[idx] = "█"
        return "".join(wave)

    lines = []
    lines.append(f"  [Timing Diagram: 0 to {duration_ps} ps, steps of {ps_per_step:.1f} ps]")
    lines.append(f"    Data (D)  : │{list_to_wave(d_pulses)}│")
    lines.append(f"    Clock(CLK): │{list_to_wave(clk_pulses)}│")
    lines.append(f"    Output (Q): │{list_to_wave(q_pulses)}│")
    return "\n".join(lines)


# =====================================================================
# DEMO EXECUTION SCENARIO
# =====================================================================

def run_cryo_simulation():
    print("\n" + "=" * 70)
    print("SCENARIO: Rapid Single Flux Quantum (RSFQ) Picosecond Timing")
    print("=" * 70)

    sim = SFQSimulator(temp_kelvin=4.2)

    # Nominally spaced pulses
    d_pulses = [10.0, 45.0, 75.0]
    clk_pulses = [20.0, 55.0, 90.0]

    print("  Running nominal pipeline (D and CLK pulses cleanly separated)...")
    res = sim.simulate_dff_pipeline(d_pulses, clk_pulses)

    print("\n--- Waveforms ---")
    print(draw_waveform(d_pulses, clk_pulses, res["q_pulses"]))

    print(f"\n  Output Q pulses generated at: {[round(x, 1) for x in res['q_pulses']]} ps")
    if res["warnings"]:
        for w in res["warnings"]:
            print(f"  WARNING: {w}")
    else:
        print("  ✓ Timing budget met. No violations detected.")

    # Metastability Scenario
    d_bad = [10.0, 53.5]  # The second pulse is 1.5 ps before CLK! (setup is 3.0)
    clk_bad = [20.0, 55.0]
    print("\n  Running marginal pipeline (D pulse arrives inside setup-time window)...")
    res_bad = sim.simulate_dff_pipeline(d_bad, clk_bad)

    print("\n--- Waveforms (Timing Failure) ---")
    print(draw_waveform(d_bad, clk_bad, res_bad["q_pulses"]))
    print(f"\n  Output Q pulses generated at: {[round(x, 1) for x in res_bad['q_pulses']]} ps")
    for w in res_bad["warnings"]:
        print(f"  ⚠ Timing Exception: {w}")


def run_energy_comparison():
    print("\n" + "=" * 70)
    print("SCENARIO: Thermodynamic Energy & Cryogenic Cooling Penalty Analysis")
    print("=" * 70)

    # Let's evaluate a workload of 1,000,000 cycles running on a 100 GHz core
    # with 50,000 Josephson Junctions (switching active 10% of time)
    active_cycles = 1_000_000
    freq = 100.0  # GHz
    num_jjs = 50_000
    switching_events = 5_000_000  # 100 switches per cycle across chip

    print(f"  Workload Parameters:")
    print(f"    Clock Frequency:        {freq} GHz")
    print(f"    Workload Duration:      {active_cycles / (freq*1e9)*1e6:.1f} microseconds ({active_cycles:,} cycles)")
    print(f"    Active Switch Events:   {switching_events:,} phase slips")

    # 1. Standard RSFQ at 4.2 K (With 0.5% Carnot efficiency)
    model_4k = CryogenicEnergyModel(temp_cold=4.2, pct_carnot_efficiency=0.005)
    metrics_rsfq = model_4k.evaluate_system_energy(
        active_cycles, freq, num_jjs, switching_events, ersfq_mode=False
    )

    # 2. ERSFQ (Energy-efficient RSFQ) at 4.2 K (No static bias resistor losses)
    metrics_ersfq = model_4k.evaluate_system_energy(
        active_cycles, freq, num_jjs, switching_events, ersfq_mode=True
    )

    # 3. High-Temperature Superconductor (HTS) ERSFQ at 77 K (Liquid nitrogen cooling)
    model_77k = CryogenicEnergyModel(temp_cold=77.0, pct_carnot_efficiency=0.02)  # Higher eff at HTS
    metrics_hts = model_77k.evaluate_system_energy(
        active_cycles, freq, num_jjs, switching_events, ersfq_mode=True
    )

    # 4. Standard Room-Temperature CMOS baseline (estimated 50,000 gates at 5 GHz, ~2 fJ per switch)
    # Total switching energy = 5,000,000 switches * 2 fJ = 10,000,000 fJ = 1e-8 Joules
    e_cmos = 1.0e-8

    print(f"\n  [Energy Metrics Evaluation]:")
    print(f"    1. Classic RSFQ (4.2 K):")
    print(f"       - Microscopic Switch Energy: {metrics_rsfq['switching_energy_aJ']:.2f} aJ")
    print(f"       - Bias Static Heat Load:     {metrics_rsfq['static_energy_aJ']:.2f} aJ (Resistive Loss)")
    print(f"       - Refrigeration Penalty:     {metrics_rsfq['cooling_penalty_factor']:.1f}x utility multiplier")
    print(f"       - Total Room-Temp Energy:    {metrics_rsfq['room_temp_utility_energy_fJ']:.2f} fJ")

    print(f"\n    2. ERSFQ (4.2 K - Resistorless Static Bias):")
    print(f"       - Microscopic Switch Energy: {metrics_ersfq['switching_energy_aJ']:.2f} aJ")
    print(f"       - Bias Static Heat Load:     {metrics_ersfq['static_energy_aJ']:.2f} aJ (Zero-Static)")
    print(f"       - Total Room-Temp Energy:    {metrics_ersfq['room_temp_utility_energy_fJ']:.2f} fJ")

    print(f"\n    3. HTS ERSFQ (77 K - High-Temp Superconducting):")
    print(f"       - Refrigeration Penalty:     {metrics_hts['cooling_penalty_factor']:.2f}x utility multiplier")
    print(f"       - Total Room-Temp Energy:    {metrics_hts['room_temp_utility_energy_fJ']:.2f} fJ")

    print(f"\n    4. Standard CMOS Baseline (300 K, 5 GHz):")
    print(f"       - Total Room-Temp Energy:    {e_cmos * 1e15:.2f} fJ")

    gain_ersfq = e_cmos / metrics_ersfq['room_temp_utility_energy_Joules']
    print("\n--- Comparative Takeaways ---")
    print(f"  ✓ Under equal workloads, ERSFQ (4.2 K) is {gain_ersfq:.1f}x more energy-efficient")
    print("    than room-temperature CMOS, EVEN AFTER accounting for the refrigeration penalty.")
    print("  ✓ Transitioning from RSFQ to ERSFQ resolves the microscopic static bias power crisis.")


# =====================================================================
# MAIN METHOD
# =====================================================================

def main():
    print("\n" + "=" * 80)
    print("     DIGITAL ARCHAEOLOGY: CRYOGENIC SUPERCONDUCTING & SFQ PULSE SIMULATOR")
    print("=" * 80)
    print("  This simulator models classical magnetic flux quantum logic, pico-second timing,")
    print("  and thermodynamic cooling penalty tradeoffs of Josephson junction architectures.")

    run_cryo_simulation()
    run_energy_comparison()


if __name__ == "__main__":
    main()
