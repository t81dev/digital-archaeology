#!/usr/bin/env python3
"""
Zero-Dependency Systolic Array Simulator.
Simulates Weight-Stationary (WS) and Output-Stationary (OS)
matrix multiplication cycle-by-cycle, computing execution cycles and energy proxies.
"""

import sys

class ProcessingElement:
    """
    Represents a single processing element (PE) in the systolic array.
    """
    def __init__(self, r: int, c: int):
        self.row = r
        self.col = c
        self.weight = 0.0
        self.accumulator = 0.0

        # Latches/Registers for cycle-by-cycle pipeline synchronization
        self.in_x = 0.0
        self.in_w = 0.0
        self.in_y = 0.0

        self.out_x = 0.0
        self.out_w = 0.0
        self.out_y = 0.0

        # Stat counters for energy proxies
        self.mac_count = 0
        self.hop_count = 0

    def reset(self):
        self.weight = 0.0
        self.accumulator = 0.0
        self.in_x = 0.0
        self.in_w = 0.0
        self.in_y = 0.0
        self.out_x = 0.0
        self.out_w = 0.0
        self.out_y = 0.0
        self.mac_count = 0
        self.hop_count = 0


class SystolicArraySimulator:
    """
    Cycle-accurate simulator for a 2D grid Systolic Array.
    Supports:
      - Weight-Stationary (WS) GEMM
      - Output-Stationary (OS) GEMM
    """
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[ProcessingElement(r, c) for c in range(cols)] for r in range(rows)]
        self.cycles = 0
        self.sram_reads = 0
        self.sram_writes = 0

        # Energy proxy factors (in arbitrary units)
        self.E_MAC = 1.0        # MAC unit logic cost
        self.E_SRAM_READ = 5.0  # SRAM read cost (high relative cost)
        self.E_SRAM_WRITE = 6.0 # SRAM write cost
        self.E_HOP = 0.5        # Local PE-to-PE register hop cost

    def reset_array(self):
        self.cycles = 0
        self.sram_reads = 0
        self.sram_writes = 0
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].reset()

    def simulate_weight_stationary(self, matrix_A, matrix_B):
        """
        Simulates Weight-Stationary (WS) Matrix Multiplication: C = A * B.
        - Matrix A has shape M x K.
        - Matrix B has shape K x N.
        - Weights (B) are pre-loaded and stationary in PEs grid[k][c] = B[k][c].
        - Inputs (A) stream from the left of the array.
          A[r][k] is fed to row k, col 0 at cycle t = r + k.
        - Partial sums (Y) stream from the top of the array, pre-skewed.
          Y for C[r][c] enters row 0, col c as 0.0 at cycle t = r + c.
        - Final results emerge from row K-1, col c at cycle t = r + c + K - 1.
        """
        self.reset_array()

        M = len(matrix_A)
        K = len(matrix_A[0])
        N = len(matrix_B[0])

        if K > self.rows or N > self.cols:
            raise ValueError(f"Matrix size requirements (K={K}, N={N}) exceed systolic array dimensions ({self.rows}x{self.cols})")
        if len(matrix_B) != K:
            raise ValueError("Incompatible matrix dimensions.")

        # 1. Load weights (B) into PEs
        for k in range(K):
            for c in range(N):
                self.grid[k][c].weight = matrix_B[k][c]
                self.sram_reads += 1  # Fetch weight from SRAM to load

        # 2. Compute total pipeline cycles needed
        total_cycles = M + N + K - 1
        output_matrix = [[0.0] * N for _ in range(M)]

        # 3. Step cycle-by-cycle
        for cycle in range(total_cycles):
            self.cycles += 1

            # Feed inputs into the left boundaries
            # At cycle t, row k (where 0 <= k < K) receives A[r][k] where r = t - k.
            for k in range(K):
                r = cycle - k
                if 0 <= r < M:
                    val_a = matrix_A[r][k]
                    self.grid[k][0].in_x = val_a
                    if val_a != 0.0:
                        self.sram_reads += 1
                else:
                    self.grid[k][0].in_x = 0.0

            # Feed partial sums into top boundary (0.0 for initial bias)
            for c in range(N):
                self.grid[0][c].in_y = 0.0

            # Execute MAC logic in all active PEs
            for k in range(K):
                for c in range(N):
                    pe = self.grid[k][c]
                    # Y_out = Y_in + X_in * Weight
                    pe.out_y = pe.in_y + (pe.in_x * pe.weight)
                    pe.out_x = pe.in_x
                    if pe.in_x != 0.0 or pe.in_y != 0.0:
                        pe.mac_count += 1

            # Collect final results from the bottom boundary (row K-1)
            # Result C[r][c] emerges at cycle t = r + c + K - 1
            for c in range(N):
                r = cycle - c - K + 1
                if 0 <= r < M:
                    val_c = self.grid[K-1][c].out_y
                    output_matrix[r][c] = val_c
                    self.sram_writes += 1

            # Shift/propagate registers for next cycle
            # Left to Right propagation (along rows)
            for k in range(K):
                for c in range(self.cols - 1, 0, -1):
                    self.grid[k][c].in_x = self.grid[k][c-1].out_x
                    if self.grid[k][c-1].out_x != 0.0:
                        self.grid[k][c].hop_count += 1

            # Top to Bottom propagation (along columns)
            for c in range(self.cols):
                for k in range(self.rows - 1, 0, -1):
                    self.grid[k][c].in_y = self.grid[k-1][c].out_y
                    if self.grid[k-1][c].out_y != 0.0:
                        self.grid[k][c].hop_count += 1

        return output_matrix

    def simulate_output_stationary(self, matrix_A, matrix_B):
        """
        Simulates Output-Stationary (OS) Matrix Multiplication: C = A * B.
        - Accumulators are stationary in PEs grid[r][c] = C[r][c].
        - Inputs (A) stream from the left boundary.
          A[r][k] is fed to row r, col 0 at cycle t = r + k.
        - Weights (B) stream from the top boundary.
          B[k][c] is fed to row 0, col c at cycle t = k + c.
        - The computation is complete for all r, c after the wave finishes.
        - Accumulators are then serially shifted down to the bottom and read out.
        """
        self.reset_array()

        M = len(matrix_A)
        K = len(matrix_A[0])
        N = len(matrix_B[0])

        if M > self.rows or N > self.cols:
            raise ValueError(f"Matrix size requirements (M={M}, N={N}) exceed systolic array dimensions ({self.rows}x{self.cols})")
        if len(matrix_B) != K:
            raise ValueError("Incompatible matrix dimensions.")

        # Compute cycles for computation wave
        compute_cycles = M + N + K - 1

        # 1. Step cycle-by-cycle for computation
        for cycle in range(compute_cycles):
            self.cycles += 1

            # Feed inputs (A) into left boundaries
            # At cycle t, row r (where 0 <= r < M) receives A[r][k] where k = t - r.
            for r in range(M):
                k = cycle - r
                if 0 <= k < K:
                    val_a = matrix_A[r][k]
                    self.grid[r][0].in_x = val_a
                    if val_a != 0.0:
                        self.sram_reads += 1
                else:
                    self.grid[r][0].in_x = 0.0

            # Feed weights (B) into top boundaries
            # At cycle t, column c (where 0 <= c < N) receives B[k][c] where k = t - c.
            for c in range(N):
                k = cycle - c
                if 0 <= k < K:
                    val_b = matrix_B[k][c]
                    self.grid[0][c].in_w = val_b
                    if val_b != 0.0:
                        self.sram_reads += 1
                else:
                    self.grid[0][c].in_w = 0.0

            # Local PEs execute MAC: Accumulator += X_in * W_in
            for r in range(M):
                for c in range(N):
                    pe = self.grid[r][c]
                    pe.accumulator += pe.in_x * pe.in_w
                    pe.out_x = pe.in_x
                    pe.out_w = pe.in_w
                    if pe.in_x != 0.0 or pe.in_w != 0.0:
                        pe.mac_count += 1

            # Shift inputs left-to-right
            for r in range(M):
                for c in range(self.cols - 1, 0, -1):
                    self.grid[r][c].in_x = self.grid[r][c-1].out_x
                    if self.grid[r][c-1].out_x != 0.0:
                        self.grid[r][c].hop_count += 1

            # Shift weights top-to-bottom
            for c in range(N):
                for r in range(self.rows - 1, 0, -1):
                    self.grid[r][c].in_w = self.grid[r-1][c].out_w
                    if self.grid[r-1][c].out_w != 0.0:
                        self.grid[r][c].hop_count += 1

        # 2. Readout Phase: Shift out stationary accumulators down columns to SRAM
        # This takes M cycles.
        output_matrix = [[0.0] * N for _ in range(M)]

        for rc in range(M):
            self.cycles += 1
            # In each readout cycle, values at the bottom of active rows (row M-1) are written to SRAM.
            for c in range(N):
                output_matrix[M - 1 - rc][c] = self.grid[M - 1][c].accumulator
                self.sram_writes += 1

            # Shift accumulators down
            for c in range(N):
                for r in range(M - 1, 0, -1):
                    self.grid[r][c].accumulator = self.grid[r-1][c].accumulator
                    self.grid[r][c].hop_count += 1

        return output_matrix

    def get_energy_metrics(self):
        """
        Computes energy proxies for current simulation run.
        """
        total_macs = sum(pe.mac_count for r in range(self.rows) for pe in self.grid[r])
        total_hops = sum(pe.hop_count for r in range(self.rows) for pe in self.grid[r])

        energy_mac = total_macs * self.E_MAC
        energy_sram_read = self.sram_reads * self.E_SRAM_READ
        energy_sram_write = self.sram_writes * self.E_SRAM_WRITE
        energy_hops = total_hops * self.E_HOP

        total_energy = energy_mac + energy_sram_read + energy_sram_write + energy_hops

        return {
            "cycles": self.cycles,
            "mac_operations": total_macs,
            "interconnect_hops": total_hops,
            "sram_reads": self.sram_reads,
            "sram_writes": self.sram_writes,
            "breakdown": {
                "mac_energy": energy_mac,
                "sram_read_energy": energy_sram_read,
                "sram_write_energy": energy_sram_write,
                "interconnect_energy": energy_hops
            },
            "total_energy_proxy": total_energy
        }

    def print_ascii_grid(self, mode="weight"):
        """
        Prints an ASCII visualization of the current systolic array state.
        """
        print(f"\n--- Systolic Array Grid State ({self.rows}x{self.cols}) ---")
        for r in range(self.rows):
            row_str = "  "
            for c in range(self.cols):
                pe = self.grid[r][c]
                if mode == "weight":
                    row_str += f"[PE_{r},{c} W={pe.weight:4.1f}] ──► "
                else:
                    row_str += f"[PE_{r},{c} Acc={pe.accumulator:4.1f}] ──► "
            print(row_str[:-5])
            if r < self.rows - 1:
                col_str = "       "
                for c in range(self.cols):
                    col_str += "  │           "
                print(col_str)


def run_demo():
    print("====================================================")
    print("  Systolic Array Cycle & Energy Proxy Simulator Demo")
    print("====================================================")

    # Define simple matrices to multiply: A (3x2) * B (2x3) = C (3x3)
    A = [
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0]
    ]
    B = [
        [7.0, 8.0, 9.0],
        [1.0, 2.0, 3.0]
    ]

    print("Matrix A (3x2):")
    for r in A: print(f"  {r}")
    print("\nMatrix B (2x3):")
    for r in B: print(f"  {r}")

    sim = SystolicArraySimulator(4, 4)

    # 1. Weight-Stationary Simulation
    print("\n----------------------------------------------------")
    print("1. Running Weight-Stationary (WS) Dataflow Simulation...")
    print("----------------------------------------------------")
    res_ws = sim.simulate_weight_stationary(A, B)
    sim.print_ascii_grid(mode="weight")
    metrics_ws = sim.get_energy_metrics()

    print("\nResult C (Weight-Stationary):")
    for r in res_ws[:3]:
        print(f"  {[round(x, 1) for x in r[:3]]}")

    print("\nWS Metrics:")
    for k, v in metrics_ws.items():
        if k != "breakdown":
            print(f"  {k:20}: {v}")
        else:
            print("  Energy Breakdown:")
            for ek, ev in v.items():
                print(f"    {ek:20}: {ev}")

    # 2. Output-Stationary Simulation
    print("\n----------------------------------------------------")
    print("2. Running Output-Stationary (OS) Dataflow Simulation...")
    print("----------------------------------------------------")
    res_os = sim.simulate_output_stationary(A, B)
    sim.print_ascii_grid(mode="acc")
    metrics_os = sim.get_energy_metrics()

    print("\nResult C (Output-Stationary):")
    for r in res_os[:3]:
        print(f"  {[round(x, 1) for x in r[:3]]}")

    print("\nOS Metrics:")
    for k, v in metrics_os.items():
        if k != "breakdown":
            print(f"  {k:20}: {v}")
        else:
            print("  Energy Breakdown:")
            for ek, ev in v.items():
                print(f"    {ek:20}: {ev}")

    print("\n----------------------------------------------------")
    print("Architectural Synthesis Comparison:")
    print("----------------------------------------------------")
    ratio = metrics_ws["total_energy_proxy"] / metrics_os["total_energy_proxy"]
    print(f"  WS Energy Proxy : {metrics_ws['total_energy_proxy']:.1f}")
    print(f"  OS Energy Proxy : {metrics_os['total_energy_proxy']:.1f}")
    if ratio < 1.0:
        print(f"  Weight-Stationary is {1/ratio:.2f}x more energy efficient for this workload configuration.")
    else:
        print(f"  Output-Stationary is {ratio:.2f}x more energy efficient for this workload configuration.")


if __name__ == "__main__":
    run_demo()
