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
