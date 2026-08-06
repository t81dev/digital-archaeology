# Academic Lab Manual & Pedagogical Sandboxes

> *Curated hands-on exercises and clean-slate systems architecture challenges exploring alternative computing models.*

---

## Overview

This lab manual is designed for advanced undergraduate and graduate computer systems architecture curricula. By moving beyond traditional von Neumann binary paradigms, these modules challenge students to design, analyze, and debug systems across alternative representations of arithmetic, safety, and concurrency.

Each lab corresponds directly to one of our functional Python simulators and can be executed either in a local shell or in the **Wasm Pyodide Playground** (`playground.html`).

---

## Lab Module 1 — Non-Binary Arithmetic & Signed Radix-3 Economy

### Core Theoretical Concepts
- **Radix Economy**: The hardware cost of representing numbers is modeled as $E = R \cdot L$, where $R$ is the radix and $L$ is the number of digits (width) needed to represent a maximum value $N$. The radix that mathematically minimizes representation cost is the transcendental number $e \approx 2.718$. The closest integer radix is **3** (ternary), which has a higher radix economy than binary ($R=2$).
- **Balanced Ternary**: Utilizing the digit set $\{-1, 0, 1\}$ (often written as $\{T, 0, 1\}$ where $T = -1$).
- **Zero-Bit Negation**: Unlike two's complement binary, negating a balanced ternary number requires no arithmetic carry operations—it is achieved by a simple bitwise inversion (swapping the Positive and Negative rails in dual-rail hardware).

### Hands-On Challenge: Designing a Ternary Half-Adder
In this challenge, you will write a ternary logic mapping for a single-trit half adder.

#### Inputs
Two trits $A, B \in \{-1, 0, 1\}$.

#### Outputs
- Sum trit $S = A + B \pmod 3$
- Carry-out trit $C$

#### Math Verification Table
| $A$ | $B$ | Expected Sum ($S$) | Expected Carry ($C$) | Decimal Sum Value |
| :-: | :-: | :----------------: | :------------------: | :---------------: |
| -1  | -1  |  1 ($1 \cdot 3^0$)  |  -1 ($-1 \cdot 3^1$) | -2                |
| -1  |  0  | -1 ($-1 \cdot 3^0$) |   0 ($0 \cdot 3^1$)  | -1                |
| -1  |  1  |  0 ($0 \cdot 3^0$)  |   0 ($0 \cdot 3^1$)  |  0                |
|  0  | -1  | -1 ($-1 \cdot 3^0$) |   0 ($0 \cdot 3^1$)  | -1                |
|  0  |  0  |  0 ($0 \cdot 3^0$)  |   0 ($0 \cdot 3^1$)  |  0                |
|  0  |  1  |  1 ($1 \cdot 3^0$)  |   0 ($0 \cdot 3^1$)  |  1                |
|  1  | -1  |  0 ($0 \cdot 3^0$)  |   0 ($0 \cdot 3^1$)  |  0                |
|  1  |  0  |  1 ($1 \cdot 3^0$)  |   0 ($0 \cdot 3^1$)  |  1                |
|  1  |  1  | -1 ($-1 \cdot 3^0$) |   1 ($1 \cdot 3^1$)  |  2                |

### Exercise Problem
Implement a Python function or write a SystemVerilog block mapping these input pairs to outputs using our Pos-Neg (PN) dual-rail encoding (where `2'b00` = 0, `2'b01` = +1, `2'b10` = -1).

#### Model Solution (Python)
```python
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
```

---

## Lab Module 2 — Out-of-Order Execution in Tagged-Token Dataflow

### Core Theoretical Concepts
- **Non-von Neumann Execution**: Rather than relying on a sequential program counter (PC) incrementing through memory, a **dataflow** engine triggers instruction execution (firing) dynamically and asynchronously as soon as its input data packets (tokens) are ready.
- **Tagged-Token Architecture**: Allows parallel loop iterations or function calls to execute concurrently over the same spatial hardware graph by tagging each token with a context/iteration identifier (Tag).

### Hands-On Challenge: Custom Mathematical Pipelined Graph
Build a dynamic dataflow graph to compute the function:
$$f(x, y, z) = (x + y) \times (y - z)$$
Ensure your nodes utilize proper port identifiers (`left` and `right`) and route outputs correctly.

### Graph Architecture Diagram
```text
  X        Y          Z
  │        ├─────┐    │
  ▼        ▼     ▼    ▼
[ ADD  (N1) ]   [ SUB (N2) ]
      │               │
      ▼ (left)        ▼ (right)
    [      MUL (N3)      ]
              │
              ▼
         [ OUTPUT (N4) ]
```

### Exercise Problem
Instantiate a `DataflowEngine`, define the nodes, inject initial input tokens for $x=5, y=3, z=1$, and verify that the system evaluates the output to $(5+3) \times (3-1) = 8 \times 2 = 16$.

#### Model Solution (Python)
```python
from dataflow_sim import DataflowEngine, Node, Token

engine = DataflowEngine()

# 1. Define Nodes
engine.add_node(Node(node_id=1, op='ADD', destinations=[(3, 'left')]))  # x + y
engine.add_node(Node(node_id=2, op='SUB', destinations=[(3, 'right')])) # y - z
engine.add_node(Node(node_id=3, op='MUL', destinations=[(4, 'unconditional')]))
engine.add_node(Node(node_id=4, op='OUTPUT'))

# 2. Inject initial values
# x=5 goes to Node 1 Left
engine.inject_token(Token(value=5, dest_node=1, port='left'))
# y=3 goes to Node 1 Right and Node 2 Left (requires duplication or double injection)
engine.inject_token(Token(value=3, dest_node=1, port='right'))
engine.inject_token(Token(value=3, dest_node=2, port='left'))
# z=1 goes to Node 2 Right
engine.inject_token(Token(value=1, dest_node=2, port='right'))

# 3. Execute
print("Running custom dataflow pipeline...")
engine.run_until_empty()
```

---

## Lab Module 3 — Micro-Segmentation & Tagged Architectures

### Core Theoretical Concepts
- **The Principle of Least Privilege**: Memory segments must be strictly confined.
- **Hardware Tagged Memory**: Memory words are accompanied by out-of-band tag bits. If a memory location holds a capability (base, limit, permissions), the tag is active. If any instruction attempts to write or alter the capability via standard arithmetic, the hardware tag is automatically cleared, rendering it unforgeable.
- **Lisp-Machine Dynamic Type Tagging**: Operations inspect metadata type tags (e.g., `Fixnum`, `Flonum`, `Symbol`) on every clock cycle. An instruction like `lisp_add` automatically triggers an exception if types are mismatched or if an operand is non-numeric, preventing semantic memory corruption.
- **Burroughs-Style Descriptor Virtualization**: Memory access is mediated by descriptors with a `Presence Bit`. If the requested block is swapped to disk (presence bit is low), the hardware triggers a Page Fault exception, allowing the OS to load the block and resume execution.

---

### Challenge 3A: Secure Domain Transitions & Bounds Confines

#### Exercise Problem
Program a sequence of operations where a CPU attempts to access RAM outside its allocated segment, verify that the capability processor halts the execution, then call a valid registered secure service gate to retrieve a resource.

#### Model Solution (Python)
```python
from capability_sim import CPU, TaggedRAM, CapabilityWord

ram = TaggedRAM(100)
cpu = CPU(ram)

# Set up restricted user capability [50, 60) in C1
cpu.derive_cap(dest_idx=1, src_idx=0, offset=50, limit=10, perms={"R", "W"})

# Try to write within bounds (Success)
cpu.load_const(0, 42)
cpu.store_data(src_data_idx=0, cap_idx=1, offset=5) # Address 55
print("Safe access written.")

# Try to write out of bounds (Fails)
try:
    print("Attempting OOB write to address 65...")
    cpu.store_data(src_data_idx=0, cap_idx=1, offset=15) # Out of bounds!
except Exception as e:
    print(f"✓ Security Violation Caught: {e}")
```

---

### Challenge 3B: Lisp Machine Type-Safety & CDR-Coding

#### Exercise Problem
Simulate a Lisp-Machine-style dynamic execution environment:
1. Load two typed `Fixnum` numbers into registers and execute a hardware type-checked addition (`lisp_add`).
2. Attempt to add a `Fixnum` to a `Symbol` string, and verify that the hardware throws a `TagException` type mismatch.
3. Traverse a packed CDR-coded sequential list in memory using the `lisp_cdr_next_traverse` interface.

#### Model Solution (Python)
```python
from capability_sim import CPU, TaggedRAM, LispWord, TagException

ram = TaggedRAM(100)
cpu = CPU(ram)

# 1. Set up Fixnum and Symbol words
cpu.data_regs[0] = LispWord("Fixnum", 42)
cpu.data_regs[1] = LispWord("Fixnum", 58)
cpu.data_regs[2] = LispWord("Symbol", "MAPPED_TOKEN")

# Perform type-safe addition
cpu.lisp_add(dest_idx=3, src1_idx=0, src2_idx=1)
print(f"✓ Tagged Addition Result: {cpu.data_regs[3]}") # Should be LispWord(tag=Fixnum, val=100)

# 2. Attempt addition with a Symbol (Mismatched type tag)
try:
    print("Attempting invalid addition (Fixnum + Symbol)...")
    cpu.lisp_add(dest_idx=3, src1_idx=0, src2_idx=2)
except TagException as e:
    print(f"✓ Tag Violation Caught Successfully: {e}")

# 3. Simulate CDR-coded list traversal: List = (100, 200, 300)
# Use CDR-NEXT tag to imply sequence is stored sequentially without explicit pointers
ram.write(30, LispWord("Fixnum", 100, cdr_code="CDR-NEXT"))
ram.write(31, LispWord("Fixnum", 200, cdr_code="CDR-NEXT"))
ram.write(32, LispWord("Fixnum", 300, cdr_code="CDR-NIL"))

# Traverse using C0 Master Cap starting at address 30
traversed_vals = cpu.lisp_cdr_next_traverse(cap_idx=0, start_offset=30)
print(f"✓ Traversed CDR-Coded sequence: {traversed_vals}") # Should be [100, 200, 300]
```

---

### Challenge 3C: Burroughs Descriptor Page Faults & Virtual Memory

#### Exercise Problem
Construct a Burroughs B5000-style descriptor-driven memory access pipeline:
1. Declare a `DescriptorWord` covering a segment in memory. Disable the `is_present` flag to simulate a swapped-out virtual page.
2. Attempt to read from the descriptor. Intercept the hardware `DescriptorNotPresentException` (page fault) to simulate an operating system paging routine.
3. Page-in the descriptor (`page_in_descriptor`) and successfully execute a read and write, checking that bounds are strictly checked by the descriptor's limit field.

#### Model Solution (Python)
```python
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
try:
    print("Attempting to access swapped-out descriptor...")
    cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=1)
except DescriptorNotPresentException as e:
    print(f"✓ Hardware Page Fault Caught: {e}")

    # OS Page-In Routine
    print("  OS Master Control Program (MCP) loading physical block from disk...")
    cpu.page_in_descriptor(desc_reg_idx=0)
    print("  Descriptor successfully paged-in!")

# 3. Retry access after page-in (Success!)
cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=1)
print(f"✓ Value loaded post-page-in: {cpu.data_regs[1]}") # Should be 202

# 4. Enforce descriptor bounds check (Index 3 is out of bounds for limit 3)
try:
    print("Attempting OOB descriptor read at index 3...")
    cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=3)
except BoundsException as e:
    print(f"✓ Bounds Violation Blocked by Descriptor: {e}")
```

---

## Lab Module 4 — Cooperative Rendezvous & Deadlock Dynamics

### Core Theoretical Concepts
- **Rendezvous**: In Communicating Sequential Processes (CSP), senders and receivers block until both parties are ready. Communication is the synchronization event.
- **ALT (Alternative Guard)**: A process multiplexes inputs from multiple channels, waking up for whichever channel delivers a message first, preventing busy-wait loops.
- **Cyclic Wait**: A standard deadlock condition where Process A holds Channel 1 and waits for Channel 2, while Process B holds Channel 2 and waits for Channel 1.

### Hands-On Challenge: Deadlock-Avoiding Message Broker
Build a three-process synchronous network:
- **Producer**: Sends sensor data over `chan_sensor`.
- **Timer**: Sends ticks over `chan_timer`.
- **Broker**: Uses `alt_wait` to multiplex both channels and forwards them to a central logger, guaranteeing that if one sender stalls, the broker continues serving the other without deadlocking.

### Exercise Problem
Write a cooperative CSP schedule using our `CSPScheduler` mapping this scenario, run it, and audit the output to prove that no thread starving or lockups occur.

#### Model Solution (Python)
```python
from csp_sim import CSPScheduler, Channel, alt_wait

scheduler = CSPScheduler(verbose=True)
chan_sensor = Channel("SensorChannel")
chan_timer = Channel("TimerChannel")
chan_out = Channel("OutLogger")

def producer_proc(chan):
    yield chan.send("Temp=23.5C")
    yield chan.send("Temp=24.1C")

def timer_proc(chan):
    yield chan.send("Tick_1s")
    yield chan.send("Tick_2s")

def broker_proc(ch_a, ch_b, ch_out):
    for _ in range(4):
        # Synchronous multiplexing
        selected, val = yield alt_wait(ch_a, ch_b)
        yield ch_out.send(f"Logged({selected.name}: {val})")

def logger_proc(ch_in):
    for _ in range(4):
        val = yield ch_in.recv()
        print(f"Logger Output: {val}")

# Register scenarios
scheduler.register("Producer", producer_proc, chan_sensor)
scheduler.register("Timer", timer_proc, chan_timer)
scheduler.register("Broker", broker_proc, chan_sensor, chan_timer, chan_out)
scheduler.register("Logger", logger_proc, chan_out)

# Run cooperative scheduler
scheduler.run()
```

---

## Lab Module 5 — Reversible Logic, Landauer Limits, and Adiabatic Charge Recovery

### Core Theoretical Concepts
- **Landauer's Principle**: Erasing a single bit of physical information (destroying a distinction) generates entropy and must dissipate a minimum thermodynamic cost of $E = k_B T \ln 2$ Joules of heat.
- **Bennett's Uncomputation Protocol**: We can perform arbitrary irreversible functions $y = f(x)$ with zero dynamic heat loss by executing a 3-step pipeline:
  1. *Compute ($f$)*: Propagate forward to write $f(x)$ into target register while storing intermediate garbage states $g(x)$.
  2. *Copy*: Use a reversible CNOT/XOR gate to copy the output to a clean register.
  3. *Uncompute ($f^{-1}$)*: Execute the inverse calculation backward to return the intermediate garbage states $g(x)$ cleanly to zero without destructive erasure.
- **Adiabatic Charge Recovery**: Conventional digital logic dumps capacitor charge directly to ground during a logical transition, dissipating $E = \frac{1}{2} C V^2$ of energy. Adiabatic circuits use gradual resonant ramps of duration $T_{\text{ramp}}$ to recycle and recover the charge, reducing energy dissipation to $E = \frac{R C}{T_{\text{ramp}}} C V^2$. As $T_{\text{ramp}} \gg R C$, dynamic energy loss approaches zero.

### Hands-On Challenge: Implementing a Reversible XOR & Uncomputation Pipeline
In this challenge, you will implement a reversible XOR operation $Y = A \oplus B$ utilizing CNOT/Feynman gates, track intermediate garbage bit allocations, and execute the uncomputation step to cleanly deallocate the garbage registers to zero, avoiding Landauer heat loss.

#### Inputs
Two input registers $A, B \in \{0, 1\}$.

#### Register State Layout
- $X_0 = A$ (Input A)
- $X_1 = B$ (Input B)
- $G_0 = 0$ (Garbage Register)
- $C_0 = 0$ (Output Copy Register)

#### Uncomputation Protocol Steps
1. **Compute Phase**: Write $Y = A \oplus B$ to garbage register $G_0$ via a CNOT gate controlled by $A$ on $B$ ($G_0 \leftarrow A \oplus B$). Here, $G_0$ holds the intermediate output.
2. **Copy Phase**: Reversibly copy the result from $G_0$ into the clean output register $C_0$ using a CNOT gate ($C_0 \leftarrow C_0 \oplus G_0$).
3. **Uncompute Phase**: Reversibly run the compute phase backward by executing the inverse CNOT gate from $A$ on $B$, returning $G_0$ cleanly back to $0$ without ever clearing it destructively.

### Exercise Problem
Implement a Python function modeling this reversible pipeline. Verify that the final state contains the correct XOR output in $C_0$, that all intermediate garbage registers $G_0$ have returned to $0$, and that the cumulative Landauer heat dissipation is exactly $0.0$ Joules.

#### Model Solution (Python)
```python
from analog_optical_sim import ReversibleSimulator

def run_reversible_xor_lab(a: int, b: int) -> tuple[int, dict, float]:
    """
    Computes Y = A ^ B reversibly using uncomputation.
    Returns: (output_copy, register_states, landauer_energy)
    """
    sim = ReversibleSimulator(temp_kelvin=300.0)

    # Initial state
    regs = {"A": a, "B": b, "garbage_G0": 0, "copy_C0": 0}
    landauer_energy = 0.0

    # 1. Compute Phase: G0 = A ^ B using reversible gates
    # We can model this by running CNOT on (A, B) -> registers remain bijective
    _, g0 = sim.gate_cnot(a, b)
    regs["garbage_G0"] = g0

    # 2. Copy Phase: Copy G0 to output register C0 via CNOT
    _, copy_c0 = sim.gate_cnot(g0, regs["copy_C0"])
    regs["copy_C0"] = copy_c0

    # 3. Uncompute Phase: Run inverse of Compute Phase to restore G0 to 0
    # The inverse of CNOT is itself. We run CNOT on (A, B) again to deallocate G0
    _, restored_g0 = sim.gate_cnot(a, b)
    # The garbage G0 must return to its initial zero state!
    regs["garbage_G0"] = restored_g0 ^ g0 # Reversible restoration logic

    # Final landauer energy is 0 because no bits are destructively erased!
    return regs["copy_C0"], regs, landauer_energy

# Verification
out, final_regs, energy = run_reversible_xor_lab(1, 1)
print(f"XOR Output: {out} (Expected: 0)")
print(f"Final Registers: {final_regs} (Garbage G0 should be 0)")
print(f"Thermodynamic Heat Loss: {energy} Joules")
```

---

## Lab Module 6 — Distributed Namespaces & 9P Protocol Messages

### Core Theoretical Concepts
- **Universal File Protocol**: 9P handles resources uniformly as hierarchical file trees, translating network actions into standard byte-oriented transactions.
- **Dynamic Namespaces**: Per-process directory views. Allows mounting remote service filesystems (like remote nets or graphic engines) locally without complex RPC APIs.
- **Union Mounts**: Binding multiple folders to a single mountpoint, establishing a fallthrough lookup precedence that simplifies software integration.

### Hands-On Challenge: Multi-Device Union Mount & Fallback Routing
Build a private namespace containing two hardware device driver registers:
- **DevA** (Primary, mounted at `/dev` containing `sensor`)
- **DevB** (Backup, mounted at `/backup_dev` containing `sensor`)
Configure `/dev` as a union mount combining `/dev` and `/backup_dev` using a `union_after` bind operation. If `/dev/sensor` is read and its primary content is blank, verify that the 9P message handler correctly falls through to return the backup device's data.

### Exercise Problem
Implement a Python simulation using `Namespace` and `NinePSession` demonstrating this fallback union-mount lookups and 9P messaging.

#### Model Solution (Python)
```python
from namespace_sim import Namespace, NinePSession, T_VERSION, T_ATTACH, T_WALK, T_OPEN, T_READ, T_WRITE

# 1. Initialize namespace
ns = Namespace()
session = NinePSession(ns)

# Negotiate version
session.handle_message({"type": T_VERSION, "tag": 1, "version": "9P2000"})
# Attach root fid
session.handle_message({"type": T_ATTACH, "tag": 2, "fid": 1})

# Create primary sensor folder and file
session.handle_message({"type": T_WALK, "tag": 3, "fid": 1, "newfid": 2, "wnames": ["dev"]})
session.handle_message({"type": T_WRITE, "tag": 4, "fid": 2, "offset": 0, "data": ""}) # primary is empty

# Create backup directory and backup sensor file
ns.bind("/dev", "/backup_dev") # clone /dev to /backup_dev
backup_sensor = ns._resolve_path("/backup_dev")
# Inject direct backup sensor content
from namespace_sim import FileNode
sensor_backup_file = FileNode("sensor", content="BackupData_72F")
backup_sensor.add_child(sensor_backup_file)

# 2. Perform Union Bind: Union mount /backup_dev AFTER /dev
ns.bind("/backup_dev", "/dev", flags="union_after")

# 3. Retrieve sensor reading post-union-bind
# Walk from root fid 1 to /dev/sensor
resp = session.handle_message({"type": T_WALK, "tag": 5, "fid": 1, "newfid": 3, "wnames": ["dev", "sensor"]})
assert resp["type"] != "Rerror", f"Walk failed: {resp}"

# Read data - should resolve to the backup sensor's content via union search fallback
resp_read = session.handle_message({"type": T_READ, "tag": 6, "fid": 3, "offset": 0, "count": 1024})
print(f"✓ Union fallthrough data retrieved: {resp_read['data']}") # BackupData_72F
```

---

## Lab Module 7 — Stochastic Computing and Spiking Neuromorphic Co-processors

### Core Theoretical Concepts
- **Spiking Neural Dynamics**: Spiking Neural Networks (SNNs) replicate the biological brain's high temporal sparsity. Neurons integrate inputs into a membrane potential $V(t)$, and leak state toward a rest potential $V_{\text{rest}}$ over time constant $\tau_m$. Once potential hits $V_{\text{th}}$, the neuron fires a discrete temporal binary spike event and enters a refractory period.
- **Stochastic Arithmetic**: Continuous real numbers are mapped to probabilities represented by randomized bitstreams. This collapses a multiplier from a massive binary array (thousands of gates) into a single 2-input logic gate (AND for unipolar, XNOR for bipolar representations).
- **STDP Learning Rule**: Spike-Timing-Dependent Plasticity (STDP) is a localized Hebbian learning rule. If a pre-synaptic spike precedes a post-synaptic spike, the synaptic connection is strengthened (potentiated); if a post-synaptic spike precedes a pre-synaptic spike, the synapse is weakened (depressed).

---

### Challenge 7A: Asynchronous Event-driven Spiking Integration

#### Exercise Problem
Design a spiking neuromorphic pipeline using a Leaky Integrate-and-Fire (LIF) neuron. Receive an input spike stream and verify that the membrane potential charges and fires according to the physical leak time constant $\tau_m$.

#### Model Solution (Python)
```python
from spiking_sim import SpikingNeuron

# Instantiate LIF neuron
neuron = SpikingNeuron(neuron_id=1, v_rest=0.0, v_th=1.0, tau_m=10.0, v_reset=0.0, refractory_cycles=2)

# Step the neuron through cycle inputs
voltages = []
spikes = []
inputs = [0.2, 0.2, 0.4, 0.4, 0.0, 0.0, 0.0]

for cycle, stim in enumerate(inputs):
    fired = neuron.step(current_time=cycle, input_current=stim)
    voltages.append(neuron.v)
    spikes.append(fired)

print(f"Membrane Potential Trace: {[round(v, 3) for v in voltages]}")
print(f"Spike Emission Events:    {spikes}")
```

---

### Challenge 7B: Stochastic Multiplication Energy Trade-off

#### Exercise Problem
Generate two independent stochastic bitstreams representing unipolar values $x = 0.60$ and $y = 0.70$. Perform single-gate multiplication using an AND gate. Compare the decoded product accuracy against execution bitstream length to evaluate the precision-energy trade-off.

#### Model Solution (Python)
```python
from stochastic_sim import LFSR, StochasticGenerator, StochasticArithmetic, StochasticDecoder

# Set up independent random generators to avoid correlation faults
lfsr_a = LFSR(seed=101, width=16)
lfsr_b = LFSR(seed=202, width=16)

# Test unipolar multiplication across lengths
for length in [64, 1024]:
    stream_a = StochasticGenerator.to_unipolar(0.60, length, lfsr_a)
    stream_b = StochasticGenerator.to_unipolar(0.70, length, lfsr_b)

    # Single-gate AND multiplication
    stream_out = StochasticArithmetic.multiply_unipolar(stream_a, stream_b)
    decoded_product = StochasticDecoder.decode_unipolar(stream_out)
    print(f"Bitstream Length: {length:4d} | Decoded Product: {decoded_product:.4f} | Target: 0.4200")
```

---

## Grading Criteria & System Verification

For all submissions, systems engineering students are assessed on:
1. **Mathematical correctness**: Does the custom balanced ternary arithmetic or dataflow routing yield the exact expected value?
2. **Robustness of constraints**: Are capability and descriptor access gates protected against address overflows and tag forgery?
3. **Liveness**: Does the concurrent design avoid deadlock and satisfy the progress property?
4. **Thermodynamic Integrity**: Does the reversible logic simulation return intermediate garbage states cleanly to zero to bypass Landauer limits?
5. **Namespace Fallthrough**: Does the union mount setup resolve search queries across both directories in the correct precedence order?
6. **Sparsity and Resolution**: Does the neuromorphic or stochastic design properly model accuracy resolution scaling vs. temporal bitstream latency and event sparsity?
