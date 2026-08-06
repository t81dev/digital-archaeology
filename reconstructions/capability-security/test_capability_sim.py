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
# New Security & Performance Tests
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
