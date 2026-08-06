# Plan 9

> A distributed operating system built around the idea that "everything is a file" taken to its logical extreme, designed from the ground up for networks and research rather than backward compatibility.

---

## Summary

Plan 9 from Bell Labs is a research operating system developed in the late 1980s and 1990s by many of the same people who created Unix. It represents one of the most ambitious and coherent attempts to rethink operating system design in the network era.

Instead of bolting networking onto an existing system, Plan 9 was designed with distribution, simplicity, and research flexibility as core principles. While it never achieved widespread commercial adoption, its ideas — particularly the 9P protocol, per-process namespaces, and unified file interface — have influenced modern systems and remain highly relevant.

---

## Historical Context

By the mid-1980s, Unix was becoming burdened by its own success and compatibility requirements. Researchers at Bell Labs (including Ken Thompson, Rob Pike, Dave Presotto, and Phil Winterbottom) set out to build a new system unencumbered by legacy. Development began in 1987 under the Computing Science Research Center of AT&T Bell Laboratories.

```
 AT&T Bell Labs Plan 9 Release Timeline
 ┌───────────────┬──────────────────────────────────────────────────────┐
 │ Release       │ Context / Major Features                             │
 ├───────────────┼──────────────────────────────────────────────────────┤
 │ 1st Edition   │ 1992: Internal research release, 9P1 protocol        │
 │ 2nd Edition   │ 1995: Commercial licensing ($350/non-commercial)     │
 │ 3rd Edition   │ 2000: Released under Lucent Plan 9 Open Source License│
 │ 4th Edition   │ 2002: Released under free software license (LPL)      │
 └───────────────┴──────────────────────────────────────────────────────┘
```

Rather than building a fat workstation operating system, Plan 9 was split into three specialized components connected by a network:
1. **CPU Servers**: Multi-processor compute pools devoid of local graphics.
2. **File Servers**: Dedicated, high-performance, write-once-read-many (WORM) storage engines.
3. **Terminals**: Diskless local systems providing user interaction (Geryon, terminal nodes) running the `rio` windowing system.

---

## Technical Overview

Plan 9's design is built on three simple, orthogonal, but universally applied principles:

1. **Everything is a file**: All resources, including devices, network connections, memory, process states, and graphic contexts, are represented as files or hierarchical file trees.
2. **Per-process namespaces**: Every process operates in its own customized view of the filesystem. Namespaces can be dynamically configured at runtime via three primitives: `mount`, `bind`, and union mounts.
3. **9P protocol**: A simple, synchronous, connection-oriented, stateful byte-oriented request/response protocol. Every resource access, whether local or remote, is translated into 9P transactions.

```
       Plan 9 Unified 9P Network Abstraction

    [ User Process ]      [ User Process ]
           │                     │
      (Local View)          (Local View)
     /dev/draw             /net/tcp/0/data
           │                     │
    ┌──────▼─────────────────────▼──────┐
    │       Plan 9 Namespace Layer      │
    └──────────────────┬────────────────┘
                       │ (Uniform 9P Protocol Messages)
                       ▼
    ┌───────────────────────────────────┐
    │     IL Protocol or TCP/IP Net     │
    └──────────────────┬────────────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼ (Remote File) ▼ (Local Device)▼ (Remote CPU)
  [ File Server ]   [ VGA Driver ]   [ CPU Server ]
```

### The 9P Protocol Message Flows
The 9P protocol maps system calls into sequential message pairs (Request `T-message` and Response `R-message`):
- `Tversion` / `Rversion`: Negotiate protocol version.
- `Tauth` / `Rauth`: Establish authentication channel.
- `Tattach` / `Rattach`: Mount the root of a file tree.
- `Twalk` / `Rwalk`: Traverse a directory tree to obtain a new file fid (file identifier).
- `Topen` / `Ropen`: Open a file fid for read/write.
- `Tread` / `Rread`: Retrieve bytes from a file fid.
- `Twrite` / `Rwrite`: Write bytes to a file fid.
- `Tclunk` / `Rclunk`: Release a file fid.

---

## Innovations

- **Dynamic Union Mounts**: Multiple directories can be bound to the exact same mount point. When a lookup occurs, the system searches the directories sequentially. This allows multiple bin folders or custom library sets to be cleanly merged without copying files.
- **Protocol-driven Isolation**: The process file server `/proc` allows debuggers like `acid` to inspect and control processes solely by writing or reading standard files, bypassing exotic, hardware-dependent system calls like `ptrace`.
- **Private Namespaces**: Unlike Unix where `/dev` and `/net` are global and shared, Plan 9 allows a process to import a remote `/net` stack (e.g., from an internet-connected gateway) and mount it locally, making remote network stacks completely transparent to existing programs.
- **Unified Hardware Controls**: Devices are configured using simple text commands written directly to their control files (e.g., writing `"size 1024 768"` to `/dev/screen/ctrl`), completely standardizing hardware driver interfaces.

---

## Limitations

- **Performance Penalties of Aggressive File Conversions**: Exposing everything through a serial string-based file interface introduced context-switching and parsing overheads. For example, text-based parsing of process states in `/proc` is significantly slower than direct memory structures.
- **Lack of Memory Overcommit & Page Swapping**: Early Plan 9 did not support virtual page-swapping to disk; memory allocation was strictly tied to physical RAM limits, restricting large application processes.
- **Incompatible Posix / Socket APIs**: Standard socket-based network applications (using `gethostbyname`, `bind`, `connect`) had to be heavily rewritten to match Plan 9’s network filesystem layout (`/net/tcp/...`).

---

## Reasons for Decline

1. **Ecosystem Lock-In & POSIX Dominance**: By the mid-1990s, software vendors standardized exclusively on POSIX and Win32 interfaces. The cost of porting foundational applications (e.g., databases, web browsers, compilers) to Plan 9 was economically prohibitive.
2. **The Success of Linux**: Linux provided a "good enough" free, open-source Unix clone that ran on cheap x86 PCs, satisfying the open-source community's needs while maintaining binary compatibility with existing Unix code.
3. **Corporate and Licensing Hesitation**: AT&T's early commercial licensing policies were highly restrictive and expensive. By the time Plan 9 was open-sourced under a free license in 2002, the market had completely consolidated around Linux and Windows.

---

## Modern Evaluation (Forward-Looking)

Plan 9's dynamic namespace design directly prefigures modern virtualization:
- **Containers and Microservices**: Docker containers rely on namespace isolation (mount namespaces, network namespaces) to create sandboxed environments. This is conceptually identical to Plan 9's per-process namespace isolation.
- **9P in Virtualized Infrastructure**: The 9P protocol is actively used in modern cloud virtualization. **WSL2** (Windows Subsystem for Linux) uses a highly optimized 9P client/server to share folders between Windows and Linux. Similarly, **QEMU/KVM** leverages VirtFS (a 9P transport over virtio) to share host directories with guest VMs with near-zero overhead.
- **Edge Computing and IoT**: Representing distributed sensors and actuators as simple, network-transparent 9P file streams eliminates the need for proprietary, fragmented IoT APIs.

---

## Related Technologies

- [Inferno](../excavations/inferno.md) — *Direct descendant of Plan 9, running 9P (as Styx) inside a register-based VM (Dis).*
- [Transputers](../excavations/transputers.md) — *Shares the philosophy of a network-transparent distributed fabric.*
- [Capability Systems](../excavations/capability-systems.md) — *Plan 9's fine-grained namespace mounts can be analyzed as a spatial capability mechanism.*

---

## Lessons Learned

1. **Elegance Does Not Break Lock-In**: A clean-slate, mathematically beautiful system design cannot overcome the economic inertia of existing toolchains and legacy standard APIs (POSIX).
2. **Unified Interfaces Lower System Complexity**: Standardizing all IO on a single protocol (9P) makes network distribution, security sandboxing, and device drivers orthagonal, greatly reducing kernel LOC (Lines of Code).
3. **Separate Concerns at the Network Level**: Distinguishing compute (CPU servers), storage (File servers), and interface (Terminals) is highly scalable and matches modern cloud compute/storage disaggregation.

---

## Scorecard

| Category | Rating | Rationale |
| --- | --- | --- |
| Historical Importance | ★★★★☆ | Deeply influenced Unix developments (e.g., `/proc`, UTF-8) and modern containerization. |
| Technical Innovation | ★★★★★ | Flawless unification of networking, device control, and isolation under a single protocol. |
| Commercial Success | ★☆☆☆☆ | Failed to capture market share due to pricing, timing, and POSIX compatibility issues. |
| Modern Potential | ★★★★☆ | 9P remains highly active in cloud-mounting layers (VirtFS/WSL2); namespace concepts form the core of containers. |
| AI Synergy | ★★☆☆☆ | Low direct synergy with neural models, but provides secure or distributed runtimes. |
| Difficulty to Recreate | ★★★★☆ | Requires extensive systems-level implementation and emulation efforts. |

---

## References & Further Reading

1. Pike, R., Presotto, D., Thompson, K., Trickey, H., & Winterbottom, P. (1995). *The Use of Name Spaces in Plan 9*. Operating Systems Review, 29(2), 72-76.
2. Pike, R., Presotto, D., Thompson, K., & Trickey, H. (1990). *Plan 9 from Bell Labs*. UKUUG Summer Conference.
3. Presotto, D., & Winterbottom, P. (1993). *The Organization of Networks in Plan 9*. USENIX Winter 1993 Conference.
4. Welch, B. (1994). *A Comparison of Three Distributed File Systems: AFS, Sprite, and Plan 9*. Computing Systems, 7(2).
5. Foundation, 9front. (2024). *The 9front FQA (Frequently Questioned Answers)*. Community-driven active fork documentation.

---

*Cross-links: [Inferno](../excavations/inferno.md), [Transputers](../excavations/transputers.md), [Capability Systems](../excavations/capability-systems.md), [Ecosystem Lock-In](../patterns/ecosystem-lockin.md), [Constraint Migration](../patterns/constraint-migration.md), [Forgotten Abstractions](../patterns/forgotten-abstractions.md).*
