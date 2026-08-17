"""
Unit Tests for Solaris Core Subsystems Simulator
=================================================

Tests:
1. DTrace Dynamic Instrumentation, Probe Execution, Verification & Aggregation
2. SMF Service Dependency Resolution, Topological Boot & Auto-Restarter
3. ZFS Copy-On-Write, Merkle Tree Checksum Verification, Self-Healing & Snapshots
4. Solaris Zones Process Table Isolation & Fair Share Scheduler (FSS) Allocation
"""

import pytest
from reconstructions.solaris_subsystems.solaris_sim import (
    DTraceEngine, DTraceVerifierError,
    SMFSupervisor, SMFState,
    ZFSPoolEngine,
    ZoneSandboxEngine
)


# ============================================================================
# 1. DTrace Engine Tests
# ============================================================================

def test_dtrace_probe_registration_and_firing():
    engine = DTraceEngine()
    probe = engine.register_probe("syscall", "genunix", "open", "entry")
    assert probe.fqpn == "syscall:genunix:open:entry"
    assert not probe.enabled

    fired = []

    def action_fn(ctx, eng):
        fired.append(ctx["filename"])
        eng.aggregate_count("syscall_count", ctx["filename"])

    script_code = "syscall:::entry { @counts[arg0] = count(); }"
    engine.enable_probe_action("syscall:genunix:open:entry", lambda ctx: ctx.get("filename") is not None, action_fn, script_code)

    assert probe.enabled

    # Fire probe
    engine.fire_probe("syscall:genunix:open:entry", {"filename": "/etc/passwd"})
    assert fired == ["/etc/passwd"]
    assert engine.aggregations["syscall_count"]["/etc/passwd"] == 1


def test_dtrace_verifier_rejects_loops():
    engine = DTraceEngine()
    illegal_script = "syscall:::entry { while(1) { trace(arg0); } }"

    with pytest.raises(DTraceVerifierError) as exc_info:
        engine.enable_probe_action(
            "syscall:genunix:read:entry",
            lambda ctx: True,
            lambda ctx, eng: None,
            illegal_script
        )
    assert "Forbidden construct 'while'" in str(exc_info.value)


def test_dtrace_fault_interception():
    engine = DTraceEngine()

    def faulting_action(ctx, eng):
        # Simulate memory fault dereference
        raise MemoryError("Invalid kernel address dereference 0x0")

    script_code = "fbt::vnode_rele:entry { trace(args[0]->v_path); }"
    engine.enable_probe_action("fbt:genunix:vnode_rele:entry", lambda ctx: True, faulting_action, script_code)

    ctx = {}
    engine.fire_probe("fbt:genunix:vnode_rele:entry", ctx)

    # Verifies fault was intercepted, probe disabled, and kernel spared
    assert not engine.probes["fbt:genunix:vnode_rele:entry"].enabled
    assert "__dtrace_fault" in ctx
    assert "Invalid kernel address" in ctx["__dtrace_fault"]


# ============================================================================
# 2. SMF Service Supervisor Tests
# ============================================================================

def test_smf_dependency_and_topological_boot():
    smf = SMFSupervisor()

    # Register services with dependencies
    smf.register_service("svc:/system/filesystem/local:default", [], "mountall", "umountall")
    smf.register_service("svc:/network/physical:default", [], "netstart", "netstop")
    smf.register_service(
        "svc:/network/http:apache22",
        ["svc:/system/filesystem/local:default", "svc:/network/physical:default"],
        "apachectl start",
        "apachectl stop"
    )

    booted = smf.boot_system_topological()
    assert len(booted) == 3
    assert booted[-1] == "svc:/network/http:apache22"
    assert smf.services["svc:/network/http:apache22"].state == SMFState.ONLINE


def test_smf_auto_restarter_and_maintenance_transition():
    smf = SMFSupervisor()
    smf.register_service("svc:/application/database:db", [], "db_start", "db_stop")
    smf.start_service("svc:/application/database:db")

    # Simulate crashes up to retry limit
    for i in range(3):
        smf.notify_service_crash("svc:/application/database:db")
        assert smf.services["svc:/application/database:db"].state == SMFState.ONLINE

    # Exceed retry limit -> transition to MAINTENANCE
    smf.notify_service_crash("svc:/application/database:db")
    assert smf.services["svc:/application/database:db"].state == SMFState.MAINTENANCE


# ============================================================================
# 3. ZFS Pooled Storage & Integrity Tests
# ============================================================================

def test_zfs_cow_write_and_merkle_verification():
    pool = ZFSPoolEngine("tank", ["/dev/dsk/c0t0d0s0", "/dev/dsk/c0t1d0s0"])

    root_ptr = pool.write_dataset_file("db_data.db", "PAYLOAD_BLOCK_A")
    assert root_ptr is not None

    content, is_valid = pool.read_dataset_file(root_ptr)
    assert is_valid
    assert content == "PAYLOAD_BLOCK_A"


def test_zfs_silent_corruption_detection_and_self_healing():
    pool = ZFSPoolEngine("tank", ["/dev/dsk/c0t0d0s0"])
    root_ptr = pool.write_dataset_file("critical.dat", "ORIGINAL_DATA_CONTENT")

    leaf_ptr = root_ptr.child_pointer
    block_id = leaf_ptr.block_id

    # Corrupt block data on disk (bit rot simulation)
    pool.corrupt_block_data(block_id, "CORRUPTED_DATA_CONTENT")

    # Verification fails due to Merkle checksum mismatch
    content, is_valid = pool.read_dataset_file(root_ptr)
    assert not is_valid

    # Perform ZFS self-healing using replica
    healed = pool.self_heal_block(leaf_ptr, "ORIGINAL_DATA_CONTENT")
    assert healed

    # Verify data is now valid
    content, is_valid = pool.read_dataset_file(root_ptr)
    assert is_valid
    assert content == "ORIGINAL_DATA_CONTENT"


def test_zfs_snapshot_creation():
    pool = ZFSPoolEngine("tank", ["/dev/dsk/c0t0d0s0"])
    root_tx1 = pool.write_dataset_file("file1.txt", "VERSION_1")

    snap_id = pool.create_snapshot("snap1")
    assert snap_id == "tank@snap1"

    # Write new TX (COW updates current root, but snapshot preserves root_tx1)
    root_tx2 = pool.write_dataset_file("file1.txt", "VERSION_2")

    # Read current state
    curr_content, _ = pool.read_dataset_file(root_tx2)
    assert curr_content == "VERSION_2"

    # Read snapshot state
    snap_ptr = pool.snapshots["snap1"]
    snap_content, _ = pool.read_dataset_file(snap_ptr)
    assert snap_content == "VERSION_1"


# ============================================================================
# 4. Solaris Zones Virtualization Tests
# ============================================================================

def test_zone_process_isolation():
    engine = ZoneSandboxEngine()

    web_zone = engine.create_zone("web_zone", cpu_shares=30)
    db_zone = engine.create_zone("db_zone", cpu_shares=70)

    p_global = engine.spawn_process(0, "system_daemon")
    p_web = engine.spawn_process(web_zone, "httpd")
    p_db = engine.spawn_process(db_zone, "mysqld")

    # Global zone sees all 3 processes
    global_procs = engine.list_processes(0)
    assert len(global_procs) == 3

    # Non-global zone sees ONLY its own processes
    web_procs = engine.list_processes(web_zone)
    assert len(web_procs) == 1
    assert web_procs[0].command == "httpd"

    db_procs = engine.list_processes(db_zone)
    assert len(db_procs) == 1
    assert db_procs[0].command == "mysqld"


def test_zone_fss_cpu_quantum_allocation():
    engine = ZoneSandboxEngine()
    engine.create_zone("web", cpu_shares=30)
    engine.create_zone("db", cpu_shares=70)

    alloc = engine.allocate_fss_cpu_quantum()

    # Total shares: 100 (global) + 30 (web) + 70 (db) = 200
    # Global = 100/200 = 50%
    # Web = 30/200 = 15%
    # DB = 70/200 = 35%
    assert alloc["global"] == 50.0
    assert alloc["web"] == 15.0
    assert alloc["db"] == 35.0
