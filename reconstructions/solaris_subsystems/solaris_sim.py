"""
Solaris Core Systems Architecture Simulator
=============================================

A zero-dependency Python reconstruction of core Solaris 10+ computational subsystems:
1. DTrace Dynamic Instrumentation & DIF Verification Engine
2. SMF (Service Management Facility) Dependency Graph & Restarter Supervisor
3. ZFS Copy-on-Write Pooled Storage & Merkle Tree Integrity Engine
4. Solaris Zones (Containers) Lightweight OS Virtualization & Resource Control Engine
"""

import hashlib
import time
import dataclasses
from typing import Dict, List, Optional, Set, Tuple, Any, Callable


# ============================================================================
# 1. DTrace Dynamic Instrumentation & DIF Safety Verification Engine
# ============================================================================

@dataclasses.dataclass
class DTraceProbe:
    provider: str        # e.g., "syscall", "fbt", "sdt"
    module: str          # e.g., "genunix", "vfs"
    function: str        # e.g., "open", "read", "vnode_rele"
    name: str            # e.g., "entry", "return"
    enabled: bool = False

    @property
    def fqpn(self) -> str:
        """Fully Qualified Probe Name: provider:module:function:name."""
        return f"{self.provider}:{self.module}:{self.function}:{self.name}"


class DTraceVerifierError(Exception):
    """Raised when a DScript program fails DIF safety verification."""
    pass


class DTraceEngine:
    """
    Simulates the DTrace dynamic instrumentation infrastructure and DIF VM verifier.
    Enforces production safety rules:
    - No unbounded loops
    - Read-only supervisor memory guarantees
    - In-kernel fault interception and lockless aggregation buffers
    """
    def __init__(self):
        self.probes: Dict[str, DTraceProbe] = {}
        self.active_scripts: Dict[str, Dict[str, Any]] = {}
        # Lockless Per-CPU Aggregation Buffers: aggregation_name -> {key: numeric_value}
        self.aggregations: Dict[str, Dict[str, int]] = {}

    def register_probe(self, provider: str, module: str, function: str, name: str) -> DTraceProbe:
        probe = DTraceProbe(provider, module, function, name)
        self.probes[probe.fqpn] = probe
        return probe

    def verify_dscript(self, script_code: str) -> bool:
        """
        DIF Safety Verifier:
        Analyzes DScript bytecode/text prior to execution.
        Fails verification if script contains forbidden loop primitives or memory write actions.
        """
        forbidden_keywords = ["while", "for", "do", "goto", "write_kernel", "asm"]
        for keyword in forbidden_keywords:
            if keyword in script_code:
                raise DTraceVerifierError(
                    f"DIF Verification Failed: Forbidden construct '{keyword}' detected. "
                    "DScript must be loop-free and read-only to guarantee production safety."
                )
        return True

    def enable_probe_action(self, probe_fqpn: str, predicate: Callable[[Dict[str, Any]], bool],
                            action: Callable[[Dict[str, Any], 'DTraceEngine'], None], script_code: str):
        self.verify_dscript(script_code)

        if probe_fqpn not in self.probes:
            # Auto-create statically defined probe if not pre-registered
            parts = probe_fqpn.split(":")
            if len(parts) == 4:
                self.register_probe(parts[0], parts[1], parts[2], parts[3])
            else:
                raise ValueError(f"Invalid probe format: {probe_fqpn}")

        self.probes[probe_fqpn].enabled = True
        self.active_scripts[probe_fqpn] = {
            "predicate": predicate,
            "action": action,
            "code": script_code
        }

    def fire_probe(self, probe_fqpn: str, context: Dict[str, Any]):
        """
        Fires an in-kernel probe event. If enabled, evaluates predicate and executes DIF action.
        Includes fault interception for invalid memory dereferences.
        """
        probe = self.probes.get(probe_fqpn)
        if not probe or not probe.enabled:
            return  # Zero overhead when probe is disabled

        script = self.active_scripts.get(probe_fqpn)
        if not script:
            return

        try:
            # Evaluate predicate
            if script["predicate"](context):
                # Execute action
                script["action"](context, self)
        except Exception as e:
            # Fault Interception: Disable probe to protect kernel, record error
            probe.enabled = False
            context["__dtrace_fault"] = str(e)

    def aggregate_count(self, agg_name: str, key: str, value: int = 1):
        if agg_name not in self.aggregations:
            self.aggregations[agg_name] = {}
        self.aggregations[agg_name][key] = self.aggregations[agg_name].get(key, 0) + value


# ============================================================================
# 2. SMF (Service Management Facility) Dependency Graph & Supervisor
# ============================================================================

class SMFState:
    UNINITIALIZED = "UNINITIALIZED"
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"
    MAINTENANCE = "MAINTENANCE"
    DISABLED = "DISABLED"


@dataclasses.dataclass
class SMFService:
    fmri: str                           # e.g., "svc:/network/http:apache22"
    dependencies: List[str]             # List of required FMRIs
    start_command: str
    stop_command: str
    state: str = SMFState.UNINITIALIZED
    restarter_retries: int = 0
    max_retries: int = 3


class SMFSupervisor:
    """
    Simulates the SMF (Service Management Facility) Master Restarter (`svc.startd`).
    Evaluates declarative service dependency trees, executes topological startup,
    and performs automatic state self-healing on service crash.
    """
    def __init__(self):
        self.services: Dict[str, SMFService] = {}
        self.execution_log: List[str] = []

    def register_service(self, fmri: str, dependencies: List[str], start_cmd: str, stop_cmd: str) -> SMFService:
        service = SMFService(fmri=fmri, dependencies=dependencies, start_command=start_cmd, stop_command=stop_cmd)
        service.state = SMFState.OFFLINE
        self.services[fmri] = service
        return service

    def check_dependencies(self, fmri: str) -> bool:
        service = self.services.get(fmri)
        if not service:
            return False
        for dep_fmri in service.dependencies:
            dep_svc = self.services.get(dep_fmri)
            if not dep_svc or dep_svc.state != SMFState.ONLINE:
                return False
        return True

    def start_service(self, fmri: str) -> bool:
        service = self.services.get(fmri)
        if not service or service.state == SMFState.DISABLED:
            return False

        if not self.check_dependencies(fmri):
            service.state = SMFState.OFFLINE
            return False

        # Execute start command
        self.execution_log.append(f"EXEC: {service.start_command}")
        service.state = SMFState.ONLINE
        return True

    def boot_system_topological(self) -> List[str]:
        """
        Evaluates dependency graph and boots all eligible services in topological order.
        """
        booted = []
        progress = True
        while progress:
            progress = False
            for fmri, service in self.services.items():
                if service.state == SMFState.OFFLINE and self.check_dependencies(fmri):
                    if self.start_service(fmri):
                        booted.append(fmri)
                        progress = True
        return booted

    def notify_service_crash(self, fmri: str):
        """
        Simulates restarter process tracking catching a crash signal.
        Attempts auto-restart up to max_retries, after which it transitions to MAINTENANCE.
        """
        service = self.services.get(fmri)
        if not service:
            return

        self.execution_log.append(f"CRASH_DETECTED: {fmri}")
        service.restarter_retries += 1

        if service.restarter_retries <= service.max_retries:
            self.execution_log.append(f"RESTARTER_RETRY_{service.restarter_retries}: {fmri}")
            if not self.start_service(fmri):
                service.state = SMFState.OFFLINE
        else:
            service.state = SMFState.MAINTENANCE
            self.execution_log.append(f"TRANSITION_TO_MAINTENANCE: {fmri}")


# ============================================================================
# 3. ZFS Copy-on-Write Pooled Storage & Merkle Tree Integrity Engine
# ============================================================================

@dataclasses.dataclass
class ZFSBlockPointer:
    block_id: str
    checksum: str
    child_pointer: Optional['ZFSBlockPointer'] = None
    data_payload: Optional[str] = None


class ZFSPoolEngine:
    """
    Simulates ZFS Storage Pool Allocator (SPA), Copy-on-Write (COW) transactions,
    parent-pointer Merkle tree checksum integrity, and instantaneous snapshots.
    """
    def __init__(self, pool_name: str, devices: List[str]):
        self.pool_name = pool_name
        self.devices = devices
        # Uberblock -> Root Block Pointer
        self.root_block_pointer: Optional[ZFSBlockPointer] = None
        # Block Storage Media: block_id -> raw_data
        self.storage_media: Dict[str, str] = {}
        # Snapshots: snapshot_name -> root_block_pointer copy
        self.snapshots: Dict[str, ZFSBlockPointer] = {}
        self.transaction_id: int = 0

    def _compute_checksum(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def write_dataset_file(self, filename: str, content: str) -> ZFSBlockPointer:
        """
        Copy-On-Write (COW) Write Operation:
        Writes new data payload to unallocated block storage, then updates parent pointers up to the Uberblock.
        """
        self.transaction_id += 1
        data_block_id = f"blk_tx{self.transaction_id}_{filename}"
        checksum = self._compute_checksum(content)

        # Store raw block data
        self.storage_media[data_block_id] = content

        # Create leaf pointer
        leaf_ptr = ZFSBlockPointer(
            block_id=data_block_id,
            checksum=checksum,
            data_payload=content
        )

        # Create new root pointer (COW tree root update)
        root_data = f"dataset_root_tx{self.transaction_id}:{filename}->{data_block_id}"
        root_checksum = self._compute_checksum(root_data + checksum)

        new_root = ZFSBlockPointer(
            block_id=f"root_tx{self.transaction_id}",
            checksum=root_checksum,
            child_pointer=leaf_ptr,
            data_payload=root_data
        )

        self.root_block_pointer = new_root
        return new_root

    def read_dataset_file(self, root_ptr: Optional[ZFSBlockPointer] = None) -> Tuple[str, bool]:
        """
        Reads file and validates parent-pointer Merkle tree checksum integrity.
        Returns (content, is_valid).
        """
        ptr = root_ptr or self.root_block_pointer
        if not ptr or not ptr.child_pointer:
            return ("", False)

        leaf_ptr = ptr.child_pointer
        raw_content = self.storage_media.get(leaf_ptr.block_id, "")

        # Re-compute checksum
        computed_checksum = self._compute_checksum(raw_content)

        # Parent pointer validation
        if computed_checksum == leaf_ptr.checksum:
            return (raw_content, True)
        else:
            # Checksum Mismatch: Silent Data Corruption Detected!
            return (raw_content, False)

    def corrupt_block_data(self, block_id: str, corrupted_content: str):
        """Simulates physical disk bit-rot corruption."""
        if block_id in self.storage_media:
            self.storage_media[block_id] = corrupted_content

    def self_heal_block(self, leaf_ptr: ZFSBlockPointer, replica_content: str) -> bool:
        """
        Simulates ZFS self-healing data repair using mirror/parity replica.
        """
        repair_checksum = self._compute_checksum(replica_content)
        if repair_checksum == leaf_ptr.checksum:
            self.storage_media[leaf_ptr.block_id] = replica_content
            return True
        return False

    def create_snapshot(self, snapshot_name: str) -> str:
        """
        Creates an instantaneous O(1) read-only snapshot by saving the current root_block_pointer.
        """
        if not self.root_block_pointer:
            raise RuntimeError("Cannot snapshot empty pool")
        self.snapshots[snapshot_name] = self.root_block_pointer
        return f"{self.pool_name}@{snapshot_name}"


# ============================================================================
# 4. Solaris Zones (Containers) Virtualization & Resource Control Engine
# ============================================================================

@dataclasses.dataclass
class ZoneProcess:
    pid: int
    zone_id: int
    command: str
    cpu_shares: int


class ZoneSandboxEngine:
    """
    Simulates Solaris Zones (Containers) Lightweight OS Virtualization:
    - Global Zone vs Non-Global Zone execution
    - Process table filtering by zone_id
    - Loopback File System (lofs) virtual root paths
    - Fair Share Scheduler (FSS) resource control enforcement
    """
    def __init__(self):
        self.zones: Dict[int, str] = {0: "global"}  # zone_id -> zone_name
        self.next_zone_id: int = 1
        self.process_table: List[ZoneProcess] = []
        self.next_pid: int = 100
        # Zone Resource Limits: zone_id -> {"cpu_shares": int, "memory_cap_mb": int}
        self.resource_limits: Dict[int, Dict[str, int]] = {0: {"cpu_shares": 100, "memory_cap_mb": 8192}}
        # Virtual Filesystem Mounts: zone_id -> virtual_root_path
        self.virtual_roots: Dict[int, str] = {0: "/"}

    def create_zone(self, zone_name: str, cpu_shares: int = 10, memory_cap_mb: int = 1024) -> int:
        zone_id = self.next_zone_id
        self.next_zone_id += 1
        self.zones[zone_id] = zone_name
        self.resource_limits[zone_id] = {
            "cpu_shares": cpu_shares,
            "memory_cap_mb": memory_cap_mb
        }
        self.virtual_roots[zone_id] = f"/zones/{zone_name}/root"
        return zone_id

    def spawn_process(self, zone_id: int, command: str) -> ZoneProcess:
        if zone_id not in self.zones:
            raise ValueError(f"Zone ID {zone_id} does not exist.")

        pid = self.next_pid
        self.next_pid += 1
        proc = ZoneProcess(
            pid=pid,
            zone_id=zone_id,
            command=command,
            cpu_shares=self.resource_limits[zone_id]["cpu_shares"]
        )
        self.process_table.append(proc)
        return proc

    def list_processes(self, querying_zone_id: int) -> List[ZoneProcess]:
        """
        Enforces process visibility boundaries:
        - Global Zone (zone_id 0) can see ALL processes across all zones.
        - Non-Global Zone (zone_id > 0) can ONLY see processes belonging to its own zone_id.
        """
        if querying_zone_id == 0:
            return list(self.process_table)
        return [p for p in self.process_table if p.zone_id == querying_zone_id]

    def allocate_fss_cpu_quantum(self) -> Dict[str, float]:
        """
        Simulates Fair Share Scheduler (FSS) CPU allocation based on relative zone CPU shares.
        """
        total_shares = sum(limits["cpu_shares"] for limits in self.resource_limits.values())
        allocation = {}
        for zone_id, zone_name in self.zones.items():
            shares = self.resource_limits[zone_id]["cpu_shares"]
            allocation[zone_name] = round((shares / total_shares) * 100.0, 2)
        return allocation
