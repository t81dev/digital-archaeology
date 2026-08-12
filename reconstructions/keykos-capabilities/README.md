# [KeyKOS](../../GLOSSARY.md)-style Object-Capability Simulator

Demonstrates unforgeable capability keys, message invocation, least authority sandboxing, attenuation/minting, and basic persistence checkpointing of a capability graph (mimicking continuous orthogonal persistence).

## Features
- Unforgeable `Key` representation designating target object + permission sets.
- Explicit `attenuate` operations to derive restricted keys.
- Completely ambient-authority-free routing engine (`KeykosSystem`).
- Standard, self-contained `FileNode` and `DirectoryNode` abstractions.
- Continuous orthogonal persistence simulation via dynamic state serialization and restoration.
