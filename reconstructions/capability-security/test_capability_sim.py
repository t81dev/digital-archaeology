import pytest
from capability_sim import (
    CPU,
    TaggedRAM,
    DataWord,
    CapabilityWord,
    BoundsException,
    PermissionException,
    TagException,
    RevocableCapabilityWord,
    LispWord,
    DescriptorWord,
    DescriptorNotPresentException,
)

def test_tagged_ram_operations():
    ram = TaggedRAM(50)
    assert isinstance(ram.read(0), DataWord)

    # Basic write/read
    ram.write(10, DataWord(99))
    assert ram.read(10).value == 99

    # Cap write/read
    cap = CapabilityWord(base=10, limit=5, permissions={'R'})
    ram.write(20, cap)
    assert ram.read(20) == cap

    # Out of physical bounds read/write
    with pytest.raises(IndexError):
        ram.read(55)
    with pytest.raises(IndexError):
        ram.write(-1, DataWord(10))

def test_cpu_data_operations():
    ram = TaggedRAM(50)
    cpu = CPU(ram)

    cpu.load_const(0, 100)
    cpu.load_const(1, 150)
    cpu.add(2, 0, 1)
    assert cpu.data_regs[2] == 250

    # Store/Load using C0 (Master)
    cpu.store_data(src_data_idx=2, cap_idx=0, offset=5)
    cpu.load_data(dest_data_idx=3, cap_idx=0, offset=5)
    assert cpu.data_regs[3] == 250

def test_bounds_violations():
    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Create small sandbox capability
    cpu.derive_cap(dest_idx=1, src_idx=0, offset=10, limit=5, perms={'R', 'W'})

    # Write in bounds
    cpu.load_const(0, 77)
    cpu.store_data(src_data_idx=0, cap_idx=1, offset=2)
    assert ram.read(12).value == 77

    # Out of bounds write
    with pytest.raises(BoundsException):
        cpu.store_data(src_data_idx=0, cap_idx=1, offset=5) # offset must be < 5

    # Out of bounds read
    with pytest.raises(BoundsException):
        cpu.load_data(dest_data_idx=1, cap_idx=1, offset=-1)

def test_permission_violations():
    ram = TaggedRAM(50)
    cpu = CPU(ram)

    # C1 gets READ-ONLY capability
    cpu.derive_cap(dest_idx=1, src_idx=0, offset=10, limit=5, perms={'R'})

    cpu.load_const(0, 42)
    with pytest.raises(PermissionException):
        cpu.store_data(src_data_idx=0, cap_idx=1, offset=0) # no write permissions

def test_sealed_capabilities():
    ram = TaggedRAM(50)
    cpu = CPU(ram)

    cpu.derive_cap(dest_idx=1, src_idx=0, offset=10, limit=5, perms={'R', 'W'})
    # Seal the capability
    cpu.cap_regs[1].sealed = True

    with pytest.raises(PermissionException):
        cpu.load_data(dest_data_idx=0, cap_idx=1, offset=0)

    with pytest.raises(PermissionException):
        cpu.derive_cap(dest_idx=2, src_idx=1, offset=0, limit=2, perms={'R'})

def test_tag_and_forgery_mismatch():
    ram = TaggedRAM(50)
    cpu = CPU(ram)

    # Write raw data to a location
    cpu.load_const(0, 999)
    cpu.store_data(src_data_idx=0, cap_idx=0, offset=10)

    # Attempt to load that raw data as a capability
    with pytest.raises(TagException):
        cpu.load_cap(dest_cap_idx=1, cap_idx=0, offset=10)


# =========================================================
# Security & Performance Tests
# =========================================================

def test_performance_counters():
    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Perform a derivation
    cpu.derive_cap(dest_idx=1, src_idx=0, offset=10, limit=10, perms={'R', 'W'})
    assert cpu.perf_counters["derivations"] == 1
    assert cpu.perf_counters["bounds_checks"] == 1

    # Perform a memory write
    cpu.load_const(0, 500)
    cpu.store_data(src_data_idx=0, cap_idx=1, offset=0)
    assert cpu.perf_counters["memory_writes"] == 1
    assert cpu.perf_counters["bounds_checks"] == 2

    # Perform a memory read
    cpu.load_data(dest_data_idx=1, cap_idx=1, offset=0)
    assert cpu.perf_counters["memory_reads"] == 1
    assert cpu.perf_counters["tag_validations"] == 3  # 1 during derivation, 1 during store, 1 during read
    assert cpu.perf_counters["bounds_checks"] == 3

    # Reset and verify
    cpu.reset_perf_counters()
    assert all(val == 0 for val in cpu.perf_counters.values())


def test_confused_deputy_prevention():
    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Secret resource at 80
    cpu.load_const(0, "SECRET")
    cpu.store_data(src_data_idx=0, cap_idx=0, offset=80)

    # Attacker sandbox at [10, 20) in C1
    cpu.derive_cap(dest_idx=1, src_idx=0, offset=10, limit=10, perms={'R', 'W'})

    # Try compiler write with attacker capability passing
    # Attempting to access offset 70 (which is physical 80) inside C1 should raise BoundsException
    with pytest.raises(BoundsException):
        cpu.load_const(0, "MALICIOUS")
        cpu.store_data(src_data_idx=0, cap_idx=1, offset=70) # 10 + 70 = 80, but limit is 10!


def test_revocable_capabilities():
    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Derive revocable capability at [30, 40) bound to Gate 42
    cpu.derive_revocable_cap(dest_idx=1, src_idx=0, offset=30, limit=10, perms={'R', 'W'}, gate_id=42)
    assert isinstance(cpu.cap_regs[1], RevocableCapabilityWord)

    # Perform valid read/write
    cpu.load_const(0, 999)
    cpu.store_data(src_data_idx=0, cap_idx=1, offset=2)
    cpu.load_data(dest_data_idx=1, cap_idx=1, offset=2)
    assert cpu.data_regs[1] == 999

    # Revoke Gate 42
    cpu.revoke_gate(42)

    # Try read/write again - should fail with PermissionException
    with pytest.raises(PermissionException):
        cpu.load_data(dest_data_idx=1, cap_idx=1, offset=2)

    with pytest.raises(PermissionException):
        cpu.store_data(src_data_idx=0, cap_idx=1, offset=2)


# =========================================================
# Lisp Machine & Burroughs Descriptor Tests
# =========================================================

def test_lisp_machine_simulation():
    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # 1. Setup Lisp words in memory
    w1 = LispWord("Fixnum", 42)
    w2 = LispWord("Fixnum", 58)
    w3 = LispWord("Symbol", "HELLO")

    # Store them using system capability C0
    cpu.data_regs[0] = w1
    cpu.data_regs[1] = w2
    cpu.data_regs[2] = w3

    cpu.store_lisp_word(src_reg_idx=0, cap_idx=0, offset=10)
    cpu.store_lisp_word(src_reg_idx=1, cap_idx=0, offset=11)
    cpu.store_lisp_word(src_reg_idx=2, cap_idx=0, offset=12)

    # 2. Load them back
    cpu.load_lisp_word(dest_reg_idx=0, cap_idx=0, offset=10)
    cpu.load_lisp_word(dest_reg_idx=1, cap_idx=0, offset=11)
    cpu.load_lisp_word(dest_reg_idx=2, cap_idx=0, offset=12)

    assert isinstance(cpu.data_regs[0], LispWord)
    assert cpu.data_regs[0].value == 42
    assert cpu.data_regs[1].value == 58

    # 3. Perform Type-Checked Dynamic Lisp Addition
    cpu.lisp_add(dest_idx=3, src1_idx=0, src2_idx=1)
    assert isinstance(cpu.data_regs[3], LispWord)
    assert cpu.data_regs[3].type_tag == "Fixnum"
    assert cpu.data_regs[3].value == 100

    # 4. Try adding mismatching types (Fixnum + Symbol)
    with pytest.raises(TagException):
        cpu.lisp_add(dest_idx=3, src1_idx=0, src2_idx=2)

    # 5. Try adding a raw non-LispWord
    cpu.load_const(src1_idx := 0, 999)
    with pytest.raises(TagException):
        cpu.lisp_add(dest_idx=3, src1_idx=0, src2_idx=1)


def test_lisp_cdr_coding_traversal():
    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Store sequential list [10, 20, 30] using CDR-NEXT
    ram.write(20, LispWord("Fixnum", 10, cdr_code="CDR-NEXT"))
    ram.write(21, LispWord("Fixnum", 20, cdr_code="CDR-NEXT"))
    ram.write(22, LispWord("Fixnum", 30, cdr_code="CDR-NIL"))

    # Traverse list using C0
    vals = cpu.lisp_cdr_next_traverse(cap_idx=0, start_offset=20)
    assert vals == [10, 20, 30]


def test_burroughs_descriptor_checks():
    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Write data segment elements in memory [30, 35)
    ram.write(30, DataWord(111))
    ram.write(31, DataWord(222))
    ram.write(32, DataWord(333))

    # Setup a descriptor inside data register 0
    desc_normal = DescriptorWord(base=30, limit=5, is_present=True, read_only=False, label="ArrayBuf")
    cpu.data_regs[0] = desc_normal

    # Read via descriptor (Success)
    cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=1)
    assert cpu.data_regs[1] == 222

    # Write via descriptor (Success)
    cpu.load_const(src_data_idx := 2, 777)
    cpu.store_via_descriptor(src_data_idx=2, desc_reg_idx=0, index=2)
    assert ram.read(32).value == 777

    # Bounds Violation (Index 5 is out of bounds for limit 5)
    with pytest.raises(BoundsException):
        cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=5)

    with pytest.raises(BoundsException):
        cpu.store_via_descriptor(src_data_idx=2, desc_reg_idx=0, index=-1)

    # Read-Only Protection Violation
    desc_ro = DescriptorWord(base=30, limit=5, is_present=True, read_only=True, label="ReadOnlyBuf")
    cpu.data_regs[0] = desc_ro

    # Read RO is fine
    cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=1)
    assert cpu.data_regs[1] == 222

    # Write RO is blocked
    with pytest.raises(PermissionException):
        cpu.store_via_descriptor(src_data_idx=2, desc_reg_idx=0, index=1)

    # Virtual Memory Page Fault (Descriptor not present)
    desc_swapped = DescriptorWord(base=30, limit=5, is_present=False, read_only=False, label="SwappedArray")
    cpu.data_regs[0] = desc_swapped

    with pytest.raises(DescriptorNotPresentException):
        cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=1)

    assert cpu.perf_counters["page_faults"] == 1

    # Simulate Page-in by OS
    cpu.page_in_descriptor(desc_reg_idx=0)
    cpu.load_via_descriptor(dest_data_idx=1, desc_reg_idx=0, index=1)
    assert cpu.data_regs[1] == 222
