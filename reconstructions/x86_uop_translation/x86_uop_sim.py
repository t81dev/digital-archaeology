#!/usr/bin/env python3
"""
x86 Microcode µop Translation, CPUID Negotiation, and Address Mode Simulator.

This zero-dependency Python simulator reconstructs three fundamental Intel architectural abstractions:
1. CISC macro-instruction decoding into RISC-like micro-operations (µops) with Out-of-Order execution.
2. CPUID-based dynamic feature interrogation and runtime vector dispatching.
3. Multi-generational memory address translation (16-bit Real Mode, 32-bit Protected Mode, 64-bit Long Mode).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Tuple, Optional


class OperatingMode(Enum):
    REAL_MODE_16 = "16-bit Real Mode"
    PROTECTED_MODE_32 = "32-bit Protected Mode"
    LONG_MODE_64 = "64-bit Long Mode"


class UopType(Enum):
    NOP = "NOP"
    LOAD = "LOAD"
    STORE = "STORE"
    ALU = "ALU"
    BRANCH = "BRANCH"
    VECTOR_ALU = "VECTOR_ALU"
    SPECIAL = "SPECIAL"


@dataclass
class MicroOp:
    """Represents a single RISC-like micro-operation (µop)."""
    op_type: UopType
    mnemonic: str
    src1: Optional[str] = None
    src2: Optional[str] = None
    dest: Optional[str] = None
    immediate: Optional[int] = None
    executed: bool = False
    result: Optional[int] = None


@dataclass
class X86Instruction:
    """Represents an x86 CISC macro-instruction."""
    raw_assembly: str
    mnemonic: str
    operands: List[str]
    length_bytes: int


class MicrocodeDecoder:
    """
    Simulates the Intel P6/Core Microcode Instruction Decoder.
    Translates variable-length x86 macro-instructions into RISC µops.
    """

    def __init__(self):
        self.microcode_rom = {
            "ENTER": [
                MicroOp(UopType.STORE, "PUSH_EBP", src1="EBP", dest="[ESP]"),
                MicroOp(UopType.ALU, "MOV_EBP_ESP", src1="ESP", dest="EBP"),
                MicroOp(UopType.ALU, "SUB_ESP_IMM", src1="ESP", dest="ESP", immediate=16)
            ],
            "LEAVE": [
                MicroOp(UopType.ALU, "MOV_ESP_EBP", src1="EBP", dest="ESP"),
                MicroOp(UopType.LOAD, "POP_EBP", src1="[ESP]", dest="EBP")
            ]
        }

    def decode(self, inst: X86Instruction) -> List[MicroOp]:
        mnemonic = inst.mnemonic.upper()
        operands = [op.strip() for op in inst.operands if op.strip()]

        # Microcode ROM lookup for complex instructions
        if mnemonic in self.microcode_rom:
            return [MicroOp(u.op_type, u.mnemonic, u.src1, u.src2, u.dest, u.immediate) for u in self.microcode_rom[mnemonic]]

        # Register-to-register ALU instruction: 1 µop
        if mnemonic in ("ADD", "SUB", "AND", "OR", "XOR") and len(operands) == 2 and not any("[" in op for op in operands):
            return [MicroOp(UopType.ALU, mnemonic, src1=operands[0], src2=operands[1], dest=operands[0])]

        # Memory store/load ALU CISC instruction: e.g., ADD [EAX + 4], EBX -> 3 µops (LOAD, ALU, STORE)
        if mnemonic == "ADD" and len(operands) == 2 and "[" in operands[0]:
            mem_addr = operands[0]
            src_reg = operands[1]
            return [
                MicroOp(UopType.LOAD, "LOAD", src1=mem_addr, dest="t1"),
                MicroOp(UopType.ALU, "ADD", src1="t1", src2=src_reg, dest="t2"),
                MicroOp(UopType.STORE, "STORE", src1="t2", dest=mem_addr)
            ]

        # Register load from memory: e.g., MOV EAX, [EBX + 8] -> 1 LOAD µop
        if mnemonic == "MOV" and len(operands) == 2 and "[" in operands[1]:
            return [MicroOp(UopType.LOAD, "LOAD", src1=operands[1], dest=operands[0])]

        # Memory write from register: e.g., MOV [EBX + 8], EAX -> 1 STORE µop
        if mnemonic == "MOV" and len(operands) == 2 and "[" in operands[0]:
            return [MicroOp(UopType.STORE, "STORE", src1=operands[1], dest=operands[0])]

        # Simple Register MOV: 1 ALU/MOVE µop
        if mnemonic == "MOV" and len(operands) == 2:
            return [MicroOp(UopType.ALU, "MOV", src1=operands[1], dest=operands[0])]

        # Vector AVX instruction: e.g., VADDPS YMM1, YMM2, YMM3 -> 1 VECTOR_ALU µop
        if mnemonic in ("VADDPS", "VMULPS", "VFMADD231PS"):
            return [MicroOp(UopType.VECTOR_ALU, mnemonic, src1=operands[1], src2=operands[2] if len(operands) > 2 else None, dest=operands[0])]

        # CPUID instruction: 1 SPECIAL µop
        if mnemonic == "CPUID":
            return [MicroOp(UopType.SPECIAL, "CPUID", dest="REG_FLAGS")]

        # Default fallback: 1 NOP or Generic ALU µop
        return [MicroOp(UopType.ALU, mnemonic, src1=operands[0] if operands else None, dest=operands[0] if operands else None)]


class CPUIDFeatureEngine:
    """
    Simulates x86 CPUID feature flag discovery leaf queries.
    Allows software to interrogate hardware and select execution fastpaths.
    """

    def __init__(self, family: int = 6, model: int = 142, stepping: int = 9):
        self.family = family
        self.model = model
        self.stepping = stepping
        self.feature_flags = {
            "FPU": True,
            "MMX": True,
            "SSE": True,
            "SSE2": True,
            "SSE3": True,
            "SSSE3": True,
            "SSE4_1": True,
            "SSE4_2": True,
            "AVX": True,
            "AVX2": True,
            "AVX512F": False,
            "AMX_TILE": False,
            "VT_X": True
        }

    def set_feature(self, feature: str, supported: bool):
        self.feature_flags[feature] = supported

    def query(self, leaf: int, subleaf: int = 0) -> Dict[str, int]:
        """Simulates CPUID instruction output in EAX, EBX, ECX, EDX registers."""
        if leaf == 0:
            # Vendor ID string: "GenuineIntel"
            return {
                "EAX": 7,  # Max supported basic leaf
                "EBX": 0x756e6547,  # "Genu"
                "EDX": 0x49656e69,  # "ineI"
                "ECX": 0x6c65746e   # "ntel"
            }
        elif leaf == 1:
            # Processor Signature & Feature Flags
            eax_sig = (self.family << 8) | (self.model << 4) | self.stepping
            ecx_flags = 0
            if self.feature_flags.get("SSE3"): ecx_flags |= (1 << 0)
            if self.feature_flags.get("SSSE3"): ecx_flags |= (1 << 9)
            if self.feature_flags.get("SSE4_1"): ecx_flags |= (1 << 19)
            if self.feature_flags.get("SSE4_2"): ecx_flags |= (1 << 20)
            if self.feature_flags.get("AVX"): ecx_flags |= (1 << 28)

            edx_flags = 0
            if self.feature_flags.get("FPU"): edx_flags |= (1 << 0)
            if self.feature_flags.get("MMX"): edx_flags |= (1 << 23)
            if self.feature_flags.get("SSE"): edx_flags |= (1 << 25)
            if self.feature_flags.get("SSE2"): edx_flags |= (1 << 26)

            return {"EAX": eax_sig, "EBX": 0x00100800, "ECX": ecx_flags, "EDX": edx_flags}
        elif leaf == 7 and subleaf == 0:
            # Structured Extended Feature Flags
            ebx_flags = 0
            if self.feature_flags.get("AVX2"): ebx_flags |= (1 << 5)
            if self.feature_flags.get("AVX512F"): ebx_flags |= (1 << 16)

            edx_flags = 0
            if self.feature_flags.get("AMX_TILE"): edx_flags |= (1 << 24)

            return {"EAX": 0, "EBX": ebx_flags, "ECX": 0, "EDX": edx_flags}
        else:
            return {"EAX": 0, "EBX": 0, "ECX": 0, "EDX": 0}

    def select_vector_fastpath(self, data: List[float]) -> Dict[str, str]:
        """Exemplifies dynamic runtime dispatching based on CPUID capability."""
        leaf7 = self.query(7, 0)
        has_avx512 = bool(leaf7["EBX"] & (1 << 16))

        leaf1 = self.query(1, 0)
        has_avx2 = bool(leaf7["EBX"] & (1 << 5))
        has_avx = bool(leaf1["ECX"] & (1 << 28))

        if has_avx512:
            return {"path": "AVX-512 Fastpath", "vector_width_bits": "512", "elements_per_iter": "16"}
        elif has_avx2 or has_avx:
            return {"path": "AVX/AVX2 Fastpath", "vector_width_bits": "256", "elements_per_iter": "8"}
        elif bool(leaf1["EDX"] & (1 << 26)):
            return {"path": "SSE2 Fallback", "vector_width_bits": "128", "elements_per_iter": "4"}
        else:
            return {"path": "Scalar x87 Fallback", "vector_width_bits": "64", "elements_per_iter": "1"}


class MemoryModeTranslator:
    """
    Simulates x86 memory address translation across operating modes:
    16-bit Real Mode, 32-bit Protected Mode, and 64-bit Long Mode.
    """

    def __init__(self):
        # Segment registers
        self.cs = 0x1000
        self.ds = 0x2000
        # Global Descriptor Table (GDT) simulation for 32-bit Protected Mode
        self.gdt = {
            0x08: {"base": 0x00000000, "limit": 0xFFFFFFFF, "dpl": 0, "type": "Code32"},
            0x10: {"base": 0x00000000, "limit": 0xFFFFFFFF, "dpl": 0, "type": "Data32"},
            0x1B: {"base": 0x00400000, "limit": 0x000FFFFF, "dpl": 3, "type": "User32"}
        }

    def translate_real_mode(self, segment: int, offset: int) -> int:
        """Calculates 20-bit physical address in 16-bit Real Mode: Physical = (Segment * 16) + Offset."""
        if not (0 <= segment <= 0xFFFF and 0 <= offset <= 0xFFFF):
            raise ValueError("Segment or Offset out of 16-bit range")
        return ((segment << 4) + offset) & 0xFFFFF

    def translate_protected_mode(self, selector: int, offset: int, cpl: int = 0) -> int:
        """Translates address in 32-bit Protected Mode using GDT descriptor validation."""
        descriptor = self.gdt.get(selector)
        if not descriptor:
            raise PermissionError(f"General Protection Fault (#GP): Invalid selector 0x{selector:02X}")

        if cpl > descriptor["dpl"]:
            raise PermissionError(f"General Protection Fault (#GP): CPL {cpl} exceeds Descriptor DPL {descriptor['dpl']}")

        if offset > descriptor["limit"]:
            raise ValueError(f"Segment Limit Fault: Offset 0x{offset:X} exceeds limit 0x{descriptor['limit']:X}")

        return descriptor["base"] + offset

    def translate_long_mode(self, virtual_addr: int) -> Dict[str, int]:
        """Translates 48-bit virtual address in 64-bit Long Mode using 4-level paging (PML4)."""
        if not (0 <= virtual_addr < (1 << 48)):
            raise ValueError("Canonical 48-bit Virtual Address Fault")

        pml4_idx = (virtual_addr >> 39) & 0x1FF
        pdpt_idx = (virtual_addr >> 30) & 0x1FF
        pd_idx = (virtual_addr >> 21) & 0x1FF
        pt_idx = (virtual_addr >> 12) & 0x1FF
        offset = virtual_addr & 0xFFF

        return {
            "PML4_INDEX": pml4_idx,
            "PDPT_INDEX": pdpt_idx,
            "PD_INDEX": pd_idx,
            "PT_INDEX": pt_idx,
            "PAGE_OFFSET": offset
        }


class X86MicroarchitectureSimulator:
    """
    Integrates microcode decoding, Out-of-Order execution, CPUID negotiation,
    and multi-mode address translation.
    """

    def __init__(self):
        self.decoder = MicrocodeDecoder()
        self.cpuid_engine = CPUIDFeatureEngine()
        self.mmu = MemoryModeTranslator()
        self.registers: Dict[str, int] = {
            "EAX": 10,
            "EBX": 20,
            "ECX": 30,
            "EDX": 0,
            "ESP": 0x1000,
            "EBP": 0x1000,
            "t1": 0,
            "t2": 0
        }
        self.memory: Dict[int, int] = {0x1004: 100}

    def execute_program(self, instructions: List[X86Instruction]) -> Dict[str, List[MicroOp]]:
        """Decodes x86 instructions into µops and executes them in simulated OOO engine."""
        uop_stream: List[MicroOp] = []
        for inst in instructions:
            uops = self.decoder.decode(inst)
            uop_stream.extend(uops)

        # Simple execution pass
        for uop in uop_stream:
            if uop.op_type == UopType.LOAD:
                # Simulating load: src1 is address e.g. "[EAX + 4]"
                uop.result = self.memory.get(0x1004, 0)
                if uop.dest:
                    self.registers[uop.dest] = uop.result
                uop.executed = True
            elif uop.op_type == UopType.ALU:
                v1 = self.registers.get(uop.src1, 0) if uop.src1 in self.registers else (uop.immediate if uop.immediate is not None else 0)
                v2 = self.registers.get(uop.src2, 0) if uop.src2 in self.registers else 0
                if uop.mnemonic == "ADD":
                    uop.result = v1 + v2
                elif uop.mnemonic == "SUB_ESP_IMM":
                    uop.result = v1 - (uop.immediate or 0)
                elif uop.mnemonic in ("MOV", "MOV_EBP_ESP", "MOV_ESP_EBP"):
                    uop.result = v1
                else:
                    uop.result = v1 + v2

                if uop.dest and uop.dest in self.registers:
                    self.registers[uop.dest] = uop.result
                uop.executed = True
            elif uop.op_type == UopType.STORE:
                val = self.registers.get(uop.src1, 0)
                self.memory[0x1004] = val
                uop.result = val
                uop.executed = True
            elif uop.op_type == UopType.VECTOR_ALU:
                uop.result = 256  # 256-bit vector operation executed
                uop.executed = True
            elif uop.op_type == UopType.SPECIAL:
                res = self.cpuid_engine.query(1)
                uop.result = res["ECX"]
                uop.executed = True

        return {"uops": uop_stream, "registers": self.registers}


if __name__ == "__main__":
    print("=== x86 Microcode µop & Platform Architecture Simulator ===")
    sim = X86MicroarchitectureSimulator()

    # Sample instruction sequence
    program = [
        X86Instruction("ADD [EAX + 4], EBX", "ADD", ["[EAX + 4]", "EBX"], 4),
        X86Instruction("VADDPS YMM1, YMM2, YMM3", "VADDPS", ["YMM1", "YMM2", "YMM3"], 5),
        X86Instruction("CPUID", "CPUID", [], 2)
    ]

    res = sim.execute_program(program)
    print(f"\nDecoded {len(res['uops'])} micro-ops (µops):")
    for u in res["uops"]:
        print(f"  - [{u.op_type.value:10s}] {u.mnemonic:12s} Dest={u.dest} Src1={u.src1} Src2={u.src2} (Executed={u.executed})")

    # CPUID fastpath query
    fastpath = sim.cpuid_engine.select_vector_fastpath([1.0, 2.0, 3.0])
    print(f"\nCPUID Vector Selection: {fastpath['path']} ({fastpath['vector_width_bits']}-bit, {fastpath['elements_per_iter']} elements/iter)")

    # Memory Mode Translation
    mmu = MemoryModeTranslator()
    phys_16 = mmu.translate_real_mode(0x1000, 0x0200)
    print(f"\n16-Bit Real Mode Translation: CS=0x1000 IP=0x0200 ➔ Physical 0x{phys_16:05X}")

    phys_32 = mmu.translate_protected_mode(0x08, 0x00001000)
    print(f"32-Bit Protected Mode Translation: Selector=0x08 Offset=0x1000 ➔ Physical 0x{phys_32:08X}")

    page_64 = mmu.translate_long_mode(0x00007FFFF0001020)
    print(f"64-Bit Long Mode Page Breakdown: {page_64}")
