#!/usr/bin/env python3
"""
Unit tests for x86 Microcode µop Translation and Platform Simulator.
"""

import pytest
from reconstructions.x86_uop_translation.x86_uop_sim import (
    MicrocodeDecoder,
    CPUIDFeatureEngine,
    MemoryModeTranslator,
    X86MicroarchitectureSimulator,
    X86Instruction,
    UopType
)


def test_microcode_decoder_simple_alu():
    decoder = MicrocodeDecoder()
    inst = X86Instruction("ADD EAX, EBX", "ADD", ["EAX", "EBX"], 2)
    uops = decoder.decode(inst)
    assert len(uops) == 1
    assert uops[0].op_type == UopType.ALU
    assert uops[0].mnemonic == "ADD"
    assert uops[0].dest == "EAX"


def test_microcode_decoder_cisc_memory_op():
    decoder = MicrocodeDecoder()
    inst = X86Instruction("ADD [EAX + 4], EBX", "ADD", ["[EAX + 4]", "EBX"], 4)
    uops = decoder.decode(inst)
    # Memory CISC ADD breaks into 3 µops: LOAD, ALU, STORE
    assert len(uops) == 3
    assert uops[0].op_type == UopType.LOAD
    assert uops[1].op_type == UopType.ALU
    assert uops[2].op_type == UopType.STORE


def test_microcode_decoder_enter_leave_rom():
    decoder = MicrocodeDecoder()
    inst = X86Instruction("ENTER", "ENTER", [], 4)
    uops = decoder.decode(inst)
    assert len(uops) == 3
    assert uops[0].op_type == UopType.STORE
    assert uops[1].op_type == UopType.ALU
    assert uops[2].op_type == UopType.ALU


def test_cpuid_feature_discovery():
    cpuid = CPUIDFeatureEngine()
    vendor = cpuid.query(0)
    assert vendor["EBX"] == 0x756e6547  # "Genu"

    leaf1 = cpuid.query(1)
    # Check AVX bit in ECX (bit 28)
    assert bool(leaf1["ECX"] & (1 << 28)) is True

    fastpath = cpuid.select_vector_fastpath([1.0, 2.0])
    assert "AVX" in fastpath["path"]


def test_cpuid_avx512_toggle():
    cpuid = CPUIDFeatureEngine()
    cpuid.set_feature("AVX512F", True)
    fastpath = cpuid.select_vector_fastpath([1.0, 2.0])
    assert fastpath["path"] == "AVX-512 Fastpath"
    assert fastpath["vector_width_bits"] == "512"


def test_memory_translator_real_mode():
    mmu = MemoryModeTranslator()
    # Segment 0x1000, Offset 0x0200 -> (0x1000 * 16) + 0x0200 = 0x10200
    phys = mmu.translate_real_mode(0x1000, 0x0200)
    assert phys == 0x10200


def test_memory_translator_protected_mode_permissions():
    mmu = MemoryModeTranslator()
    phys = mmu.translate_protected_mode(0x08, 0x1000, cpl=0)
    assert phys == 0x1000

    # User level attempt (CPL 3) on Kernel Descriptor (DPL 0) should raise General Protection Fault
    with pytest.raises(PermissionError):
        mmu.translate_protected_mode(0x08, 0x1000, cpl=3)


def test_memory_translator_long_mode():
    mmu = MemoryModeTranslator()
    translation = mmu.translate_long_mode(0x00007FFFF0001020)
    assert "PML4_INDEX" in translation
    assert "PAGE_OFFSET" in translation
    assert translation["PAGE_OFFSET"] == 0x020


def test_full_microarchitecture_simulator():
    sim = X86MicroarchitectureSimulator()
    program = [
        X86Instruction("ADD [EAX + 4], EBX", "ADD", ["[EAX + 4]", "EBX"], 4),
        X86Instruction("VADDPS YMM1, YMM2, YMM3", "VADDPS", ["YMM1", "YMM2", "YMM3"], 5),
        X86Instruction("CPUID", "CPUID", [], 2)
    ]
    res = sim.execute_program(program)
    assert len(res["uops"]) == 5
    assert all(u.executed for u in res["uops"])
