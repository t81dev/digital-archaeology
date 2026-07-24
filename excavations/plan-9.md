# Plan 9

> A distributed operating system built around the idea that "everything is a file" taken to its logical extreme, designed from the ground up for networks and research rather than backward compatibility.

---

## Summary

Plan 9 from Bell Labs is a research operating system developed in the late 1980s and 1990s by many of the same people who created Unix. It represents one of the most ambitious and coherent attempts to rethink operating system design in the network era.

Instead of bolting networking onto an existing system, Plan 9 was designed with distribution, simplicity, and research flexibility as core principles. While it never achieved widespread commercial adoption, its ideas — particularly the 9P protocol, per-process namespaces, and unified file interface — have influenced modern systems and remain highly relevant.

---

## Historical Context

By the mid-1980s, Unix was becoming burdened by its own success and compatibility requirements. Researchers at Bell Labs (including Ken Thompson, Rob Pike, and others) set out to build a new system unencumbered by legacy.

Plan 9 development began in the late 1980s. Key releases occurred throughout the 1990s, with the system being made open source in 2000. It was used internally at Bell Labs and by a dedicated community of researchers and enthusiasts, but never displaced commercial Unix, Linux, or Windows.

---

## Technical Overview

Plan 9’s design is built on a few powerful principles:
- **Everything is a file** — Including devices, networks, processes, and even graphics windows.
- **Per-process namespaces** — Every process can have its own view of the filesystem, enabling powerful isolation and customization.
- **9P protocol** — A simple, universal protocol for accessing remote resources as files.
- **Distributed by default** — Resources (CPU servers, file servers, auth servers) are naturally spread across machines.
- **Minimal kernel** — Clean, small, and focused on providing the core abstractions.

The system includes a complete user environment (including the Acme editor, which remains influential) and supports multiple architectures.

---

## Innovations

- **Unified resource access** via the file interface — radically simplifies system programming.
- **Dynamic namespaces** — Allows sophisticated sandboxing, union mounts, and per-user/per-process customization.
- **Protocol-based distribution** — 9P makes remote resources indistinguishable from local ones.
- **Research-first design** — Prioritizes elegance and flexibility over backward compatibility.
- **Influence on later systems** — Concepts live on in Linux
