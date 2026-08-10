"""
Student Solutions for the Digital Archaeology Lab Manual challenges.
Pre-filled with model solutions for out-of-the-box verification.
"""

import sys
import os

# Ensure the parent directories and subfolders are in import path so we can import relative simulators
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "mixed-radix-sim"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataflow-engine"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "capability-security"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "csp-messaging"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "analog-optical"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan9-9p"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "neuromorphic-spiking"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "stochastic-computing"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cryogenic-superconducting"))


# =====================================================================
# Lab Module 1 — Non-Binary Arithmetic & Signed Radix-3 Economy
# =====================================================================

def ternary_half_adder(a: int, b: int) -> tuple[int, int]:
    """
    Computes single trit sum and carry.
    Inputs: a, b in [-1, 0, 1]
    Returns: (sum, carry)
    """
    raw_sum = a + b
    if raw_sum == 2:
        return -1, 1   # Sum=-1, Carry=1  (-1*3^0 + 1*3^1 = 2)
    elif raw_sum == -2:
        return 1, -1   # Sum=1, Carry=-1  (1*3^0 + -1*3^1 = -2)
    elif raw_sum == 1:
        return 1, 0
    elif raw_sum == -1:
        return -1, 0
    else:
        return 0, 0


# =====================================================================
# Lab Module 2 — Out-of-Order Execution in Tagged-Token Dataflow
# =====================================================================

def run_custom_dataflow_graph(x: int, y: int, z: int) -> int:
    """
    Computes f(x, y, z) = (x + y) * (y - z) using the DataflowEngine.
    """
    from dataflow_sim import DataflowEngine, Node, Token

    engine = DataflowEngine()

    # Define Nodes
    engine.add_node(Node(node_id=1, op='ADD', destinations=[(3, 'left')]))  # x + y
    engine.add_node(Node(node_id=2, op='SUB', destinations=[(3, 'right')])) # y - z
    engine.add_node(Node(node_id=3, op='MUL', destinations=[(4, 'unconditional')]))
    engine.add_node(Node(node_id=4, op='OUTPUT'))

    # Inject inputs
    engine.inject_token(Token(value=x, dest_node=1, port='left'))
    engine.inject_token(Token(value=y, dest_node=1, port='right'))
    engine.inject_token(Token(value=y, dest_node=2, port='left'))
    engine.inject_token(Token(value=z, dest_node=2, port='right'))

    engine.run_until_empty()

    # Retrieve result from outputs map for Node 4
    if 4 in engine.outputs and engine.outputs[4]:
        return engine.outputs[4][0][0]
    return 0


# =====================================================================
# Lab Module 3 — Micro-Segmentation & Tagged Architectures
# =====================================================================

def run_secure_domain_transitions() -> tuple[bool, bool]:
    """
    Challenge 3A: Secure Domain Transitions & Bounds Confines.
    Writes inside bounds (success), triggers out-of-bounds bounds violation check.
    """
    from capability_sim import CPU, TaggedRAM, CapabilityWord, BoundsException

    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Set up restricted user capability [50, 60) in C1
    cpu.derive_cap(dest_idx=1, src_idx=0, offset=50, limit=10, perms={"R", "W"})

    # Try to write within bounds (Success)
    cpu.load_const(0, 42)
    cpu.store_data(src_data_idx=0, cap_idx=1, offset=5) # Address 55
    safe_ok = True

    # Try to write out of bounds (Fails)
    oob_caught = False
    try:
        cpu.store_data(src_data_idx=0, cap_idx=1, offset=15) # Out of bounds!
    except BoundsException:
        oob_caught = True

    return safe_ok, oob_caught


def run_lisp_machine_type_safety() -> tuple[int, bool, list]:
    """
    Challenge 3B: Lisp Machine Type-Safety & CDR-Coding.
    Performs type-safe lisp addition, checks Symbol mismatch failure, and traverses CDR packed list.
    """
    from capability_sim import CPU, TaggedRAM, LispWord, TagException

    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # 1. Set up Fixnum and Symbol words
    cpu.data_regs[0] = LispWord("Fixnum", 42)
    cpu.data_regs[1] = LispWord("Fixnum", 58)
    cpu.data_regs[2] = LispWord("Symbol", "MAPPED_TOKEN")

    # Perform type-safe addition
    cpu.lisp_add(dest_idx=3, src1_idx=0, src2_idx=1)
    added_val = cpu.data_regs[3].value # 100

    # 2. Attempt addition with a Symbol (Mismatched type tag)
    tag_violation_caught = False
    try:
        cpu.lisp_add(dest_idx=3, src1_idx=0, src2_idx=2)
    except TagException:
        tag_violation_caught = True

    # 3. Simulate CDR-coded list traversal: List = (100, 200, 300)
    ram.write(30, LispWord("Fixnum", 100, cdr_code="CDR-NEXT"))
    ram.write(31, LispWord("Fixnum", 200, cdr_code="CDR-NEXT"))
    ram.write(32, LispWord("Fixnum", 300, cdr_code="CDR-NIL"))

    # Traverse using C0 Master Cap starting at address 30
    traversed_vals = cpu.lisp_cdr_next_traverse(cap_idx=0, start_offset=30)

    return added_val, tag_violation_caught, traversed_vals


def run_burroughs_descriptors() -> tuple[bool, int, bool]:
    """
    Challenge 3C: Burroughs Descriptor Page Faults & Virtual Memory.
    Simulates Page Fault (DescriptorNotPresentException), OS Page-In, post-page-in Read, and Bounds Exception.
    """
    from capability_sim import CPU, TaggedRAM, DataWord, DescriptorWord, DescriptorNotPresentException, BoundsException

    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Write database table in memory at [40, 45)
    ram.write(40, DataWord(101))
    ram.write(41, DataWord(202))
    ram.write(42, DataWord(303))

    # 1. Setup a swapped-out descriptor (is_present = False) in D0
    swapped_desc = DescriptorWord(base=40, limit=3, is_present=False, read_only=False, label="DBTable")
    cpu.data_regs[0] = swapped_desc

    # 2. Attempt read - Should Page Fault!
    page_fault_caught = False
    try:
        cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=1)
    except DescriptorNotPresentException:
        page_fault_caught = True
        cpu.page_in_descriptor(desc_reg_idx=0)

    # 3. Retry access after page-in (Success!)
    cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=1)
    val_loaded = cpu.data_regs[1] # Should be 202

    # 4. Enforce descriptor bounds check
    bounds_caught = False
    try:
        cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=3)
    except BoundsException:
        bounds_caught = True

    return page_fault_caught, val_loaded, bounds_caught


# =====================================================================
# Lab Module 4 — Cooperative Rendezvous & Deadlock Dynamics
# =====================================================================

def run_deadlock_avoiding_broker() -> list:
    """
    Grades Lab 4 message broker with alternative guard ALT multiplexing.
    """
    from csp_sim import CSPScheduler, Channel, alt_wait

    scheduler = CSPScheduler(verbose=False)
    chan_sensor = Channel("SensorChannel")
    chan_timer = Channel("TimerChannel")
    chan_out = Channel("OutLogger")

    output_logs = []

    def producer_proc(chan):
        yield chan.send("Temp=23.5C")
        yield chan.send("Temp=24.1C")

    def timer_proc(chan):
        yield chan.send("Tick_1s")
        yield chan.send("Tick_2s")

    def broker_proc(ch_a, ch_b, ch_out):
        for _ in range(4):
            selected, val = yield alt_wait(ch_a, ch_b)
            yield ch_out.send(f"Logged({selected.name}: {val})")

    def logger_proc(ch_in):
        for _ in range(4):
            val = yield ch_in.recv()
            output_logs.append(val)

    # Register scenarios
    scheduler.register("Producer", producer_proc, chan_sensor)
    scheduler.register("Timer", timer_proc, chan_timer)
    scheduler.register("Broker", broker_proc, chan_sensor, chan_timer, chan_out)
    scheduler.register("Logger", logger_proc, chan_out)

    scheduler.run()
    return output_logs


# =====================================================================
# Lab Module 5 — Reversible Logic, Landauer Limits, and Adiabatic Charge Recovery
# =====================================================================

def run_reversible_xor_lab(a: int, b: int) -> tuple[int, dict, float]:
    """
    Computes Y = A ^ B reversibly using uncomputation.
    Returns: (output_copy, register_states, landauer_energy)
    """
    from analog_optical_sim import ReversibleSimulator

    sim = ReversibleSimulator(temp_kelvin=300.0)

    # Initial state
    regs = {"A": a, "B": b, "garbage_G0": 0, "copy_C0": 0}
    landauer_energy = 0.0

    # 1. Compute Phase: G0 = A ^ B using reversible CNOT logic
    _, g0 = sim.gate_cnot(a, b)
    regs["garbage_G0"] = g0

    # 2. Copy Phase: Copy G0 to output register C0 via CNOT
    _, copy_c0 = sim.gate_cnot(g0, regs["copy_C0"])
    regs["copy_C0"] = copy_c0

    # 3. Uncompute Phase: Run inverse of Compute Phase to restore G0 to 0
    # The inverse of CNOT is itself. We run CNOT on (A, B) again to deallocate G0
    _, restored_g0 = sim.gate_cnot(a, b)
    regs["garbage_G0"] = restored_g0 ^ g0 # Reversible restoration logic

    return regs["copy_C0"], regs, landauer_energy


# =====================================================================
# Lab Module 6 — Distributed Namespaces & 9P Protocol Messages
# =====================================================================

def run_ninep_union_mount() -> str:
    """
    Challenge Lab 6: Multi-Device Union Mount & Fallback Routing.
    Union binds a backup dev directory after primary dev directory. Returns resolved fallback content.
    """
    from namespace_sim import Namespace, NinePSession, T_VERSION, T_ATTACH, T_WALK, T_OPEN, T_READ, T_WRITE, FileNode

    ns = Namespace()
    session = NinePSession(ns)

    # Negotiate version & attach root fid
    session.handle_message({"type": T_VERSION, "tag": 1, "version": "9P2000"})
    session.handle_message({"type": T_ATTACH, "tag": 2, "fid": 1})

    # Create primary sensor folder and empty file
    session.handle_message({"type": T_WALK, "tag": 3, "fid": 1, "newfid": 2, "wnames": ["dev"]})
    session.handle_message({"type": T_WRITE, "tag": 4, "fid": 2, "offset": 0, "data": ""})

    # Create backup directory and backup sensor file
    ns.bind("/dev", "/backup_dev")
    backup_sensor = ns._resolve_path("/backup_dev")
    sensor_backup_file = FileNode("sensor", content="BackupData_72F")
    backup_sensor.add_child(sensor_backup_file)

    # Perform Union Bind: Union mount /backup_dev AFTER /dev
    ns.bind("/backup_dev", "/dev", flags="union_after")

    # Walk from root fid 1 to /dev/sensor
    session.handle_message({"type": T_WALK, "tag": 5, "fid": 1, "newfid": 3, "wnames": ["dev", "sensor"]})

    # Read data - falls through to backup sensor's content via union search fallback
    resp_read = session.handle_message({"type": T_READ, "tag": 6, "fid": 3, "offset": 0, "count": 1024})

    return resp_read['data']


# =====================================================================
# Lab Module 7 — Stochastic Computing and Spiking Neuromorphic Co-processors
# =====================================================================

def run_spiking_neuron() -> tuple[list, list]:
    """
    Challenge 7A: Asynchronous Event-driven Spiking Integration.
    Steps a LIF neuron and tracks potential and spikes.
    """
    from spiking_sim import SpikingNeuron

    neuron = SpikingNeuron(neuron_id=1, v_rest=0.0, v_th=1.0, tau_m=10.0, v_reset=0.0, refractory_cycles=2)

    voltages = []
    spikes = []
    inputs = [0.2, 0.2, 0.4, 0.4, 0.0, 0.0, 0.0]

    for cycle, stim in enumerate(inputs):
        fired = neuron.step(current_time=cycle, input_current=stim)
        voltages.append(neuron.v)
        spikes.append(fired)

    return voltages, spikes


def run_stochastic_multiplication() -> dict:
    """
    Challenge 7B: Stochastic Multiplication Energy Trade-off.
    Generates stochastic streams for 0.60 and 0.70, AND multiplies them, and decodes.
    """
    from stochastic_sim import LFSR, StochasticGenerator, StochasticArithmetic, StochasticDecoder

    lfsr_a = LFSR(seed=101, width=16)
    lfsr_b = LFSR(seed=202, width=16)

    results = {}
    for length in [64, 1024]:
        stream_a = StochasticGenerator.to_unipolar(0.60, length, lfsr_a)
        stream_b = StochasticGenerator.to_unipolar(0.70, length, lfsr_b)

        stream_out = StochasticArithmetic.multiply_unipolar(stream_a, stream_b)
        decoded_product = StochasticDecoder.decode_unipolar(stream_out)
        results[length] = decoded_product

    return results


# =====================================================================
# Lab Module 8 — Cryogenic Superconducting Logic and Refrigeration Penalty
# =====================================================================

def run_cryo_and_timing_lab() -> dict:
    """
    Grades Lab 8. Simulates setup timing violation and calculates ERSFQ vs RSFQ cooling costs.
    """
    from sfq_sim import DFlipFlop, CryogenicEnergyModel

    dff = DFlipFlop(name="LabDFF", setup_time=3.0, prop_delay=5.0)

    # Nominal case: D at 10.0 ps, CLK at 20.0 ps (Diff = 10.0 ps > 3.0 ps setup)
    dff.process_pulse_d(10.0)
    nominal_fired, nominal_time, nominal_warns = dff.process_pulse_clk(20.0)

    # Violating case: D at 53.5 ps, CLK at 55.0 ps (Diff = 1.5 ps < 3.0 ps setup)
    dff.process_pulse_d(53.5)
    violating_fired, violating_time, violating_warns = dff.process_pulse_clk(55.0)

    # Refrigeration Power Evaluation
    energy_model = CryogenicEnergyModel(temp_cold=4.2, pct_carnot_efficiency=0.005)

    rsfq_metrics = energy_model.evaluate_system_energy(
        active_cycles=100_000_000, freq_ghz=100.0, num_jjs=100_000,
        switching_events=10_000_000, ersfq_mode=False
    )

    ersfq_metrics = energy_model.evaluate_system_energy(
        active_cycles=100_000_000, freq_ghz=100.0, num_jjs=100_000,
        switching_events=10_000_000, ersfq_mode=True
    )

    return {
        "nominal_success": nominal_fired and (len(nominal_warns) == 0),
        "violating_prevented": (not violating_fired) and (len(violating_warns) > 0),
        "rsfq_utility_joules": rsfq_metrics["room_temp_utility_energy_Joules"],
        "ersfq_utility_joules": ersfq_metrics["room_temp_utility_energy_Joules"]
    }
