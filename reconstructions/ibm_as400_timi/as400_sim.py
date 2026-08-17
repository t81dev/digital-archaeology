"""
IBM AS/400 Architectural Simulator (TIMI, Single-Level Store, Object OS & DB2)

This module provides a zero-dependency, interactive reconstruction of the IBM AS/400
computational substrate:
1. Single-Level Store (SLS): Unified 64-bit virtual address space with transparent
   RAM/Disk paging and tagged pointer capabilities.
2. Technology Independent Machine Interface (TIMI): Abstract intermediate program representation
   and dynamic SLIC retranslation engine supporting CISC 48-bit and RISC 64-bit POWER backends.
3. OS/400 Typed Object Model & Authority: Library namespaces, typed system objects (*PGM, *FILE, *LIB),
   and capability-based user profile authority enforcement.
4. Integrated Database (DB2 for OS/400): Physical Files (PF) and Logical Files (LF) with Record-Level Access.
"""

from typing import Dict, List, Any, Optional, Tuple, Set


class CapabilityError(Exception):
    """Raised when a tagged pointer capability check fails."""
    pass


class AuthorityError(Exception):
    """Raised when a user profile lacks authority for an object operation."""
    pass


class SingleLevelStore:
    """
    Simulates the AS/400 Single-Level Store (SLS).
    Merges volatile RAM and persistent secondary storage into a single 64-bit flat address space.
    Addresses are page-aligned (4096 bytes per page).
    Pointers carry a 1-bit tag bit enforcing capability protection.
    """

    PAGE_SIZE = 4096

    def __init__(self, ram_capacity_pages: int = 4):
        self.ram_capacity_pages = ram_capacity_pages
        self.next_virtual_address = 0x10000  # Start address
        self.ram: Dict[int, bytearray] = {}  # Page_ID -> bytearray(PAGE_SIZE)
        self.disk: Dict[int, bytearray] = {}  # Page_ID -> bytearray(PAGE_SIZE)
        self.lru_pages: List[int] = []  # Tracking RAM eviction order
        self.page_fault_count = 0
        self.page_writeback_count = 0

    def allocate_page(self) -> int:
        """Allocates a new page in virtual address space."""
        vaddr = self.next_virtual_address
        page_id = vaddr // self.PAGE_SIZE
        self.next_virtual_address += self.PAGE_SIZE

        # Initialize empty page on disk
        self.disk[page_id] = bytearray(self.PAGE_SIZE)
        return vaddr

    def _ensure_page_in_ram(self, page_id: int):
        """Page Fault Manager: Pages missing from RAM are transparently swapped in from Disk."""
        if page_id in self.ram:
            # Touch LRU
            self.lru_pages.remove(page_id)
            self.lru_pages.append(page_id)
            return

        # Page fault occurred
        self.page_fault_count += 1

        # Evict LRU page if RAM is full
        if len(self.ram) >= self.ram_capacity_pages:
            evict_page_id = self.lru_pages.pop(0)
            # Write back evicted page to disk
            self.disk[evict_page_id] = bytearray(self.ram[evict_page_id])
            del self.ram[evict_page_id]
            self.page_writeback_count += 1

        # Load page from disk to RAM
        disk_data = self.disk.get(page_id, bytearray(self.PAGE_SIZE))
        self.ram[page_id] = bytearray(disk_data)
        self.lru_pages.append(page_id)

    def write_bytes(self, vaddr: int, data: bytes):
        """Writes raw bytes across virtual page boundaries."""
        offset = 0
        total_len = len(data)
        curr_vaddr = vaddr

        while offset < total_len:
            page_id = curr_vaddr // self.PAGE_SIZE
            page_offset = curr_vaddr % self.PAGE_SIZE
            self._ensure_page_in_ram(page_id)

            chunk_len = min(total_len - offset, self.PAGE_SIZE - page_offset)
            self.ram[page_id][page_offset:page_offset + chunk_len] = data[offset:offset + chunk_len]

            offset += chunk_len
            curr_vaddr += chunk_len

    def read_bytes(self, vaddr: int, length: int) -> bytes:
        """Reads raw bytes across virtual page boundaries."""
        res = bytearray()
        curr_vaddr = vaddr

        while len(res) < length:
            page_id = curr_vaddr // self.PAGE_SIZE
            page_offset = curr_vaddr % self.PAGE_SIZE
            self._ensure_page_in_ram(page_id)

            remaining = length - len(res)
            chunk_len = min(remaining, self.PAGE_SIZE - page_offset)
            res.extend(self.ram[page_id][page_offset:page_offset + chunk_len])

            curr_vaddr += chunk_len

        return bytes(res)


class TaggedPointer:
    """
    Capability-protected pointer.
    Hardware and microcode enforce that pointers contain a hidden 1-bit tag.
    Direct integer manipulation of a pointer clears the tag flag, making it un-dereferenceable.
    """

    def __init__(self, vaddr: int, tag_valid: bool = True):
        self.vaddr = vaddr
        self.tag_valid = tag_valid

    def tamper_with_address(self, offset: int):
        """Simulates arithmetic tampering with raw memory address."""
        self.vaddr += offset
        self.tag_valid = False  # Hardware invalidates capability tag upon user manipulation

    def dereference(self) -> int:
        if not self.tag_valid:
            raise CapabilityError(f"Hardware capability violation: Pointer at 0x{self.vaddr:016X} has invalid tag!")
        return self.vaddr


class AS400Object:
    """Base class for OS/400 typed system objects."""

    def __init__(self, name: str, obj_type: str, owner: str):
        self.name = name
        self.obj_type = obj_type  # e.g. *PGM, *FILE, *LIB, *USRPRF
        self.owner = owner
        self.authorities: Dict[str, Set[str]] = {
            owner: {"*READ", "*ADD", "*UPD", "*DLT", "*EXECUTE", "*ALL"}
        }
        self.vaddr: Optional[int] = None

    def grant_authority(self, user: str, auth: str):
        if user not in self.authorities:
            self.authorities[user] = set()
        self.authorities[user].add(auth)

    def check_authority(self, user: str, required_auth: str):
        if user == "QSECOFR":  # Security Officer has root/unconditional authority
            return
        user_auths = self.authorities.get(user, set())
        if "*ALL" in user_auths or required_auth in user_auths:
            return
        raise AuthorityError(f"User '{user}' lacks '{required_auth}' authority on object '{self.name}' ({self.obj_type})")


class UserProfile(AS400Object):
    """Represents an OS/400 *USRPRF object."""

    def __init__(self, username: str, is_special_auth: bool = False):
        super().__init__(username, "*USRPRF", "QSECOFR")
        self.username = username
        self.is_special_auth = is_special_auth


class Library(AS400Object):
    """Represents an OS/400 *LIB object container."""

    def __init__(self, name: str, owner: str):
        super().__init__(name, "*LIB", owner)
        self.contents: Dict[Tuple[str, str], AS400Object] = {}  # (Name, Type) -> Object

    def add_object(self, obj: AS400Object):
        self.contents[(obj.name, obj.obj_type)] = obj

    def get_object(self, name: str, obj_type: str) -> AS400Object:
        key = (name, obj_type)
        if key not in self.contents:
            raise KeyError(f"Object '{name}' of type '{obj_type}' not found in library '{self.name}'")
        return self.contents[key]


class PhysicalFile(AS400Object):
    """Represents an OS/400 DB2 Physical File (*FILE PF)."""

    def __init__(self, name: str, owner: str, field_names: List[str], primary_key: str):
        super().__init__(name, "*FILE", owner)
        self.file_type = "PF"
        self.field_names = field_names
        self.primary_key = primary_key
        self.records: List[Dict[str, Any]] = []

    def write_record(self, user: str, record: Dict[str, Any]):
        self.check_authority(user, "*ADD")
        self.records.append(record)

    def read_records(self, user: str) -> List[Dict[str, Any]]:
        self.check_authority(user, "*READ")
        return self.records


class LogicalFile(AS400Object):
    """
    Represents an OS/400 DB2 Logical File (*FILE LF).
    Acts as a filtered/indexed view over a PhysicalFile.
    """

    def __init__(self, name: str, owner: str, physical_file: PhysicalFile, filter_field: str, filter_val: Any):
        super().__init__(name, "*FILE", owner)
        self.file_type = "LF"
        self.physical_file = physical_file
        self.filter_field = filter_field
        self.filter_val = filter_val

    def read_records(self, user: str) -> List[Dict[str, Any]]:
        self.check_authority(user, "*READ")
        raw_records = self.physical_file.read_records(user)
        return [r for r in raw_records if r.get(self.filter_field) == self.filter_val]


class TIMIInstruction:
    """Abstract instruction representation in TIMI."""

    def __init__(self, opcode: str, operands: List[Any]):
        self.opcode = opcode  # e.g., ADDN, SUBN, FETCH_REC, PRINT_MSG
        self.operands = operands

    def __repr__(self):
        return f"{self.opcode} {', '.join(map(str, self.operands))}"


class ProgramObject(AS400Object):
    """
    Represents an OS/400 *PGM object.
    Contains:
    - Abstract TIMI code instructions (Hardware-Independent)
    - Compiled Native Executable section (CISC or RISC assembly stream)
    - Target CPU architecture metadata
    """

    def __init__(self, name: str, owner: str, timi_instructions: List[TIMIInstruction]):
        super().__init__(name, "*PGM", owner)
        self.timi_instructions = timi_instructions
        self.compiled_arch: Optional[str] = None
        self.native_code: List[str] = []

    def compile_to_native(self, target_arch: str):
        """
        Simulates SLIC Microcode Compiler translating abstract TIMI to physical assembly.
        Supported backends: 'CISC_48BIT' and 'RISC_64BIT_POWER'.
        """
        self.compiled_arch = target_arch
        self.native_code = []

        if target_arch == "CISC_48BIT":
            self.native_code.append("; --- SLIC Translator output for 48-bit IMPI CISC ---")
            for inst in self.timi_instructions:
                if inst.opcode == "ADDN":
                    self.native_code.append(f"IMPI_ADD48 {inst.operands[0]}, {inst.operands[1]} -> {inst.operands[2]}")
                elif inst.opcode == "FETCH_REC":
                    self.native_code.append(f"IMPI_SLS_FETCH {inst.operands[0]}, {inst.operands[1]}")
                elif inst.opcode == "PRINT_MSG":
                    self.native_code.append(f"IMPI_5250_DISP {inst.operands[0]}")
        elif target_arch == "RISC_64BIT_POWER":
            self.native_code.append("; --- SLIC Translator output for 64-bit PowerPC AS RISC ---")
            self.native_code.append("std r31, -8(r1) ; Save link reg")
            for inst in self.timi_instructions:
                if inst.opcode == "ADDN":
                    self.native_code.append(f"add r3, r4, r5 ; TIMI ADDN ({inst.operands[0]} + {inst.operands[1]})")
                elif inst.opcode == "FETCH_REC":
                    self.native_code.append(f"ld r10, 0(r20) ; TIMI FETCH_REC {inst.operands[0]}")
                elif inst.opcode == "PRINT_MSG":
                    self.native_code.append(f"bl sys_print_5250 ; TIMI PRINT_MSG")
            self.native_code.append("ld r31, -8(r1) ; Restore link reg")
        else:
            raise ValueError(f"Unknown target architecture: {target_arch}")


class SystemEnvironment:
    """
    Top-Level AS/400 System Environment.
    Manages Single-Level Store, Libraries, Jobs, Subsystems, and Host CPU execution context.
    """

    def __init__(self, host_cpu_arch: str = "CISC_48BIT"):
        self.sls = SingleLevelStore(ram_capacity_pages=4)
        self.host_cpu_arch = host_cpu_arch
        self.libraries: Dict[str, Library] = {}
        self.system_retranslations = 0

        # Initialize core system library QGPL (General Purpose Library)
        qgpl = Library("QGPL", "QSECOFR")
        self.libraries["QGPL"] = qgpl

    def set_host_cpu_arch(self, new_arch: str):
        """Simulates physical hardware upgrade (e.g. CISC to RISC migration)."""
        self.host_cpu_arch = new_arch

    def resolve_object(self, lib_name: str, obj_name: str, obj_type: str) -> AS400Object:
        if lib_name not in self.libraries:
            raise KeyError(f"Library '{lib_name}' not found")
        return self.libraries[lib_name].get_object(obj_name, obj_type)

    def execute_program(self, current_user: str, lib_name: str, pgm_name: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Executes a *PGM object.
        If the program's compiled native architecture does not match the current host CPU,
        SLIC automatically performs a TIMI retranslation event before execution!
        """
        pgm = self.resolve_object(lib_name, pgm_name, "*PGM")
        assert isinstance(pgm, ProgramObject)

        # Check authority
        pgm.check_authority(current_user, "*EXECUTE")

        # Check if retranslation is required
        if pgm.compiled_arch != self.host_cpu_arch:
            pgm.compile_to_native(self.host_cpu_arch)
            self.system_retranslations += 1

        # Simulate execution output
        output_log = []
        for inst in pgm.timi_instructions:
            if inst.opcode == "PRINT_MSG":
                output_log.append(f"[5250 DISPLAY]: {inst.operands[0]}")
            elif inst.opcode == "ADDN":
                val1 = context.get(inst.operands[0], 0) if context else 0
                val2 = context.get(inst.operands[1], 0) if context else 0
                res = val1 + val2
                if context is not None:
                    context[inst.operands[2]] = res
                output_log.append(f"[COMPUTE]: {inst.operands[0]} ({val1}) + {inst.operands[1]} ({val2}) = {res}")

        return output_log
