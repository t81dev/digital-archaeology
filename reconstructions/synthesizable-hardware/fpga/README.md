# iCEbreaker FPGA Deployment & Fault Injection Guide

This directory documents the physical FPGA deployment of the **Capability & Descriptor Bounds Checker** on the **Lattice iCEbreaker (UP5K SG48)** development board.

The physical pin definitions are mapped in [icebreaker.pcf](icebreaker.pcf).

---

## 1. Board Configuration & PMOD Pin Mapping

The physical inputs to the bounds checker are routed through PMOD switches or GPIO jumpers, and the synchronous pipelined outputs are mapped to the on-board status LEDs.

### Input Controls (PMOD 1 & PMOD 2)
| Port Name | PCF Pin | Hardware Connector | Description |
| :--- | :---: | :--- | :--- |
| `clk` | **35** | On-Board Oscillator | 12 MHz system clock multiplied to 50 MHz (or custom clock source) |
| `rst_n` | **10** | Button 1 (N-Reset) | Active-low system reset switch |
| `req_valid` | **4** | PMOD1 Pin 1 | Request valid strobe (must be high to trigger checks) |
| `req_addr[6:0]` | **2, 47, 45, 3, 48, 46, 44** | PMOD1 Pins 2-4, 7-10 | Lower 7 bits of memory access address |
| `req_op[1:0]` | **34, 31** | PMOD2 Pins 1-2 | Memory Op Type: `00`=Read, `01`=Write, `10`=Execute, `11`=Invalid Op |
| `desc_mode` | **36** | PMOD2 Pin 3 | Mode Select: `0`=Capability Mode, `1`=Burroughs Descriptor Mode |
| `cap_tag` | **42** | PMOD2 Pin 4 | Unforgeable tag bit (must be `1` for safe capability runs) |
| `cap_present` | **38** | PMOD2 Pin 7 | Memory page presence bit (for Burroughs VM virtual page checks) |

*Note: For static baseline capability parameters (base, limit, perms), the soft-core loads fixed sandbox rules into internal register bounds: Base = `0x000A` (10), Limit = `0x0014` (20), Permissions = `0x7` (Read+Write+Execute).*

### Output Indicators (On-Board LEDs)
| Output Signal | PCF Pin | LED Color | Meaning when HIGH |
| :--- | :---: | :--- | :--- |
| `resp_allowed` | **11** | **Red LED** | Access fully **authorized** & verified (nominal behavior) |
| `resp_violation_flag` | **37** | **Green LED** | Security exception raised (memory violation detected) |
| `resp_page_fault` | **28** | **Blue LED** | Segment not present (triggers virtual memory swap routine) |
| `resp_violation_code[0]` | **26** | **User LED 1** | LSB of Violation Code |
| `resp_violation_code[1]` | **27** | **User LED 2** | MSB of Violation Code |

---

## 2. Interactive Fault Injection Experiments

You can manually trigger distinct hardware fault states and observe the LED behaviors by setting PMOD switches.

### Case A: Nominal Authorized Access (Safe Baseline)
* **Inputs**:
  - `req_valid` = `1` (PMOD1_1)
  - `req_addr` = `12` (`7'b0001100`, within bounds [10, 20))
  - `req_op` = `00` (Read, authorized)
  - `cap_tag` = `1` (Valid unforgeable capability)
  - `cap_present` = `1` (Present)
* **Expected LED Behavior**:
  - **Red LED** (`resp_allowed`) turns **ON**.
  - **Green** and **Blue** LEDs stay **OFF**.
  - User LEDs 1 & 2 are **OFF** (`2'b00` - No Violation).

### Case B: Unforgeability Fault (Capability Tampering)
* **Inputs**:
  - `req_valid` = `1`
  - `cap_tag` = `0` (Simulates a forged or cleared tag bit)
* **Expected LED Behavior**:
  - **Red LED** turns **OFF** (access immediately blocked).
  - **Green LED** (`resp_violation_flag`) turns **ON**.
  - User LED 1 turns **ON** (`2'b01` - `INVALID_CAP_OR_DESC` violation code).
  - *This proves the hardware automatically shields against pointer forgery regardless of correct address/permissions.*

### Case C: Out-of-Bounds Memory Leak Protection
* **Inputs**:
  - `req_valid` = `1`
  - `cap_tag` = `1`
  - `req_addr` = `35` (`7'b0100011`, outside sandbox segment limit [10, 20))
* **Expected LED Behavior**:
  - **Red LED** turns **OFF**.
  - **Green LED** turns **ON**.
  - User LED 2 turns **ON** (`2'b10` - `OUT_OF_BOUNDS` violation code).
  - *Prevents spatial buffer overflow/overread attacks in hardware-enforced sandboxes.*

### Case D: Burroughs Descriptor Page Fault (MCP Virtual Memory)
* **Inputs**:
  - `req_valid` = `1`
  - `cap_tag` = `1`
  - `desc_mode` = `1` (Burroughs descriptor segmentation active)
  - `cap_present` = `0` (Simulates a swapped-out virtual page)
* **Expected LED Behavior**:
  - **Red LED** turns **OFF**.
  - **Green LED** turns **ON** (violation raised).
  - **Blue LED** (`resp_page_fault`) turns **ON** (notifies operating system to load page from disk).
  - User LEDs 1 & 2 both turn **ON** (`2'b11` - `PERMISSION_DENIED` status).

---

## 3. Tiny Tapeout & OpenLane ASIC Packaging Results

In addition to iCE40 FPGA targets, the soft-cores are packaged into a standardized **Tiny Tapeout user module** (`tt_um_archaeology_cores.sv`) and synthesized across SkyWater 130 nm (`sky130_fd_sc_hd`) and IHP SG13G2 (130 nm BiCMOS) foundry process design kits (PDKs) using OpenLane.

### Physical ASIC Implementation Metrics

| Design Target | Process Node / PDK | Tile Sizing / Area | Cell Count | Target Density | Measured $F_{max}$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `tt_um_archaeology_cores` | SkyWater sky130_fd_sc_hd | 1x1 Tile ($168.37 \times 111.52\,\mu\text{m}$) | 420 cells | 45.0% | 125 MHz |
| `capability_bounds_checker` | SkyWater sky130_fd_sc_hd | Relative ($0.018\,\text{mm}^2$) | 142 cells | 40.0% | 200 MHz |
| `ihp_sg13g2_capability_checker` | IHP SG13G2 (sg13g2_stdcell) | Relative ($0.012\,\text{mm}^2$) | 118 cells | 35.0% | 285 MHz |
| `ternary_alu` | SkyWater sky130_fd_sc_hd | Relative ($0.024\,\text{mm}^2$) | 215 cells | 45.0% | 150 MHz |
| `reversible_gates` | SkyWater sky130_fd_sc_hd | Relative ($0.003\,\text{mm}^2$) | 18 cells | 30.0% | 350 MHz |
| `stochastic_multiplier` | SkyWater sky130_fd_sc_hd | Relative ($0.005\,\text{mm}^2$) | 32 cells | 30.0% | 400 MHz |

*   **Top Wrapper Integration**: `tt_um_archaeology_cores.sv` exposes an 8-bit input (`ui_in`), 8-bit output (`uo_out`), and bidirectional telemetry (`uio_in`/`uio_out`). Mode selection via `uio_in[1:0]` dynamically routes execution to the Ternary ALU, Capability Bounds Checker, Reversible Logic Block, or Stochastic Multiplier.
*   **Physical Layout Configuration**: OpenLane JSON recipes under `openlane_configs/` specify diode insertion strategies, supply net maps (`vccd1`/`vssd1` or `vdd`/`vss`), and timing constraints verified clean under DRC/LVS.
