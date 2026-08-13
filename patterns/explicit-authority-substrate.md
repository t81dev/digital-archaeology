# Explicit Authority Substrate

> **The pattern where a system makes authority and resource allocation explicit, unforgeable, and composable (using object-capabilities or hardware-checked descriptors), dramatically improving isolation and least-privilege security but shifting costs into compilation, development tooling, and compatibility with ambient-authority platforms.**

---

## Summary

The mainstream computing ecosystem (such as POSIX/Unix operating systems and flat virtual memory models) is built on the concept of **ambient authority**. In an ambient-authority environment, a running process inherits the full privileges of the user executing it. When a thread executes, it can access any file or memory location within its address space unless explicitly blocked by a coarse access control list (ACL). This model makes software development and operating system design simple, but makes systems highly vulnerable to buffer overflows, privilege escalation, and lateral movement.

An **Explicit Authority Substrate** is an alternative architecture that completely replaces ambient authority. In this model, processes, objects, or threads possess absolutely zero ambient authority. Instead, designation and authority are merged into unforgeable, fine-grained tokens called **capabilities** or **descriptors**. A process can only access a resource (a memory segment, a file, an I/O device, or another process) if it possesses an explicit capability token for it. Authority can be dynamically attenuated, composed, and delegated, creating a secure, self-documenting, and least-privilege computing environment.

However, this architecture shifts costs from security enforcement into programming complexity, compiler design, and developer tooling. Because standard languages (such as C or C++) and standard legacy software expect ambient authority, compiling standard applications onto an explicit authority substrate introduces significant software friction, boundary translation, and tooling gaps.

---

## Core Characteristics

An architecture implements an **Explicit Authority Substrate** when:
1.  **Merged Designation and Authority**: To reference a resource *is* to possess the authority to access it. There is no separate permission check against a global access control list (ACL).
2.  **Unforgeable Representation**: Capability tokens cannot be fabricated by user-space code. They are protected either by microkernel isolation, hardware-checked memory tags, or cryptographic bounds.
3.  **No Ambient Permissions**: An instantiated module is created with an empty resource space (a "space bank"). It has no ambient access to the host file system, network, or kernel APIs unless they are explicitly passed to it as capability handles during initialization.
4.  **Least-Authority Attenuation**: Capabilities can be dynamically restricted (e.g., converting a read-write memory capability to read-only) before being delegated to untrusted sub-modules.

---

## System Dynamics: Ambient vs. Explicit Authority

```
  [AMBIENT AUTHORITY MODEL (POSIX / Unix)]
  User Identity (e.g., root) ──► Process ──► Ambient Access to Filesystem & APIs
                                            (Coarse-grained ACL checks)

  [EXPLICIT AUTHORITY SUBSTRATE (KeyKOS / CHERI / WASI)]
  Host Kernel ──► Sandboxed Process ──► [Zero Ambient Authority]
                     │
                     ├─ (Possesses Capability A) ──► Accesses Memory Block A
                     ├─ (Possesses Capability B) ──► Invokes API B
                     └─ (No Capability for C)    ──► [PHYSICALLY BLOCKED]
```

---

## Case Studies from This Repository

*   **[KeyKOS and the Nanokernel Capability Lineage](../excavations/keykos-nanokernel-capabilities.md)** — A pioneering implementation of pure software-defined object capabilities. The [KeyKOS](../GLOSSARY.md) supervisor nanokernel managed only four primitive objects (Pages, Nodes, Domains, Meters) and routed all system activity through unforgeable, 16-byte keys. There were no user IDs, no global file paths, and no ambient permissions. [KeyKOS](../GLOSSARY.md) pioneered the **Factory pattern** for secure multi-tenant resource containment and **Meters** for hierarchical resource delegation, proving that a microkernel could enforce perfect isolation on mainframe hardware.
*   **[Capability Systems](../excavations/capability-systems.md) / [Intel iAPX 432](../excavations/intel-iapx-432.md)** — The iAPX 432 was an ambitious, hardware-enforced object-oriented capability system of the 1980s. It checked capabilities directly in the processor pipeline, but suffered from terrible performance due to complex instruction decoding and the lack of register cache optimizations, demonstrating the physical overhead of naive hardware capability checking on early silicon.
*   **[Burroughs Large Systems](../excavations/burroughs-large-systems.md)** — Introduced **descriptors** in the 1960s, checking array bounds and memory types directly in hardware. This prevented buffer overflows and enforced type-safe execution, but required writing code exclusively in high-level ALGOL variants, isolating the platform from the rising Unix/C ecosystem.
*   **[Multics](../excavations/multics.md)** — Implemented hierarchical **protection rings** (Rings 0 through 7) and segmented memory address spaces to isolate the kernel from user applications, which served as a foundational precursor to modern hardware-enforced virtual memory protection.

---

## Modern Implications

Explicit authority substrates are undergoing a spectacular revival driven by modern zero-trust security demands:
*   **The CHERI Pipeline**: CHERI (Capability Hardware Enhanced RISC Instructions) resolves the historical performance overhead of capability checking by adding 128-bit unforgeable capability registers directly to standard CPU architectures (ARM, RISC-V). This allows hardware to enforce spatial and temporal memory safety at near-zero performance cost, preventing 70%+ of typical software vulnerabilities.
*   **WebAssembly System Interface (WASI)**: WebAssembly uses an explicit authority model. A compiled Wasm module has zero access to files, networks, or env variables. Under WASI, the host must explicitly pass a directory handle or an API capability to the Wasm sandbox during instantiation, preventing unauthorized file system access or prompt-injection exploits inside multi-agent AI pipelines.
*   **Object-Capabilities in Modern Languages**: Languages like Pony or research extensions of Scala utilize object-capability patterns directly in the type system, ensuring data race freedom and secure information flow at compile time.

---

## Lessons Learned

1.  **Designation must equal permission.** Decoupling the naming of a resource from the right to access it is the root cause of ambient-authority exploits (e.g., confused deputy attacks).
2.  **Mitigate the compatibility tax.** The success of an explicit authority substrate depends heavily on the availability of automated compiler tools (like LLVM-based CHERI-Clang) that can compile legacy C/C++ code with minimal manual modification.
3.  **Resource containment requires explicit metering.** To prevent denial-of-service exploits in sandboxed environments, an explicit authority substrate must integrate resource metering (such as [KeyKOS](../GLOSSARY.md)'s Meter trees) as a first-class architectural primitive.

---

## Related Patterns

- [Interface / Conversion Tax](interface-conversion-tax.md)
- [Constraint Migration](constraint-migration.md)
- [Forgotten Abstractions](forgotten-abstractions.md)

## Related Excavations

- [KeyKOS and the Nanokernel Capability Lineage](../excavations/keykos-nanokernel-capabilities.md)
- [Capability Systems](../excavations/capability-systems.md)
- [Burroughs Large Systems](../excavations/burroughs-large-systems.md)
- [Intel iAPX 432](../excavations/intel-iapx-432.md)
- [Multics](../excavations/multics.md)

---

**Last updated**: August 24, 2026
