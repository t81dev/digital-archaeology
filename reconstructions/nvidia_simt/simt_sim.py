"""
NVIDIA SIMT Microarchitecture Simulator (SIMT-Sim)

A zero-dependency Python simulator modeling key computational abstractions of
NVIDIA's Single Instruction, Multiple Threads (SIMT) execution architecture:
1. Warp-level lockstep execution across SIMT lanes (32 threads per warp).
2. Dynamic branch divergence & re-convergence via execution mask stacks.
3. Warp scheduling & occupancy latency hiding across Streaming Multiprocessors (SMs).
4. Shared Memory bank conflicts & address mapping (32 memory banks).
5. Warp Matrix Multiply-Accumulate (WMMA) Tensor Core operations.
6. Host-Device memory transfers and Unified Memory page migration modeling.
"""

from typing import List, Dict, Tuple, Optional, Any, Callable
import enum


class WarpState(enum.Enum):
    READY = "READY"
    STALLED_MEMORY = "STALLED_MEMORY"
    STALLED_PIPELINE = "STALLED_PIPELINE"
    COMPLETED = "COMPLETED"


class SimtThread:
    """Represents a single SIMT thread inside a warp."""
    def __init__(self, thread_id: int, lane_id: int):
        self.thread_id = thread_id
        self.lane_id = lane_id
        self.registers: Dict[str, Any] = {}
        self.active: bool = True


class MaskStackEntry:
    """Represents an entry on the SIMT execution divergence stack."""
    def __init__(self, mask: List[bool], reconvergence_pc: int):
        self.mask = mask
        self.reconvergence_pc = reconvergence_pc


class SimtWarp:
    """
    Represents a warp of SIMT threads (default 32 lanes) executing in lockstep.
    """
    def __init__(self, warp_id: int, warp_size: int = 32):
        self.warp_id = warp_id
        self.warp_size = warp_size
        self.threads: List[SimtThread] = [
            SimtThread(thread_id=warp_id * warp_size + i, lane_id=i)
            for i in range(warp_size)
        ]
        self.pc: int = 0
        self.state: WarpState = WarpState.READY
        self.active_mask: List[bool] = [True] * warp_size
        self.divergence_stack: List[MaskStackEntry] = []
        self.stall_cycles_remaining: int = 0
        self.total_cycles_executed: int = 0
        self.diverged_cycles: int = 0

    @property
    def num_active_lanes(self) -> int:
        return sum(1 for m in self.active_mask if m)

    def push_divergence(self, condition_results: List[bool], reconvergence_pc: int):
        """
        Handles branch divergence across SIMT lanes.
        Pushes untaken path onto stack, sets active mask for taken path.
        """
        taken_mask = [m and cond for m, cond in zip(self.active_mask, condition_results)]
        untaken_mask = [m and not cond for m, cond in zip(self.active_mask, condition_results)]

        has_taken = any(taken_mask)
        has_untaken = any(untaken_mask)

        if has_taken and has_untaken:
            # Divergence occurred!
            # Push untaken path to stack for execution after taken path completes
            self.divergence_stack.append(MaskStackEntry(untaken_mask, reconvergence_pc))
            self.active_mask = taken_mask
            self.diverged_cycles += 1
        elif has_taken:
            self.active_mask = taken_mask
        elif has_untaken:
            self.active_mask = untaken_mask
        else:
            self.active_mask = [False] * self.warp_size

    def check_reconvergence(self) -> bool:
        """
        Checks if current PC has reached reconvergence point on top of divergence stack.
        """
        if self.divergence_stack and self.pc == self.divergence_stack[-1].reconvergence_pc:
            entry = self.divergence_stack.pop()
            self.active_mask = entry.mask
            return True
        return False


class SharedMemory:
    """
    Models NVIDIA GPU Shared Memory with 32 banks (4-byte bank width).
    Detects bank conflicts when multiple active threads access distinct addresses in the same bank.
    """
    def __init__(self, num_banks: int = 32, bank_width_bytes: int = 4):
        self.num_banks = num_banks
        self.bank_width_bytes = bank_width_bytes
        self.memory = bytearray(num_banks * 1024)  # Default 32 KB
        self.total_accesses = 0
        self.total_bank_conflicts = 0

    def get_bank(self, address: int) -> int:
        return (address // self.bank_width_bytes) % self.num_banks

    def access_warp(self, addresses: List[int], active_mask: List[bool]) -> int:
        """
        Simulates shared memory access for a warp.
        Returns the number of serialized clock passes required to fulfill requests.
        """
        self.total_accesses += 1
        bank_requests: Dict[int, set] = {}

        for lane_id, (addr, active) in enumerate(zip(addresses, active_mask)):
            if not active or addr < 0:
                continue
            bank = self.get_bank(addr)
            if bank not in bank_requests:
                bank_requests[bank] = set()
            # Shared memory broadcast: same address to same bank causes no conflict!
            bank_requests[bank].add(addr)

        # Max address conflicts per bank determines serialization cycles
        max_conflicts = 1
        for bank, addr_set in bank_requests.items():
            conflicts = len(addr_set)
            if conflicts > max_conflicts:
                max_conflicts = conflicts

        if max_conflicts > 1:
            self.total_bank_conflicts += (max_conflicts - 1)

        return max_conflicts


class TensorCoreEngine:
    """
    Simulates Tensor Core Warp Matrix Multiply-Accumulate (WMMA) execution.
    Executes a 4x4x4 mixed-precision matrix multiplication D = A * B + C
    across a 32-thread warp in a single micro-op.
    """
    def __init__(self):
        self.wmma_instructions_executed = 0

    def execute_wmma_4x4x4(
        self,
        warp: SimtWarp,
        matrix_a: List[List[float]], # 4x4 FP16
        matrix_b: List[List[float]], # 4x4 FP16
        matrix_c: List[List[float]]  # 4x4 FP32
    ) -> List[List[float]]:
        """
        Simulates Tensor Core 4x4x4 matrix multiply-accumulate across warp lanes.
        """
        self.wmma_instructions_executed += 1
        result = [[0.0 for _ in range(4)] for _ in range(4)]

        for i in range(4):
            for j in range(4):
                acc = matrix_c[i][j]
                for k in range(4):
                    acc += matrix_a[i][k] * matrix_b[k][j]
                result[i][j] = acc

        return result


class StreamingMultiprocessor:
    """
    Models an NVIDIA Streaming Multiprocessor (SM) executing a pool of warps.
    Includes warp scheduler, execution units, and shared memory.
    """
    def __init__(self, sm_id: int = 0, num_warps: int = 8, warp_size: int = 32):
        self.sm_id = sm_id
        self.num_warps = num_warps
        self.warp_size = warp_size
        self.warps: List[SimtWarp] = [SimtWarp(i, warp_size) for i in range(num_warps)]
        self.shared_memory = SharedMemory()
        self.tensor_core = TensorCoreEngine()
        self.current_cycle = 0
        self.scheduled_warp_cycles = 0
        self.idle_cycles = 0

    @property
    def occupancy(self) -> float:
        """Percentage of active warps relative to SM capacity."""
        active_warps = sum(1 for w in self.warps if w.state != WarpState.COMPLETED)
        return active_warps / self.num_warps

    def step_cycle(self, instructions_per_warp: Dict[int, Callable[[SimtWarp, 'StreamingMultiprocessor'], None]]) -> bool:
        """
        Advances the SM execution by 1 clock cycle.
        Uses greedy warp scheduling: selects the first READY warp to issue an instruction.
        """
        self.current_cycle += 1

        # Decrement stalls for all waiting warps
        for warp in self.warps:
            if warp.state in (WarpState.STALLED_MEMORY, WarpState.STALLED_PIPELINE):
                warp.stall_cycles_remaining -= 1
                if warp.stall_cycles_remaining <= 0:
                    warp.state = WarpState.READY

        # Select a READY warp (Greedy Warp Scheduler)
        ready_warps = [w for w in self.warps if w.state == WarpState.READY]

        if not ready_warps:
            self.idle_cycles += 1
            return any(w.state != WarpState.COMPLETED for w in self.warps)

        selected_warp = ready_warps[0]
        self.scheduled_warp_cycles += 1
        selected_warp.total_cycles_executed += 1

        # Execute instruction for selected warp
        if selected_warp.warp_id in instructions_per_warp:
            inst_fn = instructions_per_warp[selected_warp.warp_id]
            inst_fn(selected_warp, self)

        return any(w.state != WarpState.COMPLETED for w in self.warps)


class UnifiedMemoryManager:
    """
    Models NVIDIA Unified Memory (Managed Memory) page migration between Host (CPU) and Device (GPU).
    Tracks page faults and migration latencies across PCIe / NVLink.
    """
    def __init__(self, page_size_kb: int = 4, transfer_bandwidth_gbps: float = 32.0):
        self.page_size_kb = page_size_kb
        self.transfer_bandwidth_gbps = transfer_bandwidth_gbps
        self.page_table: Dict[int, str] = {} # page_id -> "HOST" or "DEVICE"
        self.page_faults = 0
        self.transfers_bytes = 0

    def access_page(self, page_id: int, requesting_entity: str) -> float:
        """
        Accesses a page from HOST or DEVICE.
        Triggers page migration if requested entity does not own the page.
        Returns latency penalty in microseconds.
        """
        current_location = self.page_table.get(page_id, "HOST")

        if current_location == requesting_entity:
            return 0.0 # Page hit, no migration needed

        # Page fault! Migrate page
        self.page_faults += 1
        self.page_table[page_id] = requesting_entity
        bytes_transferred = self.page_size_kb * 1024
        self.transfers_bytes += bytes_transferred

        # Calculate migration time in microseconds
        latency_us = (bytes_transferred / (self.transfer_bandwidth_gbps * 1e9)) * 1e6
        return latency_us
