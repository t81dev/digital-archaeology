"""
Tests for IBM AS/400 Architectural Simulator
Verifies Single-Level Store paging/capabilities, TIMI retranslation across CISC/RISC,
OS/400 typed object security, and integrated DB2 physical/logical file operations.
"""

import pytest
from reconstructions.ibm_as400_timi.as400_sim import (
    SingleLevelStore,
    TaggedPointer,
    CapabilityError,
    AuthorityError,
    UserProfile,
    Library,
    PhysicalFile,
    LogicalFile,
    TIMIInstruction,
    ProgramObject,
    SystemEnvironment,
)


def test_single_level_store_paging_and_persistence():
    """Verify SLS transparent page fault swapping and virtual memory address mapping."""
    sls = SingleLevelStore(ram_capacity_pages=2)  # Small RAM to force paging

    vaddr1 = sls.allocate_page()
    vaddr2 = sls.allocate_page()
    vaddr3 = sls.allocate_page()

    # Write data to all 3 pages (will force eviction of page 1 to disk)
    sls.write_bytes(vaddr1, b"DATA_PAGE_1_TEST")
    sls.write_bytes(vaddr2, b"DATA_PAGE_2_TEST")
    sls.write_bytes(vaddr3, b"DATA_PAGE_3_TEST")

    assert sls.page_fault_count >= 3
    assert sls.page_writeback_count >= 1

    # Read back page 1 (forces page fault to pull from disk back into RAM)
    read_data = sls.read_bytes(vaddr1, 16)
    assert read_data == b"DATA_PAGE_1_TEST"


def test_tagged_pointer_capability_protection():
    """Verify hardware tagged pointer capability enforcement."""
    vaddr = 0x20000
    ptr = TaggedPointer(vaddr, tag_valid=True)

    # Valid pointer dereference
    assert ptr.dereference() == 0x20000

    # Simulate user pointer arithmetic tampering
    ptr.tamper_with_address(0x10)
    assert ptr.vaddr == 0x20010

    # Attempting to dereference tampered pointer raises CapabilityError
    with pytest.raises(CapabilityError):
        ptr.dereference()


def test_object_authority_security():
    """Verify OS/400 object-level authority checks."""
    owner = "PGMUSER"
    unauth_user = "EVILUSER"

    pf = PhysicalFile("PAYROLL", owner, ["EMP_ID", "SALARY"], "EMP_ID")

    # Owner has authority
    pf.write_record(owner, {"EMP_ID": 101, "SALARY": 95000})
    records = pf.read_records(owner)
    assert len(records) == 1

    # Unauthorized user gets AuthorityError
    with pytest.raises(AuthorityError):
        pf.read_records(unauth_user)

    with pytest.raises(AuthorityError):
        pf.write_record(unauth_user, {"EMP_ID": 999, "SALARY": 0})

    # Security Officer (QSECOFR) bypasses check
    qsec_records = pf.read_records("QSECOFR")
    assert len(qsec_records) == 1


def test_db2_physical_and_logical_files():
    """Verify Physical File (PF) and Logical File (LF) filtering."""
    owner = "DBA"
    pf = PhysicalFile("CUSTMAST", owner, ["CUST_ID", "NAME", "REGION"], "CUST_ID")
    pf.write_record(owner, {"CUST_ID": 1, "NAME": "Acme Corp", "REGION": "NORTH"})
    pf.write_record(owner, {"CUST_ID": 2, "NAME": "Beta Inc", "REGION": "SOUTH"})
    pf.write_record(owner, {"CUST_ID": 3, "NAME": "Gamma LLC", "REGION": "NORTH"})

    lf_north = LogicalFile("CUSTNORTH", owner, pf, "REGION", "NORTH")

    records = lf_north.read_records(owner)
    assert len(records) == 2
    assert all(r["REGION"] == "NORTH" for r in records)


def test_timi_compilation_and_cisc_to_risc_retranslation():
    """Verify automatic SLIC retranslation of TIMI binaries across CPU microarchitectures."""
    env = SystemEnvironment(host_cpu_arch="CISC_48BIT")

    # Create TIMI program instructions
    instructions = [
        TIMIInstruction("ADDN", ["VAR_A", "VAR_B", "VAR_SUM"]),
        TIMIInstruction("PRINT_MSG", ["ACCOUNTING REPORT COMPLETE"]),
    ]
    pgm = ProgramObject("ACCTPGM", "FINANCE", instructions)

    # Compile initially for CISC
    pgm.compile_to_native("CISC_48BIT")
    assert pgm.compiled_arch == "CISC_48BIT"
    assert "IMPI_ADD48" in pgm.native_code[1]

    # Add program to library
    qgpl = env.libraries["QGPL"]
    qgpl.add_object(pgm)

    # Execute on CISC host
    output = env.execute_program("FINANCE", "QGPL", "ACCTPGM", {"VAR_A": 100, "VAR_B": 250})
    assert len(output) == 2
    assert env.system_retranslations == 0

    # SIMULATE HARDWARE UPGRADE TO 64-BIT POWER RISC!
    env.set_host_cpu_arch("RISC_64BIT_POWER")

    # Execute again -> SLIC automatically detects architecture mismatch and retranslates!
    output_risc = env.execute_program("FINANCE", "QGPL", "ACCTPGM", {"VAR_A": 500, "VAR_B": 500})
    assert len(output_risc) == 2
    assert env.system_retranslations == 1
    assert pgm.compiled_arch == "RISC_64BIT_POWER"
    assert any("PowerPC" in line for line in pgm.native_code)
