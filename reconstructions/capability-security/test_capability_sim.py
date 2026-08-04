import pytest
from capability_sim import (
    CPU,
    TaggedRAM,
    DataWord,
    CapabilityWord,
    BoundsException,
    PermissionException,
    TagException,
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
