#!/usr/bin/env python3
"""
Capability-Based Memory Protection Emulator
Simulates hardware-enforced capabilities, tagged memory, bounds-checking, and domain transitions.
"""

class CapabilityException(Exception):
    """Base exception for capability CPU hardware violations."""
    pass

class BoundsException(CapabilityException):
    """Raised when memory access exceeds capability limit."""
    pass

class PermissionException(CapabilityException):
    """Raised when access violating permission rights occurs."""
    pass

class TagException(CapabilityException):
    """Raised when attempting to use a raw data word as a capability."""
    pass


class Word:
    """Base memory word."""
    pass

class DataWord(Word):
    """A data word holding plain numerical or string values (tag bit = 0)."""
    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return f"Data({self.value})"


class CapabilityWord(Word):
    """
    A capability word holding bounded permissions to memory (tag bit = 1).
    This represents an unforgeable descriptor in hardware.
    """
    def __init__(self, base: int, limit: int, permissions: set, sealed: bool = False, label: str = ""):
        self.base = base
        self.limit = limit          # range is [base, base + limit)
        self.permissions = permissions  # set of 'R', 'W', 'X'
        self.sealed = sealed        # if sealed, cannot be read or modified, only called
        self.label = label

    def __repr__(self):
        seal_str = " (SEALED)" if self.sealed else ""
        perms = "".join(sorted(list(self.permissions)))
        return f"Cap(base={self.base}, limit={self.limit}, perms={perms}{seal_str}, label='{self.label}')"


class RevocableCapabilityWord(CapabilityWord):
    """
    An advanced capability that can be dynamically revoked by a parent domain
    via an associated gate identifier.
    """
    def __init__(self, base: int, limit: int, permissions: set, gate_id: int, label: str = ""):
        super().__init__(base, limit, permissions, sealed=False, label=label)
        self.gate_id = gate_id

    def __repr__(self):
        perms = "".join(sorted(list(self.permissions)))
        return f"RevocableCap(base={self.base}, limit={self.limit}, perms={perms}, gate={self.gate_id}, label='{self.label}')"


class TaggedRAM:
    """
    Simulated memory where each address contains a Word.
    A separate hardware tag bit tracks whether each word is Data or a Capability.
    """
    def __init__(self, size=100):
        self.cells = [DataWord(0) for _ in range(size)]

    def read(self, address: int) -> Word:
        if address < 0 or address >= len(self.cells):
            raise IndexError(f"Memory access out of physical RAM bounds: {address}")
        return self.cells[address]

    def write(self, address: int, word: Word):
        if address < 0 or address >= len(self.cells):
            raise IndexError(f"Memory access out of physical RAM bounds: {address}")
        # Enforce that writing plain Data clears any previous Capability in that slot
        self.cells[address] = word


class CPU:
    """
    A virtual CPU implementing capability registers and hardware-enforced bounds checking.
    Tracks performance counters for hardware validation operations.
    """
    def __init__(self, ram: TaggedRAM):
        self.ram = ram
        # 4 Data registers (D0 - D3)
        self.data_regs = [0] * 4
        # 4 Capability registers (C0 - C3)
        # C0 is initialized as the Master Capability covering entire RAM
        self.cap_regs = [
            CapabilityWord(base=0, limit=100, permissions={'R', 'W', 'X'}, label="System Master"),
            None,
            None,
            None
        ]
        self.domain_log = []
        self.revoked_gates = set()

        # Hardware Performance Counters
        self.perf_counters = {
            "memory_reads": 0,
            "memory_writes": 0,
            "bounds_checks": 0,
            "domain_crossings": 0,
            "tag_validations": 0,
            "derivations": 0
        }

    def reset_perf_counters(self):
        """Resets hardware performance counters to zero."""
        for key in self.perf_counters:
            self.perf_counters[key] = 0

    def _validate_cap(self, cap: CapabilityWord):
        """Hardware helper to verify capability validity and revocation status."""
        self.perf_counters["tag_validations"] += 1
        if isinstance(cap, RevocableCapabilityWord) and cap.gate_id in self.revoked_gates:
            raise PermissionException(f"Permission Exception: Use of revoked capability (gate={cap.gate_id}).")

    def load_const(self, reg_idx: int, value):
        """LOAD_CONST: Load raw value into a data register."""
        self.data_regs[reg_idx] = value

    def add(self, dest_idx: int, src1_idx: int, src2_idx: int):
        """ADD: Add two data registers."""
        self.data_regs[dest_idx] = self.data_regs[src1_idx] + self.data_regs[src2_idx]

    def derive_cap(self, dest_idx: int, src_idx: int, offset: int, limit: int, perms: set):
        """
        DERIVE_CAP: Create a restricted sub-capability from an existing one.
        The CPU automatically verifies that the child range fits inside the parent.
        """
        self.perf_counters["derivations"] += 1
        self.perf_counters["bounds_checks"] += 1

        parent = self.cap_regs[src_idx]
        if not parent:
            raise TagException(f"Source register C{src_idx} is empty.")
        self._validate_cap(parent)
        if parent.sealed:
            raise PermissionException("Cannot derive from a sealed capability.")

        # Verify physical bounds fit within parent's bounds
        child_base = parent.base + offset
        if child_base < parent.base or (child_base + limit) > (parent.base + parent.limit):
            raise BoundsException(f"Derived capability range [{child_base}, {child_base+limit}) exceeds parent bounds.")

        # Verify permissions are a strict subset
        if not perms.issubset(parent.permissions):
            raise PermissionException("Derived capability cannot claim permissions not possessed by parent.")

        self.cap_regs[dest_idx] = CapabilityWord(
            base=child_base,
            limit=limit,
            permissions=perms,
            label=f"Derived from C{src_idx}"
        )

    def derive_revocable_cap(self, dest_idx: int, src_idx: int, offset: int, limit: int, perms: set, gate_id: int):
        """
        DERIVE_REVOCABLE_CAP: Create a revocable sub-capability from an existing one,
        bound to a specific revocation gate.
        """
        self.perf_counters["derivations"] += 1
        self.perf_counters["bounds_checks"] += 1

        parent = self.cap_regs[src_idx]
        if not parent:
            raise TagException(f"Source register C{src_idx} is empty.")
        self._validate_cap(parent)
        if parent.sealed:
            raise PermissionException("Cannot derive from a sealed capability.")

        child_base = parent.base + offset
        if child_base < parent.base or (child_base + limit) > (parent.base + parent.limit):
            raise BoundsException(f"Derived capability range [{child_base}, {child_base+limit}) exceeds parent bounds.")

        if not perms.issubset(parent.permissions):
            raise PermissionException("Derived capability cannot claim permissions not possessed by parent.")

        self.cap_regs[dest_idx] = RevocableCapabilityWord(
            base=child_base,
            limit=limit,
            permissions=perms,
            gate_id=gate_id,
            label=f"Revocable Derived from C{src_idx}"
        )

    def revoke_gate(self, gate_id: int):
        """REVOKE_GATE: Hardware/System mechanism to invalidate all capabilities bound to a gate."""
        self.revoked_gates.add(gate_id)

    def load_data(self, dest_data_idx: int, cap_idx: int, offset: int):
        """
        LOAD_DATA: Load data word from memory using a capability register and offset.
        The hardware automatically performs bounds and permissions checking.
        """
        self.perf_counters["bounds_checks"] += 1
        self.perf_counters["memory_reads"] += 1

        cap = self.cap_regs[cap_idx]
        if not cap:
            raise TagException(f"Register C{cap_idx} contains no capability.")
        self._validate_cap(cap)
        if cap.sealed:
            raise PermissionException("Cannot load data from a sealed capability.")
        if 'R' not in cap.permissions:
            raise PermissionException(f"Capability C{cap_idx} lacks READ permission.")

        # Bounds check
        if offset < 0 or offset >= cap.limit:
            raise BoundsException(f"OOB Read: Offset {offset} exceeds capability limit {cap.limit}.")

        address = cap.base + offset
        word = self.ram.read(address)

        if not isinstance(word, DataWord):
            raise TagException(f"Type Mismatch: Memory cell at address {address} contains a Capability. Use LOAD_CAP instead.")

        self.data_regs[dest_data_idx] = word.value

    def store_data(self, src_data_idx: int, cap_idx: int, offset: int):
        """
        STORE_DATA: Store data register value to memory using a capability and offset.
        Enforces bounds, permissions, and automatically overwrites any pre-existing capability,
        clearing the hardware tag bit for that slot.
        """
        self.perf_counters["bounds_checks"] += 1
        self.perf_counters["memory_writes"] += 1

        cap = self.cap_regs[cap_idx]
        if not cap:
            raise TagException(f"Register C{cap_idx} contains no capability.")
        self._validate_cap(cap)
        if cap.sealed:
            raise PermissionException("Cannot write data to a sealed capability.")
        if 'W' not in cap.permissions:
            raise PermissionException(f"Capability C{cap_idx} lacks WRITE permission.")

        # Bounds check
        if offset < 0 or offset >= cap.limit:
            raise BoundsException(f"OOB Write: Offset {offset} exceeds capability limit {cap.limit}.")

        address = cap.base + offset
        val = self.data_regs[src_data_idx]
        self.ram.write(address, DataWord(val))

    def load_cap(self, dest_cap_idx: int, cap_idx: int, offset: int):
        """
        LOAD_CAP: Load a Capability from memory into a capability register.
        Enforces that the loaded memory slot actually has a hardware-level Capability tag.
        """
        self.perf_counters["bounds_checks"] += 1
        self.perf_counters["memory_reads"] += 1

        cap = self.cap_regs[cap_idx]
        if not cap:
            raise TagException(f"Register C{cap_idx} contains no capability.")
        self._validate_cap(cap)
        if cap.sealed:
            raise PermissionException("Cannot load capability from a sealed capability.")
        if 'R' not in cap.permissions:
            raise PermissionException(f"Capability C{cap_idx} lacks READ permission.")

        # Bounds check
        if offset < 0 or offset >= cap.limit:
            raise BoundsException(f"OOB Capability Read: Offset {offset} exceeds limit {cap.limit}.")

        address = cap.base + offset
        word = self.ram.read(address)

        if not isinstance(word, CapabilityWord):
            raise TagException(f"Tag Exception: Memory slot at address {address} does not contain a valid Capability (Tag=0).")

        self._validate_cap(word)
        self.cap_regs[dest_cap_idx] = word

    def store_cap(self, src_cap_idx: int, cap_idx: int, offset: int):
        """
        STORE_CAP: Store a Capability from a register into memory.
        The RAM preserves the capability tag bit as 1 because it's stored via specialized instruction.
        """
        self.perf_counters["bounds_checks"] += 1
        self.perf_counters["memory_writes"] += 1

        cap = self.cap_regs[cap_idx]
        if not cap:
            raise TagException(f"Register C{cap_idx} contains no capability.")
        self._validate_cap(cap)
        if cap.sealed:
            raise PermissionException("Cannot write capability to a sealed capability.")
        if 'W' not in cap.permissions:
            raise PermissionException(f"Capability C{cap_idx} lacks WRITE permission.")

        # Bounds check
        if offset < 0 or offset >= cap.limit:
            raise BoundsException(f"OOB Capability Write: Offset {offset} exceeds limit {cap.limit}.")

        address = cap.base + offset
        src_cap = self.cap_regs[src_cap_idx]
        if not src_cap:
            raise TagException(f"Source register C{src_cap_idx} is empty.")

        self._validate_cap(src_cap)
        self.ram.write(address, src_cap)

    def print_state(self):
        """Prints the CPU register and RAM status."""
        print("\n--- CPU Register Status ---")
        for i, val in enumerate(self.data_regs):
            print(f"  D{i}: {val}")
        for i, cap in enumerate(self.cap_regs):
            print(f"  C{i}: {cap if cap else 'Empty'}")
        print("-" * 30)


# =========================================================
# Attack & Security Verification Scenarios
# =========================================================

def run_scenarios():
    print("=" * 60)
    print("CAPABILITY-BASED MEMORY SAFETY SCENARIOS")
    print("=" * 60)

    ram = TaggedRAM(100)
    cpu = CPU(ram)

    # Let's write some data using C0 (master cap) to set up
    # We partition RAM:
    # Addresses [10, 20) are user's buffer.
    # Addresses [20, 30) are critical system configuration data.
    cpu.load_const(0, "SYSTEM_SECURE_TOKEN_998")
    cpu.store_data(src_data_idx=0, cap_idx=0, offset=20) # Store at address 20

    # -------------------------------------------------------------
    # Scenario 1: Normal operations & Sandboxed Buffer Overflow
    # -------------------------------------------------------------
    print("\n--- Scenario 1: Sandboxing & Bounds Checking ---")

    # Derive a restricted capability for user buffer [10, 20) with R/W rights
    print("Action: Deriving user capability for addresses [10, 20) in register C1...")
    cpu.derive_cap(dest_idx=1, src_idx=0, offset=10, limit=10, perms={'R', 'W'})
    cpu.print_state()

    # Write safe data
    print("Action: Writing data within bounds (offset 2)...")
    cpu.load_const(1, 42)
    cpu.store_data(src_data_idx=1, cap_idx=1, offset=2)

    cpu.load_data(dest_data_idx=2, cap_idx=1, offset=2)
    print(f"  Successfully wrote and read back value in register D2: {cpu.data_regs[2]}")

    # Try a Buffer Overflow Attack!
    # The attacker tries to overflow C1 to overwrite the system token at address 20 (which is C1's offset 10)
    print("\nAttacker Action: Attempting to write past bounds of C1 (offset 10) to overwrite system token...")
    try:
        cpu.load_const(3, "MALICIOUS_OVERWRITE")
        cpu.store_data(src_data_idx=3, cap_idx=1, offset=10) # Out-of-bounds write!
    except BoundsException as e:
        print(f"  [SUCCESS] CPU hardware blocked buffer overflow! Exception raised: {e}")
    else:
        print("  [FAIL] Attacker successfully bypassed bounds checking!")

    # Verify that the system token is unharmed
    cpu.load_data(dest_data_idx=3, cap_idx=0, offset=20)
    print(f"  System token remains safe in memory: {cpu.data_regs[3]}")

    # -------------------------------------------------------------
    # Scenario 2: Capability Forgery Prevention
    # -------------------------------------------------------------
    print("\n--- Scenario 2: Tagged Memory & Forgery Prevention ---")

    # The attacker wants to create a fake capability that covers the entire RAM [0, 100)
    # They try to achieve this by writing numbers directly into a memory cell (using plain write),
    # and then loading that memory cell using LOAD_CAP.
    print("Attacker Action: Writing fake capability parameters to user memory cell (offset 5)...")
    cpu.load_const(0, 0) # Base
    cpu.store_data(src_data_idx=0, cap_idx=1, offset=5) # address 15

    # Try to load address 15 as a capability
    print("Attacker Action: Attempting to load fake capability from memory slot (address 15) using LOAD_CAP...")
    try:
        cpu.load_cap(dest_cap_idx=2, cap_idx=1, offset=5)
    except TagException as e:
        print(f"  [SUCCESS] CPU blocked forgery! Tag exception raised: {e}")
        print("  (Because address 15 was written with data writes, its hardware capability tag is 0.)")
    else:
        print("  [FAIL] Attacker successfully forged a capability!")

    # -------------------------------------------------------------
    # Scenario 3: Secure Cross-Domain Transitions
    # -------------------------------------------------------------
    print("\n--- Scenario 3: Domain Transitions (Microkernel Object-Calls) ---")

    # Suppose address [50, 60) houses a secure "Database Service" with private records.
    # The Database service has a private encryption key at address 50: "SECRET_KEY_12345".
    # User should NOT be able to read address 50 directly.
    # Instead, the user must invoke the Database Service, which unseals its private memory space,
    # executes a query, and returns a verified result, without leaking the private encryption key.

    # Write database private key
    cpu.load_const(0, "SECRET_KEY_12345")
    cpu.store_data(src_data_idx=0, cap_idx=0, offset=50)

    # Derive database capability
    cpu.derive_cap(dest_idx=2, src_idx=0, offset=50, limit=10, perms={'R', 'W', 'X'})
    cpu.cap_regs[2].label = "Database Service Private"

    # Seal the capability to represent an opaque service object
    cpu.cap_regs[2].sealed = True
    print(f"Created sealed capability representing secure Database Service: {cpu.cap_regs[2]}")

    # Attacker tries to read from the sealed capability directly
    print("\nAttacker Action: Trying to load data directly from the sealed capability...")
    try:
        cpu.load_data(dest_data_idx=3, cap_idx=2, offset=0)
    except PermissionException as e:
        print(f"  [SUCCESS] CPU blocked read! Exception raised: {e}")
    else:
        print("  [FAIL] Attacker read from sealed capability!")

    # How to safely invoke it?
    # We simulate a "CALL_OBJECT" system call.
    # The hardware securely unseals the capability, runs the service's designated query method,
    # and returns the result safely.
    print("\nAction: Invoking the Database Service via CALL_OBJECT...")

    # Mocking CPU domain transition logic:
    def database_service_query(user_query):
        cpu.perf_counters["domain_crossings"] += 1
        # Service runs with access to its unsealed capability
        unsealed_cap = CapabilityWord(base=50, limit=10, permissions={'R', 'W'}, label="Unsealed Database")
        # Read private key inside service domain
        db_key_address = unsealed_cap.base + 0
        db_key = ram.read(db_key_address).value
        # Process query
        result = f"Query '{user_query}' processed using Key: {db_key[:6]}..."
        return result

    # Simulate invocation
    user_query = "GET_USER_PROFILE"
    print(f"  User input query: '{user_query}'")

    # Hardware performs transition
    if cpu.cap_regs[2].sealed and cpu.cap_regs[2].label == "Database Service Private":
        result_data = database_service_query(user_query)
        cpu.load_const(3, result_data) # Load query result into D3
        print(f"  [SUCCESS] Secure transition complete! Result returned to D3: '{cpu.data_regs[3]}'")
    else:
        print("  [FAIL] Failed secure transition.")

    # -------------------------------------------------------------
    # Scenario 4: The Confused Deputy Attack & POLA Defense
    # -------------------------------------------------------------
    print("\n--- Scenario 4: Confused Deputy Attack & POLA Defense ---")

    # Setting up the system:
    # Addresses [80, 90) contains highly sensitive system-wide "billing_log".
    # Initially contains "BILL_STATUS: PAID".
    cpu.load_const(0, "BILL_STATUS: PAID")
    cpu.store_data(src_data_idx=0, cap_idx=0, offset=80)

    # Let's define the compiler deputy function
    def compiler_deputy_ambient_write(requested_address, payload):
        """Simulates an ambient authority system where deputy uses its global master privileges."""
        # The deputy has access to the full RAM via system master capability
        # The deputy compiles user payload and writes it directly to the numeric address specified by user
        print(f"  Deputy (Ambient): Compiling and writing to address {requested_address} using system master authority...")
        ram.write(requested_address, DataWord(payload))

    # The Attacker tries to trick the compiler to write malicious data into the secure billing log at address 80
    print("Attacker Action (Ambient): Asking deputy to write compilation output to address 80...")
    compiler_deputy_ambient_write(80, "MALICIOUS_OVERWRITE")
    print(f"  Result in Memory: {ram.read(80)}  ==> [VIOLATION] Secure billing log overwritten!")

    # Restore the secure status
    cpu.load_const(0, "BILL_STATUS: PAID")
    cpu.store_data(src_data_idx=0, cap_idx=0, offset=80)

    # Now we execute the POLA (Principle of Least Authority) Defense!
    def compiler_deputy_pola_write(dest_cap_idx, offset, payload):
        """Simulates a capability system: compiler requires the caller to provide a destination capability."""
        # The compiler cannot write to arbitrary addresses using its own master authority.
        # Instead, it strictly writes using the capability passed by the caller.
        print("  Deputy (POLA): Compiling and writing output utilizing the caller's supplied capability...")
        cpu.load_const(0, payload)
        # Note: the compiler writes to memory strictly via the capability supplied in dest_cap_idx
        cpu.store_data(src_data_idx=0, cap_idx=dest_cap_idx, offset=offset)

    # Attacker tries to overwrite address 80.
    # Since the attacker's only access is to their sandbox C1 [10, 20),
    # the attacker tries to specify offset 70 inside C1 (which points to physical address 10+70 = 80).
    print("\nAttacker Action (POLA): Attempting to pass user sandbox C1 with offset 70 to deputy compiler...")
    try:
        compiler_deputy_pola_write(dest_cap_idx=1, offset=70, payload="MALICIOUS_OVERWRITE")
    except BoundsException as e:
        print(f"  [SUCCESS] CPU hardware blocked the write! Exception raised: {e}")
        print("  (The deputy compiler was not confused because its write was bounded by the caller's capability C1.)")
    else:
        print("  [FAIL] Ambient deputy bypassed bounds check!")

    # Verify that the secure billing log is completely unharmed
    cpu.load_data(dest_data_idx=3, cap_idx=0, offset=80)
    print(f"  Billing log remains safe in memory: {cpu.data_regs[3]}")

    # -------------------------------------------------------------
    # Scenario 5: Fine-grained Privilege Attenuation & Revocation
    # -------------------------------------------------------------
    print("\n--- Scenario 5: Dynamic Revocation ---")

    # Parent domain creates a revocable capability for memory slot [30, 40) bound to Gate ID 404
    print("Action: Creating revocable capability for addresses [30, 40) with Gate ID 404...")
    cpu.derive_revocable_cap(dest_idx=2, src_idx=0, offset=30, limit=10, perms={'R', 'W'}, gate_id=404)
    print(f"  Generated Revocable Capability in C2: {cpu.cap_regs[2]}")

    # Pass capability to a plugin. The plugin writes data to it successfully.
    print("Action: Untrusted plugin writing value 777 to offset 1 using capability C2...")
    cpu.load_const(1, 777)
    cpu.store_data(src_data_idx=1, cap_idx=2, offset=1)

    cpu.load_data(dest_data_idx=1, cap_idx=2, offset=1)
    print(f"  Plugin verified write: read back value {cpu.data_regs[1]} via C2.")

    # Now the parent domain revokes Gate ID 404
    print("\nParent Action: Revoking access gate 404...")
    cpu.revoke_gate(404)

    # Plugin attempts to read again using capability C2
    print("Plugin Action: Attempting to read from C2 after revocation...")
    try:
        cpu.load_data(dest_data_idx=1, cap_idx=2, offset=1)
    except PermissionException as e:
        print(f"  [SUCCESS] CPU blocked access to revoked capability! Exception raised: {e}")
    else:
        print("  [FAIL] Plugin read from revoked capability!")

    # -------------------------------------------------------------
    # Performance Counters Report
    # -------------------------------------------------------------
    print("\n" + "="*40)
    print("HARDWARE PERFORMANCE COUNTERS LOG")
    print("="*40)
    for counter, val in cpu.perf_counters.items():
        print(f"  {counter:<20}: {val}")
    print("="*40)
    print("All scenarios successfully completed and verified.")

if __name__ == "__main__":
    run_scenarios()
