# Multics

> A pioneering time-sharing operating system that introduced many foundational concepts in computing security, virtualization, hierarchical filesystems, and reliable multi-user computing—developed over decades with massive ambition and lasting influence.

---

## Summary

Multics (MULTiplexed Information and Computing Service) was one of the most ambitious and influential operating systems ever created. Developed starting in 1964 as a joint project by MIT (Project MAC), General Electric, and Bell Labs, it was designed as a high-reliability, scalable utility computing platform — essentially a "computing utility" that users could access like electricity or water.

Multics introduced or popularized numerous concepts taken for granted today: segmented virtual memory, hierarchical filesystems with access control lists (ACLs), dynamic linking, ring-based protection (security rings), online reconfiguration, and strong security principles. It ran continuously for decades at some sites and heavily influenced Unix (which was originally written as a simpler alternative to Multics). Despite its technical successes, Multics struggled with performance, complexity, and commercial adoption, ultimately becoming a niche system.

---

## Historical Context

In the early 1960s, computing was dominated by batch processing on expensive mainframes. Researchers at MIT (Project MAC) sought a true time-sharing system that could support hundreds of simultaneous users securely and reliably.

- **1964**: Project begins, target hardware is the specialized General Electric GE-645 mainframe.
- **1965**: Introduction of PL/I as the primary systems programming language, an exceptionally bold choice over assembly.
- **1969**: Bell Labs withdraws due to high delays and missing milestones, prompting Ken Thompson and Dennis Ritchie to write Unix.
- **1973**: Honeywell (having acquired GE's computer division) releases Multics commercially on the Honeywell 6180.
- **1985**: Multics is awarded the first B2 Orange Book security rating by the National Computer Security Center (NCSC).
- **2000**: The last operational Multics system, running at the Canadian Department of National Defence in Halifax, is shut down on October 30.

---

## Technical Overview

Multics was designed around the vision of computing as a secure public utility, characterized by strict hardware-software co-design:

```
            Multics Protection Ring Architecture

                 [ Ring 3: User Utilities ]
               ┌─────────────────────────────┐
               │    [ Ring 2: Libraries ]    │
               │  ┌───────────────────────┐  │
               │  │  [ Ring 1: OS Services]  │  │
               │  │  ┌─────────────────┐  │  │
               │  │  │  [ Ring 0: Kernel ]│  │  │
               │  │  │                 │  │  │  │
               │  │  │  - Hardware MMU │  │  │  │
               │  │  │  - Segment Page │  │  │  │
               │  │  └─────────────────┘  │  │  │
               │  └───────────────────────┘  │
               └─────────────────────────────┘
                  ▲                       │
                  │   (Gate Call Crossing)│
                  └───────────────────────┘
```

### 1. Ring Protection Architecture
The hardware (GE-645, Honeywell 6180) enforced concentric rings of authorization (typically 8 rings). Ring 0 held the kernel, Ring 1 held operating system services, Ring 2 held runtime libraries, and Ring 3 held user processes.
- Code in outer rings could access inner rings only via explicit hardware-trapped entry points called **gates**.
- Any attempt to jump directly to inner ring code bypassed gates, causing immediate hardware faults.

### 2. Segmented Virtual Memory & Single-Level Store
Multics completely abandoned the traditional distinction between "volatile memory" (pointers/variables) and "persistent storage" (files on disk).
- Everything in the system was represented as a **segment** of up to $2^{18}$ words.
- Files *were* memory segments. When a process accessed a file, the system mapped the segment directly into the virtual address space using demand-paging. There was no explicit file `read` or `write` system call; standard memory operations operated directly on persistent files.

---

## Innovations

- **The Single-Level Store**: Unified file IO and virtual memory, removing disk-to-memory marshalling from the application layer.
- **Dynamic Linking**: Programs linked to library routines at execution time, allowing libraries to be updated transparently without recompiling user applications.
- **Hierarchical Access Control Lists (ACLs)**: Fine-grained permissions (read, execute, write) declared on file/directory nodes, departing from Unix's basic owner/group bit scheme.
- **On-Line Reconfiguration**: Hardware components (CPUs, memory banks, disk controllers) could be dynamically added or removed from the system without halting the operating system, realizing the "always-on utility" vision.
- **High-Level Language Implementation**: Writing almost the entire operating system in PL/I proved that assembly language was no longer necessary for robust, performant kernel engineering.

---

## Limitations

- **Extreme Hardware Dependencies**: The single-level store and protection rings required specialized, complex hardware memory management units (MMUs) with custom segmentation registers, preventing the OS from being ported to commodity processors.
- **Performance Overhead**: Paging overhead, dynamic address translation, and gate-crossing register-state saves introduced significant performance penalties on 1960s/1970s microprocessors.
- **Compiler Maturity**: PL/I was an extraordinarily complex language. Early GE PL/I compilers were notoriously slow and produced highly inefficient object code, creating severe bootstrap delays.

---

## Reasons for Decline

1. **The "Worse is Better" Phenomenon**: Unix arose as a reactive, simplified derivative of Multics. By stripping out segmented memory, protection rings, and single-level stores, Unix was able to run on small, cheap minicomputers (DEC PDP-11) and scale down, whereas Multics required massive, expensive mainframes.
2. **Ecosystem Portability**: Unix was rewritten in C, making it highly portable to any new microprocessor. Multics remained bound to Honeywell mainframes, locking it out of the personal computer and workstation revolution of the 1980s.
3. **High Price and Scale**: Honeywell failed to execute a strong commercial market campaign. Multics was priced as an enterprise mainframe system, which universities and research labs could not afford, whereas Unix was distributed nearly free of charge.

---

## Modern Evaluation (Forward-Looking)

Modern computing is systematically reintroducing Multics principles to combat security and cloud infrastructure limits:
- **CHERI and Hardware Compartmentalization**: The CHERI (Capability Hardware Enhanced RISC Instructions) project revives Multics protection rings by embedding security bounds and permissions directly inside hardware capability registers, achieving secure compartmentalization inside a single address space.
- **Cloud Computing as a Public Utility**: Modern cloud virtualization (e.g., serverless compute pools, elastic billing) is the exact economic realization of Multics' 1965 "computing utility" vision.
- **Single-Level Store Revivals**: The rise of large-scale **Non-Volatile Main Memory (NVMM)** and byte-addressable persistent RAM (like CXL-attached storage) has revived interest in single-level stores. Contemporary research operating systems are returning to memory-mapped persistent segments to bypass traditional database serialization costs.

---

## Related Technologies

- [Plan 9](../excavations/plan-9.md) — *Shares the goal of a clean, unified resource architecture, but uses a file protocol rather than a single-level memory store.*
- [Lisp Machines](../excavations/lisp-machines.md) — *Rejects filesystems in favor of persistent object memory.*
- [Capability Systems](../excavations/capability-systems.md) — *Extends Multics rings into object-based unforgeable handles.*

---

## Lessons Learned

1. **Simplicity Scales Faster Than Perfection**: A simple, portable system (Unix) will outpace an elegant, comprehensive, but highly complex architecture (Multics) by capturing developer-level compounding loops first.
2. **Co-Design Must Account for Portability**: Tying an operating system's core abstractions too closely to specialized mainframe hardware MMUs guarantees obsolescence when hardware paradigms shift.
3. **Persistent Memory Simplifies Software**: Eliminating the file/memory boundary removes the need for application-level parsing, marshalling, and custom database persistence code.

---

## Scorecard

| Category | Rating | Rationale |
| --- | --- | --- |
| Historical Importance | ★★★★★ | Ground zero for modern operating system concepts; directly inspired Unix, security rings, and ACLs. |
| Technical Innovation | ★★★★★ | Extremely advanced. Features like single-level store and dynamic PL/I linking were decades ahead of standard practice. |
| Commercial Success | ★★☆☆☆ | honeywell sold only roughly 80 systems globally; was a commercial failure despite high-reliability military deployments. |
| Modern Potential | ★★★★☆ | Essential concepts (persistent stores, ring isolation, utility scaling) are highly active in secure enclaves and NVMM research. |
| AI Synergy | ★★☆☆☆ | Low direct synergy with neural models, but provides secure or distributed runtimes. |
| Difficulty to Recreate | ★★★★☆ | Requires extensive systems-level implementation and emulation efforts. |

---

## References & Further Reading

1. Corbató, F. J., & Vyssotsky, V. A. (1965). *Introduction and Overview of the Multics System*. AFIPS Fall Joint Computer Conference.
2. Organick, E. I. (1972). *The Multics System: An Examination of Its Structure*. MIT Press.
3. Saltzer, J. H. (1974). *Protection and the Control of Information Sharing in Multics*. Communications of the ACM, 17(7), 388-402.
4. Schroeder, M. D., & Saltzer, J. H. (1972). *A Hardware Architecture for Implementing Protection Rings*. Communications of the ACM, 15(3), 157-170.
5. Daley, R. C., & Dennis, J. B. (1968). *Virtual Memory, Processes, and Sharing in Multics*. Communications of the ACM, 11(5), 306-312.

---

*Cross-links: [Plan 9](../excavations/plan-9.md), [Capability Systems](../excavations/capability-systems.md), [Lisp Machines](../excavations/lisp-machines.md), [Ecosystem Lock-In](../patterns/ecosystem-lockin.md), [Constraint Migration](../patterns/constraint-migration.md), [Forgotten Abstractions](../patterns/forgotten-abstractions.md).*
