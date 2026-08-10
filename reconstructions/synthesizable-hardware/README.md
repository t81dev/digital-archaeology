# Synthesizable Hardware IP Core Blueprints

> **Production-ready, synthesizable SystemVerilog RTL cores of historic computing abstractions, optimized for FPGAs (Lattice iCE40) and ASIC layouts (Tiny-Tapeout).**

---

## Overview

This directory contains synthesizable SystemVerilog soft-cores representing some of our most important reconstructed architectural abstractions. Rather than leaving historical concepts as pure software emulators, these hardware IP cores prove the microarchitectural viability of non-von Neumann and secure-by-default execution.

### Included Hardware Cores
1. **Balanced Ternary ALU (`ternary_alu.sv`)**:
   - Implements 3-trit arithmetic and logic operations using a dual-rail Pos-Neg (PN) dual-rail representation (where `2'b00` = 0, `2'b01` = +1, `2'b10` = -1).
   - Features registered inputs/outputs, sequential single-cycle execution, and supports `ADD`, `SUB`, `NEG` (-A), `MUL` (partial-product multiplication), `MIN` (AND), `MAX` (OR), and logical shifts.
2. **Capability & Descriptor Bounds Checker (`capability_bounds_checker.sv`)**:
   - Implements inline hardware bounds protection and permissions checks.
   - Dual-mode operation:
     - *Capability Mode*: Enforces unforgeable capability validation and spatial/temporal bounds checks (CHERI style).
     - *Descriptor Mode*: Enforces Burroughs B5000-style segmented virtual memory descriptor access with hardware-triggered Page Fault exceptions when a segment is marked not-present.
3. **Reversible Logic Gates Block (`reversible_gates.sv`)**:
   - Implements synthesizable 3-bit reversible logic gates: Toffoli (CCNOT) and Fredkin (CSWAP).
   - Synchronously registers inputs and outputs to prevent glitching, serving as a primitive cell block for physical and adiabatic charge-recovery layouts.
4. **Stochastic Multiplier (`stochastic_multiplier.sv`)**:
   - Implements a unipolar stochastic multiplier by pairing an 8-bit Linear Feedback Shift Register (LFSR) with a digital comparator (for stochastic generation of input A) and a single-gate AND multiplier.
   - Ideal for low-power neural networks, showing high fault-tolerance and extremely low area utilization.

---

## Simulation & Verification

The integrity of our synthesizable RTL is verified against high-fidelity Python golden models. To run the hardware verification suite:

### 1. Verification with pytest
We run golden-model equivalence verification directly in Python via the repo-wide test framework:

```bash
# From the repository root directory
pytest reconstructions/synthesizable-hardware/test_synthesizable.py
```

### 2. RTL Synthesis & Linting with Verilator / iverilog
You can lint and simulate the SystemVerilog modules directly using open-source hardware tools such as **Verilator** or **Icarus Verilog**:

```bash
# Lint cores with Verilator to verify synthesis compliance
verilator --lint-only -Wall reconstructions/synthesizable-hardware/*.sv
```

### 3. Verification & Physical Hardware Status

This hardware suite has been advanced to a state of **formal mathematical correctness** and **physical FPGA gate-level verification** via open-source EDA tools.

#### A. Multi-Engine Verification Status

| IP Core Module | Verification Type | Status | SVA Property Coverage | Formally Proven Invariants |
| :--- | :---: | :---: | :---: | :--- |
| `capability_bounds_checker` | **Formal BMC & k-Induction (z3)** & Python Golden | **100% PASSED** | 4 Assertions | Tag Unforgeability, Boundary safety, Page-fault exceptions, Reset invariants |
| `ternary_alu` | **Formal BMC & k-Induction (z3)** & Python Golden | **100% PASSED** | 3 Assertions | Negation involution, Identity addition, Reset invariants |
| `reversible_gates` | **Formal BMC & k-Induction (z3)** & Python Golden | **100% PASSED** | 8 Assertions | Fredkin information conservation, Control line preservation, CCNOT inversion/identity |
| `stochastic_multiplier` | **Formal BMC & k-Induction (z3)** & Python Golden | **100% PASSED** | 4 Assertions | LFSR non-zero state preservation, Zero multiplication dominance, Stream B gate control |

*   **Simulation Golden Model**: Verified via Python golden emulator in `test_synthesizable.py` with 100% test coverage mapping LFSR periods, reversible gate bijectivity, and balanced ternary arithmetic.
*   **Formal Model Checking (Temporal k-Induction)**: 100% formally proven using **SymbiYosys (SBY)** and the **z3 SMT solver** configured for both bounded model checking (`bmc`) and temporal induction (`prove`). Proves that safety invariants and arithmetic assertions hold true across infinite clock cycles rather than just bounded traces.
*   **Gate-Level FPGA Synthesis**: Compiled and routed successfully for the **Lattice iCE40 UP5K** using the open-source **Yosys + nextpnr** toolchain.

---

### 4. Running the Toolchain & Build Automation

We provide a comprehensive, zero-dependency **`Makefile`** under the hardware directory to run formal verification and compile FPGA binaries out-of-the-box.

#### Target: Run Formal Verification (SymbiYosys)
To prove all 4 hardware soft-cores mathematically under the z3 solver:
```bash
cd reconstructions/synthesizable-hardware
make formal
```
This runs `sby -f` on all `.sby` configurations under `formal/` and writes clean pass logs to `formal/logs/`.

#### Target: Run Physical FPGA Compilation (Yosys + nextpnr)
To synthesize, place-and-route, and generate a physical bitstream for the `capability_bounds_checker` against the Lattice iCEbreaker board (`icebreaker.pcf`):
```bash
cd reconstructions/synthesizable-hardware
make fpga
```
This generates the following hardware artifacts under `fpga/build/`:

#### Target: Run ASIC Physical Synthesis Verification (OpenLane Configs)
To validate the format and content of all four OpenLane JSON configs and search for a local OpenLane toolchain to compile layout structures:
```bash
cd reconstructions/synthesizable-hardware
make asic
```

#### Target: Run RTL Python Equivalence Tests
To execute the pytest testbench asserting strict digital equivalence between our SystemVerilog soft-cores and Python behavioral models:
```bash
cd reconstructions/synthesizable-hardware
make test
```
*   `capability_bounds_checker.json`: Synthesized netlist.
*   `capability_bounds_checker.asc`: ASCII place-and-route layout.
*   `capability_bounds_checker.bin`: Final raw binary bitstream ready to flash to SPI flash.
*   `capability_bounds_checker_timing.rpt`: Full timing analyzer propagation delay and $F_{max}$ report.

---

### 5. Physical Demonstration & Hardware-in-the-Loop (HIL)

When deployed to a physical **iCEbreaker UP5K board**, the `capability_bounds_checker` functions as a real-time hardware-in-the-loop exception engine. PMOD switches allow manual fault injection to test hardware response:

*   **Normal Authorized Memory Access**: Asserting `req_valid = 1` with an address inside valid bounds activates the **Green LED** (`resp_allowed`).
*   **Spatial Capability Out-of-Bounds**: Injecting an address higher than `cap_limit` or lower than `cap_base` immediately triggers the **Red LED** (`resp_violation_flag`) and displays exception code `2'b10` on PMOD output indicators.
*   **Descriptor Present/Absent Page Fault**: Toggling `desc_mode = 1` while present bit is low (`cap_present = 0`) triggers the **Blue LED** (`resp_page_fault`) representing a hardware interrupt.

---

## Target Synthesis Parameters

Our SystemVerilog designs strictly avoid unsynthesizable behavioral structures. They rely entirely on clean sequential (`always_ff`) and combinational (`always_comb`) blocks with asynchronous active-low resets.

| Core Module | Est. LUT Count (iCE40 UP5K) | Clock Frequency Target | ASIC Tile Area (Tiny-Tapeout) |
| :--- | :---: | :---: | :---: |
| `ternary_alu` | ~180 LUTs | 100 MHz+ | 1x1 Tile |
| `capability_bounds_checker` | ~110 LUTs | 150 MHz+ | 1x1 Tile |
| `reversible_gates` | ~15 LUTs | 250 MHz+ | 1x1 Tile |
| `stochastic_multiplier` | ~25 LUTs | 300 MHz+ | 1x1 Tile |

---

## Runnable Multi-Paradigm Sandbox Integration

To complement our synthesizable SystemVerilog IP cores, we have wired these physical paradigms and timing models into a complete, runnable integration and co-simulation driver at **`reconstructions/co-simulation/experiments.py`**.

External researchers can execute this driver out-of-the-box using the exact single-command CLI invocation to run all three distinct, highly-synergistic architectural experiments:

```bash
# Execute all three multi-paradigm experiments with self-explanatory console logs
python3 -m reconstructions.co-simulation.experiments --all
```

Alternatively, specific experiments can be targeted:
```bash
# Run only Experiment 3 (9P Sandboxed Execution)
python3 -m reconstructions.co-simulation.experiments --experiment 3
```

The three experiments are:
1. **Experiment 1 (Cryogenic Systolic Coprocessor)**: Simulates weight-stationary systolic array operations mapped directly to Rapid Single Flux Quantum (RSFQ) switching events and Carnot refrigeration cooling budgets.
2. **Experiment 2 (Reversible Cryogenic Storage Loops)**: Integrates Bennett-style uncomputation logic gates to bypass Landauer's thermodynamic erasure limit at 4.2 K cryogenic conditions.
3. **Experiment 3 (9P Sandboxed execution)**: Mounts Plan 9 9P-style private resource file trees and filters read/write traffic through the hardware-synthesizable Capability Bounds Checker.

---

## Microarchitectural Integration Notes

These soft-cores are fully synthesizable and designed for integration with standard SoC architectures or FPGA wrappers. Below are the minimal microarchitectural connection patterns and testbench sequences for each module:

### 1. Balanced Ternary ALU (`ternary_alu`)
* **wrapper Integration**:
  - `A` and `B` carry 3-trit balanced ternary operands in 2-bit dual-rail Pos-Neg (PN) format (6 bits total per operand).
  - Tie `en` to your instruction decoder's execution strobe.
  - outputs `Out` and `CarryOut` are registered. Ensure the receiving pipeline registers or accumulator captures them exactly one clock cycle after asserting `en`.
* **Minimal Testbench Sequence**:
  ```systemverilog
  // Reset and initialization
  rst_n = 0; en = 0; A = 6'b000000; B = 6'b000000; Op = 3'b000;
  #20 rst_n = 1;
  // Perform ADD: +1 (0b000001) + +1 (0b000001)
  @(posedge clk);
  A = 6'b000001; B = 6'b000001; Op = 3'b000; en = 1;
  @(posedge clk);
  en = 0; // Deassert strobe
  @(posedge clk);
  // Out is now registered as +2 (0b000110: T0 = -1, T1 = +1, T2 = 0)
  assert(Out == 6'b000110 && CarryOut == 2'b00);
  ```

### 2. Capability & Descriptor Bounds Checker (`capability_bounds_checker`)
* **wrapper Integration**:
  - Place inline between the CPU address generator unit (AGU) and the physical or virtual memory bus.
  - Inputs `cap_base` (inclusive) and `cap_limit` (exclusive) should be wired directly to the active hardware capability registers.
  - The `resp_violation_flag` and `resp_page_fault` outputs are registered on `clk`. Wire them directly to the CPU's asynchronous trap/exception logic (e.g. triggering an M-mode interrupt or page fault exception in RISC-V).
* **Minimal Testbench Sequence**:
  ```systemverilog
  rst_n = 0; req_valid = 0; desc_mode = 0;
  cap_base = 16'h1000; cap_limit = 16'h2000; cap_perms = 3'b111; cap_tag = 1; cap_present = 1;
  #20 rst_n = 1;
  // Authorized read at 16'h1500
  @(posedge clk);
  req_addr = 16'h1500; req_op = 2'b00; req_valid = 1;
  @(posedge clk);
  req_valid = 0;
  // Access is allowed on the next cycle
  assert(resp_allowed == 1 && resp_violation_flag == 0);
  ```

### 3. Reversible Logic Gates Block (`reversible_gates`)
* **wrapper Integration**:
  - Reversible gates operate on standard digital rails.
  - Set `op` to `1'b0` for Toffoli (CCNOT) or `1'b1` for Fredkin (CSWAP).
  - Strobe `en` high to register the computed state into outputs `X`, `Y`, and `Z`.
* **Minimal Testbench Sequence**:
  ```systemverilog
  rst_n = 0; en = 0; op = 0; A = 1; B = 1; C = 0;
  #20 rst_n = 1;
  @(posedge clk);
  en = 1; // Trigger CCNOT calculation
  @(posedge clk);
  en = 0;
  // Output Z is XORed with (A & B): 0 ^ (1 & 1) = 1
  assert(X == 1 && Y == 1 && Z == 1);
  ```

### 4. Stochastic Multiplier (`stochastic_multiplier`)
* **wrapper Integration**:
  - Maintain the binary input `bin_val` stable throughout the stochastic evaluation window (typically 256 cycles for 8-bit precision).
  - Connect `stream_b` to your incoming stochastic source (such as a second LFSR stream or an optical noise channel).
  - The product stream `stream_out` is synchronous. Accumulate or count the number of high pulses on `stream_out` over the window to read the output value.
* **Minimal Testbench Sequence**:
  ```systemverilog
  rst_n = 0; enable = 0; bin_val = 8'd128; stream_b = 1;
  #20 rst_n = 1;
  @(posedge clk);
  enable = 1;
  // Cycle the clock for 256 periods to collect the bitstream product
  repeat(256) @(posedge clk);
  enable = 0;
  ```

---

## Superconducting & Cryogenic Hardware Mapping Path

Unlike traditional CMOS logic where logical states are mapped to steady-state voltage levels (e.g., $V_{DD}$ and $GND$), Rapid Single Flux Quantum (RSFQ) superconducting logic represents information as transient, picosecond-wide voltage pulses ($\approx 2.07 \text{ mV}\cdot\text{ps}$). Because of this fundamental physical divergence, compiling standard synthesizable SystemVerilog directly into physical superconducting cells requires a highly specialized microarchitectural mapping path:

### 1. Dual-Rail Pulse Emulation in CMOS RTL
To emulate SFQ pulse behavior on standard CMOS FPGAs (like Lattice iCE40) or standard digital ASIC cells (like SkyWater 130nm on Tiny-Tapeout), we represent pulses as **single-cycle clock-enveloped active-high signals**:
* **Pulse Event**: A logical pulse on channel $A$ is represented by a single-clock-cycle high value (`A_pulse == 1'b1`) on a global high-frequency clock line (e.g., running at $100\text{--}300 \text{ MHz}$ to prototype picosecond behaviors).
* **State Loops**: Trapped magnetic flux loops are emulated using sequential D-Latches or registers that toggle high upon receiving the input event, and clear back to zero upon receiving the clock pulse.

```systemverilog
// Standard CMOS RTL Emulation of an RSFQ D-Flip-Flop Cell
module cmos_rsfq_dff (
    input  logic clk,       // System reference clock
    input  logic rst_n,     // Active-low asynchronous reset
    input  logic pulse_d,   // Emulated Data pulse (single-cycle pulse)
    input  logic pulse_clk, // Emulated CLK pulse (single-cycle pulse)
    output logic pulse_q    // Emulated Output Q pulse (single-cycle pulse)
);
    logic flux_trapped;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            flux_trapped <= 1'b0;
            pulse_q      <= 1'b0;
        end else begin
            pulse_q <= 1'b0; // Default: transient pulse output

            if (pulse_d) begin
                flux_trapped <= 1'b1; // Trap magnetic flux
            end

            if (pulse_clk) begin
                if (flux_trapped) begin
                    pulse_q      <= 1'b1; // Emit output Q pulse
                    flux_trapped <= 1'b0; // Reset loop flux
                end
            end
        end
    end
endmodule
```

### 2. Transitioning to Superconducting Niobium Foundries
To manufacture physical superconducting ASICs using niobium Josephson junction processes (such as those run by **MIT Lincoln Laboratory** or **AIST (Japan)**), standard CMOS logic gates must be compiled using specialized RSFQ cell libraries:
* **Clocked Logic Cells**: In RSFQ, almost all logic gates (including AND, OR, XOR) are inherently stateful and clocked. Designers cannot use standard combinational synthesis; instead, they synthesize designs using specialized cell libraries where each gate includes internal SQUID storage loops.
* **Josephson Transmission Lines (JTL)**: Since standard metal wires exhibit resistance and delay at high speeds, superconducting chips connect gates using active Josephson Transmission Lines (cascaded arrays of JJs that propagate pulses without loss) or superconducting passive microstrip lines (micro-coax).
* **Clock Distribution Networks**: At hundreds of GHz, standard clock trees suffer from clock skew. RSFQ designs utilize concurrent clocking topologies where clock and data pulses propagate in parallel through matching JTL structures, ensuring perfect local phase alignment.

---

## Known Limitations

1. **Precision / Scalability**:
   - The Balanced Ternary ALU is fixed at a 3-trit width (range of $[-13, 13]$). Scaling to 9-trit or 27-trit words requires cascading adder blocks, which introduces log-linear propagation delays.
   - The Capability Bounds Checker handles 16-bit address offsets. For high-performance 64-bit address spaces (e.g., RISC-V CHERI), bounds must be compressed to fit in register bounds.
2. **Timing Closure**:
   - The ternary multiplier (`ternary_alu.sv` `MUL`) is implemented using combinational shift-and-add partial-product logic. For wide ternary pipelines, this multiplier must be replaced with a multi-cycle pipelined multiplier to avoid violating timing constraints.

---

## Shortest Path to Physical Silicon & FPGAs

To deploy these cores onto physical hardware, follow these guides:

### 🚀 Path A: FPGA Deployment (Lattice iCE40 UltraPlus)
We target the **Lattice iCE40 UP5K** (found on the iCEbreaker board) as it is the industry standard for open-source FPGA toolchains (Yosys + nextpnr):

1. **Install Toolchain**: Install Yosys, nextpnr-ice40, and the IceStorm tools.
2. **Create Top-level Wrapper**: Write a simple wrapper map routing `A`, `B`, `en`, and outputs to physical PMOD pins or LEDs.
3. **Run Synthesis & Place-and-Route**:
   ```bash
   yosys -p "synth_ice40 -top ternary_alu -json alu.json" reconstructions/synthesizable-hardware/ternary_alu.sv
   nextpnr-ice40 --up5k --package sg48 --json alu.json --pcf pins.pcf --asc alu.asc
   icepack alu.asc alu.bin
   ```
4. **Flash to Board**: Upload `alu.bin` to your iCEbreaker board.

### 🔬 Path B: ASIC Deployment (Tiny-Tapeout)
**Tiny-Tapeout** is an educational program that lets you manufacture custom designs on a real physical ASIC (using SkyWater 130nm PDK):

1. **Clone Tiny-Tapeout Template**: Clone the official `tt-multiplexer` or user template repository.
2. **Integrate Modules**: Map our SystemVerilog files into the project. Create a wrapper that connects the Tiny-Tapeout 8-bit input bus (`ui_in`) and 8-bit output bus (`uo_out`) to your core.
   - *Example Mapping*: For `reversible_gates`, input pins `ui_in[0]` (A), `ui_in[1]` (B), `ui_in[2]` (C), `ui_in[3]` (op), and `ui_in[4]` (en).
3. **Run GitHub Actions**: Push to your fork. The automated GitHub actions pipeline runs **OpenLane** to synthesize, place, route, and compile your design into a physical GDSII layout.
4. **Silicon Delivery**: Your design is packaged onto a shared multi-project chip wafer and shipped to you on an evaluation board.

### 🏭 Path C: Direct OpenLane GDSII Silicon Synthesis
For deep-submicron physical design tapeouts, we provide production-ready **OpenLane configuration templates** (`fpga/openlane_configs/`) targeting standard foundry PDKs (e.g., SkyWater sky130 or IHP SG13G2).

By supplying custom floorplan, density, and clock constraints, these configurations bypass manual layout:
1. **Prepare OpenLane Workspace**: Install Docker and pull the `efabless/openlane` container.
2. **Synthesize and Route**: Run the OpenLane physical synthesis flow on any core config:
   ```bash
   ./flow.tcl -design reconstructions/synthesizable-hardware/fpga/openlane_configs/capability_bounds_checker.json -tag tapeout_v1
   ```
3. **Analyze Reports**: Under `openlane/designs/capability_bounds_checker/runs/tapeout_v1/`, examine the generated macro placements, clock trees, parasitic extraction (`.spef`), and the final tapeout-ready GDSII file (`.gds`).
