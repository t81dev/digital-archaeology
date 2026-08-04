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

## Lab Module 3 — Micro-Segmentation via Capability-Based Hardware

### Core Theoretical Concepts
- **The Principle of Least Privilege**: Memory segments must be strictly confined.
- **Hardware Tagged Memory**: Memory words are accompanied by a 1-bit metadata tag. If a memory location holds a capability (base, limit, permissions), the tag is 1. If any arithmetic or user instruction attempts to rewrite or alter the capability, the hardware tag is automatically cleared to 0, rendering it unforgeable.
- **Automatic Bounds Checks**: Every register-indirect memory read or write checks the address against the active capability register `base` and `limit`. Violations cause instant hardware CPU traps.

### Hands-On Challenge: Implementing Secure Domain Transitions
In a secure system, a user program must transfer control to a trusted system routine (e.g., to write a file or allocate memory) without exposing secret kernel keys. This is achieved using a **Domain Transition Gate**.

### Exercise Problem
Program a sequence of operations where a CPU attempts to access RAM outside its allocated segment, verify that the capability processor halts the execution, then call a valid registered secure service gate to retrieve a resource.

#### Model Solution (Python)
```python
from capability_sim import TaggedCPU, TaggedRAM, Capability, DomainTransitionGate

cpu = TaggedCPU()
ram = TaggedRAM()

# Set up restricted user context
user_cap = Capability(base=50, limit=60, permissions={"READ", "WRITE"})

# Try to write within bounds (Success)
cpu.write_memory(ram, user_cap, addr=55, value=42)
print("Safe access written:", cpu.read_memory(ram, user_cap, addr=55))

# Try to write out of bounds (Fails)
try:
    print("Attempting OOB write to address 65...")
    cpu.write_memory(ram, user_cap, addr=65, value=99)
except Exception as e:
    print(f"✓ Security Violation Caught: {e}")
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

## Grading Criteria & System Verification

For all submissions, systems engineering students are assessed on:
1. **Mathematical correctness**: Does the custom balanced ternary arithmetic or dataflow routing yield the exact expected value?
2. **Robustness of constraints**: Are capability access gates protected against address overflows?
3. **Liveness**: Does the concurrent design avoid deadlock and satisfy the progress property?
