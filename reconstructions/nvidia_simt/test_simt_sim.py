"""
Unit tests for NVIDIA SIMT Microarchitecture Simulator (simt_sim.py).
"""

import pytest
from reconstructions.nvidia_simt.simt_sim import (
    SimtWarp,
    WarpState,
    SharedMemory,
    TensorCoreEngine,
    StreamingMultiprocessor,
    UnifiedMemoryManager,
)


def test_warp_creation():
    warp = SimtWarp(warp_id=0, warp_size=32)
    assert len(warp.threads) == 32
    assert warp.num_active_lanes == 32
    assert warp.state == WarpState.READY


def test_branch_divergence_and_reconvergence():
    warp = SimtWarp(warp_id=0, warp_size=32)
    # Even lanes evaluate True, odd lanes evaluate False
    conds = [i % 2 == 0 for i in range(32)]

    # Push divergence at PC 10 with reconvergence PC 50
    warp.push_divergence(conds, reconvergence_pc=50)

    # Active mask should now be 16 even threads
    assert warp.num_active_lanes == 16
    assert len(warp.divergence_stack) == 1

    # Advance PC to reconvergence point
    warp.pc = 50
    reconverged = warp.check_reconvergence()

    assert reconverged is True
    # Now odd threads active
    assert warp.num_active_lanes == 16
    assert len(warp.divergence_stack) == 0


def test_shared_memory_bank_conflicts():
    smem = SharedMemory(num_banks=32, bank_width_bytes=4)

    # Conflict-free access: active lanes access address i * 4 (banks 0..31)
    no_conflict_addrs = [i * 4 for i in range(32)]
    mask = [True] * 32
    passes = smem.access_warp(no_conflict_addrs, mask)
    assert passes == 1
    assert smem.total_bank_conflicts == 0

    # 4-way bank conflict: lanes 0..3 access addresses 0, 128, 256, 384 (all map to bank 0!)
    conflict_addrs = [0, 128, 256, 384] + [i * 4 for i in range(4, 32)]
    passes = smem.access_warp(conflict_addrs, mask)
    assert passes == 4
    assert smem.total_bank_conflicts == 3


def test_shared_memory_broadcast():
    smem = SharedMemory(num_banks=32, bank_width_bytes=4)
    # Broadcast access: all 32 lanes access address 0 (bank 0)
    broadcast_addrs = [0] * 32
    mask = [True] * 32
    passes = smem.access_warp(broadcast_addrs, mask)
    # Broadcast is handled in a single pass without conflict!
    assert passes == 1
    assert smem.total_bank_conflicts == 0


def test_tensor_core_wmma_4x4x4():
    tc = TensorCoreEngine()
    warp = SimtWarp(0, 32)

    mat_a = [
        [1.0, 2.0, 0.0, 0.0],
        [0.0, 1.0, 3.0, 0.0],
        [0.0, 0.0, 1.0, 1.0],
        [2.0, 0.0, 0.0, 1.0],
    ]
    mat_b = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    mat_c = [[0.0] * 4 for _ in range(4)]

    res = tc.execute_wmma_4x4x4(warp, mat_a, mat_b, mat_c)
    assert res == mat_a
    assert tc.wmma_instructions_executed == 1


def test_sm_warp_scheduler_latency_hiding():
    sm = StreamingMultiprocessor(num_warps=2, warp_size=32)

    # Warp 0 issues long memory instruction and stalls for 3 cycles
    def warp0_inst(w: SimtWarp, sm_ref: StreamingMultiprocessor):
        w.state = WarpState.STALLED_MEMORY
        w.stall_cycles_remaining = 3

    def warp1_inst(w: SimtWarp, sm_ref: StreamingMultiprocessor):
        w.pc += 1
        if w.pc >= 3:
            w.state = WarpState.COMPLETED

    instructions = {0: warp0_inst, 1: warp1_inst}

    # Cycle 1: Warp 0 scheduled, issues memory load & stalls
    sm.step_cycle(instructions)
    assert sm.warps[0].state == WarpState.STALLED_MEMORY

    # Cycle 2: Warp scheduler hides latency! Switches to Warp 1
    sm.step_cycle(instructions)
    assert sm.scheduled_warp_cycles == 2

    # Cycle 3: Warp 1 continues while Warp 0 is still stalled
    sm.step_cycle(instructions)
    assert sm.idle_cycles == 0


def test_unified_memory_migration():
    um = UnifiedMemoryManager(page_size_kb=4, transfer_bandwidth_gbps=32.0)

    # First access by Host: page hit (default HOST)
    lat1 = um.access_page(page_id=10, requesting_entity="HOST")
    assert lat1 == 0.0
    assert um.page_faults == 0

    # Access by Device (GPU): Page fault! Migration required
    lat2 = um.access_page(page_id=10, requesting_entity="DEVICE")
    assert lat2 > 0.0
    assert um.page_faults == 1

    # Second access by Device: Page hit!
    lat3 = um.access_page(page_id=10, requesting_entity="DEVICE")
    assert lat3 == 0.0
