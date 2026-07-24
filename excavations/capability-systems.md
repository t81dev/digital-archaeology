# Capability Systems

> *A fundamentally different approach to security and access control based on unforgeable tokens of authority rather than ambient permission checks.*

---

## Summary

Capability-based security represents a powerful alternative to traditional ACL (Access Control List) and Unix-style permission models. In a capability system, possessing an unforgeable reference (a “capability”) to a resource *is* the authority to use it. Capabilities combine designation with permission in a single mechanism.

Pioneered in the 1960s and implemented in several influential systems, capability architectures offer elegant solutions to many persistent security problems — yet they remain largely outside the mainstream.

---

## Historical Context

The idea originated in the 1960s:

- **Dennis and Van Horn** (1966) — Formalized the concept of capabilities.
- **HYDRA** (Carnegie Mellon, 1970s)
- **CAP** computer (Cambridge University)
- **KeyKOS** (1980s) — A commercial microkernel OS built entirely around capabilities.
- **EROS** (1990s–2000s) — Highly secure, formally verified capability OS.
- **L4** microkernel family and later derivatives explored capability-like mechanisms.

The most ambitious implementation was probably **KeyKOS**, which ran for years in production banking environments with exceptional reliability and security.

---

## Technical Overview

In a pure capability system:

- Every resource (file, device, memory region, service) is represented by a **capability** — an unforgeable token.
- Capabilities can be passed between processes but cannot be guessed or forged.
- Rights can be attenuated (reduced) when passing capabilities.
- No global namespaces with ambient authority (contrast with Unix `uid`/`gid` or filesystem paths).

This model eliminates many classes of vulnerabilities common in traditional systems, such as confused deputy problems and confused aliasing.

---

## Innovations

- **Principle of Least Authority (POLA)** — Enforced by design rather than discipline.
- **Fine-grained delegation** — Easy and safe to grant limited rights.
- **No ambient authority** — Reduces attack surface dramatically.
- **Object-capability model** — Natural fit for object-oriented and distributed systems.
- **Strong confinement** — Easier to reason about security boundaries.

---

## Why It Didn’t Win

- **Incompatibility** with existing Unix/Windows models.
- **Ecosystem lock-in** — Vast software assumed ACL-style permissions.
- **Performance concerns** (mostly mitigated in later designs).
- **Conceptual shift** — Developers found capabilities unfamiliar compared to simple `chmod` or file paths.
- **Timing** — Arrived during the rise of commodity operating systems that prioritized compatibility over security fundamentals.

---

## Modern Relevance

Capability systems are experiencing a quiet renaissance:

- **CHERI** (Cambridge) — Capability Hardware Enhanced RISC Instructions — adding capability support to ARM and RISC-V.
- **Google’s Fuchsia** OS uses capability-like Zircon handles.
- **WebAssembly** and cloud-native security models increasingly adopt object-capability principles.
- **Blockchain / Smart Contracts** — Essentially global capability systems (tokens as capabilities).
- **Operating system research** (seL4, Barrelfish, others).

Modern hardware support (CHERI) and the rise of distributed, zero-trust environments make capabilities far more practical than in the 1980s.

---

## Lessons Learned

- Security models are incredibly sticky — changing them requires both technical and cultural shifts.
- Elegant, mathematically clean designs can still lose to “good enough” incumbent systems.
- Hardware support (like CHERI) can dramatically lower the cost of adopting better abstractions.
- Many long-standing security problems (privilege escalation, confused deputy) have known elegant solutions that were never widely adopted.

Capability systems demonstrate that some of the best ideas in computing were abandoned not for technical reasons, but because they challenged established ways of thinking at the wrong time.

---

## Related Excavations
- [Lisp Machines](../excavations/lisp-machines.md)
- [Plan 9](../excavations/plan-9.md) (planned)
- Transputers (message-passing philosophy)

## Related Patterns
- [Forgotten Abstractions](../patterns/forgotten-abstractions.md)
- [Ecosystem Lock-In](../patterns/ecosystem-lockin.md)
- [Economic Failures](../patterns/economic-failures.md)

## Related Modern Relevance
- [Security](../modern-relevance/security.md) (planned)

---

## References (Selected)
- Dennis & Van Horn, “Programming Semantics for Multiprogrammed Computations” (1966)
- KeyKOS papers and documentation
- CHERI technical reports (University of Cambridge)
- Miller, Shapiro, et al. — Object-capability model literature