# Capability Systems

> A fundamentally different approach to security and access control based on unforgeable tokens of authority rather than ambient permission checks.

---

## Summary

Capability-based security offers a powerful alternative to traditional Access Control List (ACL) and Unix-style ambient permission models. In a capability system, possessing an unforgeable reference (a “capability”) to a resource *is* the authority to use it. Capabilities tightly combine designation (“this resource”) with permission (“you may do these operations”) in a single mechanism.

Pioneered in the 1960s and implemented in several influential systems, capability architectures provide elegant solutions to persistent security problems such as privilege escalation, confused deputy attacks, and ambient authority. Despite their strengths, they have remained largely outside the mainstream operating system ecosystem.

---

## Historical Context & Primary-Source Grounding

The formal concept was introduced by **Dennis and Van Horn** in their seminal 1966 paper, "Programming Semantics for Multiprogrammed Computations," defining the capability as an unforgeable index into a per-process list of system objects (the "C-list").

Early hardware-enforced and software-mediated systems evolved through distinct generations:

### 1. Cambridge CAP Computer & Hydra (1970s)
* **CAP Computer** (University of Cambridge, Wilkes and Needham, 1979): The first computer system in which the CPU directly enforced capabilities at the hardware instruction level. It utilized separate capability segments in memory, requiring hardware-enforced descriptor loading to execute memory reads or writes.
* **Hydra** (Carnegie Mellon University, Wulf et al., 1974): A capability-based operating system designed for the C.mmp multiprocessor system. Hydra pioneered the concept of user-defined type-extension, enabling applications to declare custom resources and specify custom permissions on capabilities.

### 2. KeyKOS (1983)
* Developed by Key Systems, KeyKOS was a commercial microkernel-based OS designed for high-availability mainframe banking environments.
* **Architecture**: KeyKOS implemented a *single-level store*, mapping disk blocks and RAM into a unified, persistent address space. Objects were represented by "keys" (capabilities).
* **Mechanisms**: Disk pages themselves acted as capabilities (disc pages as objects), mediated securely by the microkernel. To handle performance constraints, KeyKOS utilized highly optimized kernel-mediated message passing (IPC). Despite having fewer than 100,000 lines of code, it demonstrated unprecedented reliability and security, achieving years of continuous uptime without security breaches.

### 3. EROS: Extremely Reliable Operating System (1999)
* Developed by Jonathan Shapiro et al. at the University of Pennsylvania, EROS modernized the KeyKOS single-level store and capability mechanisms.
* **Performance**: EROS resolved long-standing criticisms regarding capability overhead. It achieved extremely fast synchronous IPC performance—taking only ~50 clock cycles on a Pentium II, which outperformed traditional microkernels like Mach by an order of magnitude.
* **Persistence & Safety**: EROS implemented periodic, synchronous system-wide checkpointing (continuous orthogonal persistence). It provided a clean substrate for formal verification, establishing mathematical proofs of isolation and authority confinement.

```
+-----------------------------------------------------------------------+
|  TRADITIONAL POINTER / ADDRESS-BASED MODEL (AMBIENT AUTHORITY)        |
|                                                                       |
|  User Process ----> [ Address (e.g., 0x7FFF0012) ]                    |
|                            |                                          |
|                            v                                          |
|                     [ Memory Controller ]                             |
|                            |                                          |
|                            +----> Read/Write allowed based on         |
|                                   ambient process UID/GID status      |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
|  CHERI CAPABILITY-BASED MODEL (POLA ENFORCED BY HARDWARE)             |
|                                                                       |
|  User Process ----> [ CAPABILITY REGISTER: C0 ]                       |
|                     +---------------------------------------+         |
|                     | Base: 0x7FFF0000 | Limit: 0x00000100  |         |
|                     +---------------------------------------+         |
|                     | Permissions: READ, WRITE (no EXEC)    |         |
|                     +---------------------------------------+         |
|                            |                                          |
|                            v                                          |
|                     [ Memory Controller ] <---+ Hardware Tag Bit      |
|                            |                  | (1 = Unforgeable Cap  |
|                            |                  |  0 = Corrupt Data)    |
|                            v                                          |
|                     Verifies bounds & permissions                     |
|                     within instruction pipeline                       |
+-----------------------------------------------------------------------+
```

---

## Technical Overview

In a pure capability system:
- Every resource (file, device, memory segment, service, or even a procedure) is represented exclusively by a **capability** — an unforgeable token.
- Capabilities are passed explicitly between processes; they cannot be guessed or forged.
- Rights can be **attenuated** (reduced privileges) when delegating a capability.
- There are no global namespaces granting ambient authority (in contrast to Unix UIDs/GIDs, filesystem paths, or Windows ACLs).

This model naturally eliminates many classes of vulnerabilities, including the confused deputy problem. Capabilities can be implemented in software (via cryptographic tokens or kernel-mediated references) or directly in hardware.

---

## Innovations & Key Metrics

- **Principle of Least Authority (POLA)** — Enforced by architecture rather than programmer discipline.
- **Fine-grained, safe delegation** — Easy to grant temporary or limited access.
- **No ambient authority** — Dramatically reduces the attack surface.
- **Object-capability model** — Natural fit for object-oriented, distributed, and concurrent systems.
- **Strong confinement and composability** — Security boundaries are easier to reason about and verify.

---

## Why It Didn’t Win

- **Incompatibility** with dominant Unix and Windows models and the massive existing software base.
- **Ecosystem lock-in** — Applications and tools were built around ACL-style and path-based permissions.
- **Perceived performance overhead** (largely addressed in later designs such as EROS and CHERI).
- **Conceptual and cultural shift** — Capabilities felt unfamiliar compared to familiar `chmod`, file paths, or global permissions.
- **Timing** — Emerged during the rapid rise of commodity operating systems that prioritized compatibility and developer familiarity over foundational security improvements.

---

## Modern Relevance

### CHERI Hardware
- **CHERI (Capability Hardware Enhanced RISC Instructions)**: Pioneered by SRI International and the University of Cambridge (Woodruff et al., 2014; Watson et al., 2015), CHERI extends conventional RISC architectures (such as ARM and RISC-V) with native capability registers and instructions.
- **Tag-Bit Integrity**: CHERI protects capabilities in physical RAM via a hardware-managed tag bit. If a capability word in memory is overwritten by any normal integer or data-manipulation instruction, the tag bit is automatically cleared, making the capability invalid for use.
- **128-bit Compressed Capabilities**: To minimize memory bandwidth overhead, CHERI uses floating-point-style compression to compress 256-bit architectural bounds (base, limit, permissions) into a 128-bit format that fits within existing 64-bit memory spaces.
- **Performance Overhead & Memory Pressure (The Pointer Expansion Penalty)**: Extensive benchmarking on real-world workloads (e.g., PostgreSQL, nginx, WebKit) demonstrates that CHERI's hardware-enforced spatial and temporal memory safety typically incurs a low CPU cycle overhead of **1% to 5%** on the 7nm ARM Morello prototype. However, expanding pointers to 128-bit capability descriptors doubles their size in memory. In pointer-heavy workloads (such as compilers, browser engines, or interpreter runtimes), this causes a **$10\%\text{--}25\%$ memory footprint expansion**, resulting in increased L1/L2 data cache misses and higher off-chip DRAM bandwidth utilization.
- **Developer Training & Adoption Friction**: While CHERI Clang can compile standard, well-behaved C/C++ with minimal changes, adapting legacy codebases that rely on non-standard pointer arithmetic (such as XOR-linked lists, packing data bits into unused pointer bits, or custom arena allocators) requires manual refactoring. This introduces a steep developer training and engineering cost.
- **Industry Adoption & Deployment Calendar (2028--2030)**: ARM has successfully fabricated experimental CHERI silicon (the 7nm "Morello" prototype chip), demonstrating physical viability in mass-market general-purpose processors. With the active standardization of the RISC-V CHERI ISA extension, commercial deployments in secure microcontrollers, automotive platforms, and mobile application processors are anticipated within the **2028--2030 calendar horizon**. Furthermore, modern operating systems like Google's Fuchsia utilize capability-like semantics (Zircon handles), and WebAssembly employs sandboxing principles inspired directly by object-capabilities.

---

## Lessons Learned & Constraint Migration

The trajectory of capability systems highlights how changing physical and economic realities drive [Constraint Migration](../patterns/constraint-migration.md).
1. **Security as a Primary Bottleneck**: In the 1970s and 1980s, CPU cycles and memory bandwidth were scarce, making capability-checking indirection too expensive. Today, computing is virtually free, but the economic and geopolitical cost of memory-safety vulnerabilities (composing ~70% of all major CVEs) is catastrophic. The constraint has migrated from *silicon area* to *security integrity*.
2. **Ecosystem Stickiness**: Changing basic processor-level abstractions requires rewriting compilers and runtimes. Hardware-software co-design (as seen in CHERI) is essential to preserve existing C/C++ codebases while retrofitting fine-grained spatial memory protection.
3. **Selective Abstraction Distillation**: The industry has begun adopting capabilities selectively rather than wholesale, incorporating capability-based principles into hypervisors, sandboxes (Wasm), and memory tagging (ARM MTE), as discussed in [Capability-Based Security](../synthesis/capability-based-security.md).

---

## Scorecard

| Category | Rating | Rationale |
| --- | --- | --- |
| Historical Importance | ★★★★☆ | Influential in OS research |
| Technical Innovation | ★★★★★ | Foundational security model |
| Commercial Success | ★★☆☆☆ | Limited but impactful deployments |
| Modern Potential | ★★★★★ | Strong revival via hardware |
| AI Synergy | ★★☆☆☆ | Low direct synergy with neural models, but provides secure or distributed runtimes. |
| Difficulty to Recreate | ★★★★☆ | Requires extensive systems-level implementation and emulation efforts. |

## Related Excavations
- [Lisp Machines](../excavations/lisp-machines.md) (tagged architectures)
- [Burroughs Large Systems](../excavations/burroughs-large-systems.md) (descriptor-based memory safety)
- [Intel iAPX 432](../excavations/intel-iapx-432.md) (object-oriented hardware capability attempt)

## Related Patterns
- [Forgotten Abstractions](../patterns/forgotten-abstractions.md)
- [Ecosystem Lock-In](../patterns/ecosystem-lockin.md)
- [Economic Failures](../patterns/economic-failures.md)
- [Recurring Ideas](../patterns/recurring-ideas.md)
- [Constraint Migration](../patterns/constraint-migration.md)

## Related Synthesis Essays
- [Capability-Based Security](../synthesis/capability-based-security.md)

---

## Primary Sources & Further Reading

* **Dennis, J. B., & Van Horn, E. C.** (1966). "Programming Semantics for Multiprogrammed Computations." *Communications of the ACM*, 9(3), 143–155.
  - *Relevance*: The seminal publication that defined the formal concept of "capabilities" as unforgeable references to system-managed resource descriptors.
* **Hardy, N.** (1985). "The KeyKOS Architecture." *ACM SIGOPS Operating Systems Review*, 19(4), 8–25.
  - *Relevance*: Details the implementation of the microkernel-based KeyKOS operating system, demonstrating commercial viability, single-level stores, and orthogonal persistence using capabilities.
* **Shapiro, J. S., Smith, J. M., & Farber, D. J.** (1999). "EROS: A Fast Capability System." *ACM SIGOPS Operating Systems Review*, 33(5), 72–85.
  - *Relevance*: Modernizes the KeyKOS single-level store, demonstrating that synchronous, capability-based message passing can be executed in under 50 clock cycles.
* **Woodruff, J., et al.** (2014). "CHERI: Concentrating Capability Is Safe, Fast, and Easy." *Proceedings of the 41st Annual International Symposium on Computer Architecture (ISCA)*, 487–498.
  - *Relevance*: Formulates the hardware-compressed 128-bit capability layout and extensions to the MIPS ISA, establishing a low-overhead path for hardware pointer validation.
* **Watson, R. N. M., et al.** (2015). "CHERI: A Hybrid Capability-System Architecture for Scalable Software Compartmentalization." *IEEE Symposium on Security and Privacy*, 20–37.
  - *Relevance*: Explains how the CHERI model can be used to run legacy, un-modified C/C++ codebases while retrofitting fine-grained spatial and temporal memory bounds checks at the hardware level.
* **Watson, R. N. M., et al.** (2020). *Capability Hardware Enhanced RISC Instructions (CHERI): Instruction-Set Architecture (Version 8)*. *Technical Report UCAM-CL-TR-951*, University of Cambridge Computer Laboratory.
  - *Relevance*: The authoritative, primary specification detailing the tag-integrity, permission maps, and instructions for modern CHERI implementations.
