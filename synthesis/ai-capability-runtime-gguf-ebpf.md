# [GGUF](../excavations/llama-cpp.md) + [llama.cpp](../excavations/llama-cpp.md) + [eBPF](../excavations/ebpf.md) Capability Runtime Synthesis

> **An Architectural Synthesis of Probabilistic Local Model Artifacts, Memory-Bandwidth-Aware Inference Runtimes, and Verifier-Constrained In-Kernel Execution Mediated by a Capability Broker**

---

## 1. Summary / Non-Claims

This synthesis investigates the proposed convergent boundary at the intersection of three excavated computing lineages:
1. **[GGUF model artifacts](../excavations/llama-cpp.md)** — self-describing, single-file quantized neural weight containers.
2. **[llama.cpp local inference runtime](../excavations/llama-cpp.md)** — C/C++ memory-bandwidth-aware local execution engines.
3. **[eBPF verified in-kernel execution](../excavations/ebpf.md)** — static verifier-gated, JIT-compiled supervisor-space event runtimes.

We analyze the architectural pattern that emerges when these substrates are bound together via a user-space **Capability Broker** to form a candidate **local AI capability runtime**.

```text
               THE PROPOSED LOCAL AI CAPABILITY RUNTIME

 ┌──────────────────────────────────────────────────────────────────┐
 │                       PROBABILISTIC LAYER                        │
 │  GGUF Model Artifact  ──►  llama.cpp Local Inference Runtime     │
 │  (Quantized Weights)        (Sampling, Tool Selection Intent)    │
 └────────────────────────────────┬─────────────────────────────────┘
                                  │
                                  ▼ (Structured Tool Call / Schema Intent)
 ┌──────────────────────────────────────────────────────────────────┐
 │                     DETERMINISTIC BROKER LAYER                   │
 │                     Capability Broker Substrate                  │
 │  - Schema Validation     - Token Authorization & Policy          │
 │  - Capability Registry   - Audit Logging & Rate Limiting         │
 └────────────────────────────────┬─────────────────────────────────┘
                                  │
                                  ▼ (Approved BPF Map Lookup / Attach Request)
 ┌──────────────────────────────────────────────────────────────────┐
 │                      VERIFIED KERNEL SUBSTRATE                   │
 │  BPF Static Verifier  ──►  JIT Engine  ──►  Linux Kernel Hooks    │
 │  (Ahead-of-Time Proof)     (Native Exec)    (XDP, Tracepoints, LSM) │
 └──────────────────────────────────────────────────────────────────┘
```

### Explicit Non-Claims & Epistemic Boundaries
To maintain rigorous epistemic discipline, this document establishes the following explicit non-claims:
* **No Product Pitch or Implementation Tutorial**: This is an architectural analysis of a proposed runtime pattern, not a product announcement or user manual.
* **No Format Fusion Claim**: We explicitly reject the premise that GGUF files standardly embed eBPF bytecode or that eBPF ISA execution is integrated directly into transformer tensors.
* **No Existing Standard Assertion**: This stack is **not** an established industry standard or off-the-shelf production framework. It is a proposed composition at the boundary of modern OS and AI research.
* **No Alignment-as-Safety Substitution**: We do not assert that neural model alignment (SFT/RLHF/DPO) eliminates the need for deterministic operating system access controls, or that eBPF safety proofs substitute for semantic authorization policy.

---

## 2. Scope and Method

This investigation follows the Digital Archaeology methodological framework:
* **Primary Source & Lineage Grounding**: Extracting abstractions directly from primary literature and validated excavations in this repository ([Large Language Models](../excavations/large-language-models.md), [llama.cpp](../excavations/llama-cpp.md), [eBPF](../excavations/ebpf.md), [Linux](../excavations/linux.md), [OpenAI](../excavations/openai.md), and [Capability Systems](../excavations/capability-systems.md)).
* **Epistemic Classification**: Categorizing every major claim into one of four explicit categories:
  1. *Established in Lineage Excavations*
  2. *Engineering Inference*
  3. *Proposed Architecture*
  4. *Speculative Research Direction*
* **Decomposition & Stress-Testing**: Stress-testing the core thesis against threat models, information leakage boundaries, context window constraints, and verifier complexity limits.

---

## 3. Lineage Inputs

The proposed architecture sits at the convergence of three distinct technological evolutions and one foundational security lineage:

```text
 LLM Lineage          : Prediction ──► Instruction Tuning ──► Tool Calling
 llama.cpp Lineage    : Cloud API  ──► Local GGUF Artifact ──► Memory-Aware Runtime
 eBPF Lineage         : cBPF Filter──► 64-bit JIT VM      ──► Verified Kernel Substrate
 Capability Security  : ACLs       ──► Tagged Memory       ──► Object Capabilities (POLA)
        │
        └────────────────────────────────────────► PROPOSED CAPABILITY RUNTIME
```

### A. Large Language Model Lineage ([Established in Lineage Excavations])
As excavated in [Large Language Models](../excavations/large-language-models.md) and [OpenAI](../excavations/openai.md), autoregressive neural sequence models transitioned from pure token predictors into instruction-following executives and structured tool callers. By training models to emit formal JSON schemas bounded by delimiters (such as ChatML boundary tokens), the model output is repurposed as a soft control plane capable of selecting named tool interfaces. However, neural outputs remain inherently **probabilistic, non-deterministic, and vulnerable to prompt injection**.

### B. llama.cpp / GGUF Lineage ([Established in Lineage Excavations])
As excavated in [llama.cpp](../excavations/llama-cpp.md), Georgi Gerganov's lineage decoupled LLM execution from cloud-centric Python/CUDA stacks. By introducing block-wise integer quantization (e.g., Q4_K_M) and the zero-copy memory-mapped ([`mmap`](../GLOSSARY.md)) **[GGUF](../excavations/llama-cpp.md) container format**, [llama.cpp](../excavations/llama-cpp.md) converted foundation models into portable, local, single-file software artifacts runnable on commodity hardware.

### C. eBPF Substrate Lineage ([Established in Lineage Excavations])
As excavated in [eBPF](../excavations/ebpf.md) and [Linux](../excavations/linux.md), extended Berkeley Packet Filter transformed the Linux kernel into a dynamically programmable virtual machine execution plane. By coupling a 64-bit JIT-compiled register architecture with a **static verifier**, kernel-resident **BPF maps**, and capability-gated **helpers**, eBPF allows user space to execute verified custom logic directly inside kernel event hooks (`XDP`, `kprobes`, `tracepoints`, `LSM`) without risk of kernel panics or unauthorized memory access.

### D. Capability Security Lineage ([Established in Lineage Excavations])
As excavated in [Capability-Based Security](capability-based-security.md), [Capability Systems](../excavations/capability-systems.md), and [KeyKOS](../excavations/keykos-nanokernel-capabilities.md), capability systems eliminate ambient authority. Access to a resource requires holding an unforgeable, typed token designating both the object and its permitted operations, enforcing the **Principle of Least Authority (POLA)**.

---

## 4. Proposed Architecture & Layered Decomposition

To evaluate the proposed local AI capability runtime, we decompose the system into twelve discrete architectural layers, explicitly marking which layers exist today and which are proposed artifacts:

```text
 ┌──────────────────────────────────────────────────────────────────────────────┐
 │ Layer                                                 │ Status               │
 ├───────────────────────────────────────────────────────┼──────────────────────┤
 │ 1. GGUF Model Artifact                                │ Existing Artifact    │
 │ 2. llama.cpp Inference Engine                         │ Existing Artifact    │
 │ 3. Probabilistic Executive (Model Intent)             │ Existing Behavior    │
 │ 4. Capability Schema (Typed API Contract)             │ Proposed Interface   │
 │ 5. Capability Broker (Mediator & Enforcement Gate)   │ Proposed Component   │
 │ 6. Capability Registry (Approved eBPF Repository)     │ Proposed Component   │
 │ 7. eBPF Program Artifacts (ELF Bytecode + BTF)        │ Existing Artifact    │
 │ 8. BPF Static Verifier                                │ Existing Substrate   │
 │ 9. BPF Maps / Ring Buffers (Shared Kernel State)      │ Existing Substrate   │
 │ 10. Kernel Attach Points (XDP, Tracepoints, LSM)      │ Existing Substrate   │
 │ 11. Linux Kernel (Supervisor Address Space)           │ Existing Substrate   │
 │ 12. Context Observation Return Path                   │ Proposed Interface   │
 └───────────────────────────────────────────────────────┴──────────────────────┘
```

### Detailed Layer Descriptions

1. **GGUF Model Artifact** *(Existing)*: Single-file binary package containing quantized tensor weights, tokenizer vocabulary, and hyperparameter metadata.
2. **llama.cpp Inference Engine** *(Existing)*: C++ runtime executing autoregressive matrix math, managing the KV-cache, and performing memory-mapped tensor streaming.
3. **Probabilistic Executive** *(Existing)*: The active model generation state forming semantic intent, selecting tools, and generating parameter arguments.
4. **Capability Schema** *(Proposed)*: A declarative, strongly-typed JSON/protobuf specification defining available capability names, permitted parameter types, bounds, and required authorization levels.
5. **Capability Broker** *(Proposed)*: The trusted user-space supervisor process intercepting tool call requests, checking token authorizations, validating parameter bounds against schemas, invoking approved eBPF interactions, and formatting telemetry results.
6. **Capability Registry** *(Proposed)*: A cryptographically signed local repository mapping abstract capability identifiers (`observe_process_exec`, `measure_socket_latency`) to pre-compiled, verified eBPF ELF object files.
7. **eBPF Program Artifacts** *(Existing)*: Compiled 64-bit eBPF bytecode files (`.o`) containing BPF Type Format (BTF) relocation metadata.
8. **BPF Static Verifier** *(Existing)*: The Linux kernel ahead-of-time abstract interpreter proving bounds safety, termination, pointer validity, and memory isolation before bytecode load.
9. **BPF Maps / Ring Buffers** *(Existing)*: Kernel-resident data structures (`BPF_MAP_TYPE_HASH`, `BPF_MAP_TYPE_RINGBUF`) serving as shared state storage between kernel probes and user space.
10. **Kernel Attach Points** *(Existing)*: In-kernel event surfaces (`kprobes`, `uprobes`, `tracepoints`, `sched_cls`, `lsm_hook`) where verified eBPF programs hook execution.
11. **Linux Kernel** *(Existing)*: The supervisor operating system substrate enforcing ring-0 protection and hardware isolation.
12. **Context Observation Return Path** *(Proposed)*: A sanitizing, windowing, and aggregating pipeline that transforms raw kernel ring-buffer events into concise, low-token JSON summaries suitable for model context injection.

---

## 5. Artifact Separation Model

A critical architectural requirement of this synthesis is the **rejection of format or execution containment**.

```text
  REJECTED ARCHITECTURE: FORMAT CONTAINMENT (eBPF Bytecode Inside GGUF Tensors)
  ┌──────────────────────────────────────────────────────────────────┐
  │ [ GGUF File ]                                                    │
  │   - Quantized Weight Tensors                                     │
  │   - Embedded Raw eBPF Bytecode Blobs (UNVERIFIED)                │
  │   - Direct Model Kernel Emission Path (DANGEROUS)               │
  └──────────────────────────────────────────────────────────────────┘

  PREFERRED ARCHITECTURE: COMPOSITIONAL SEPARATION (Broker-Mediated)
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │ [ GGUF File ]    │    │ [ eBPF ELF ]     │    │ [ Policy File ]  │
  │ Model Weights    │    │ Pre-Compiled     │    │ Capability       │
  │ Tokenizer        │    │ Signed Bytecode  │    │ Authorization    │
  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   ▼
                      ┌──────────────────────────┐
                      │    Capability Broker     │
                      └──────────────────────────┘
```

### Why Format Containment Fails ([Engineering Inference])
1. **Lifecycle Mismatch**: Neural network weights are re-quantized, fine-tuned, and swapped frequently. Kernel eBPF bytecode is bound strictly to kernel BTF struct layouts (`vmlinux`) and C-ABI helper signatures. Embedding kernel bytecode in model weight files breaks Compile Once – Run Everywhere (CO-RE) portability.
2. **Security Audit Collapse**: If eBPF bytecode is hidden inside massive multi-gigabyte GGUF tensor payloads, static security inspection of kernel logic becomes impossible without extracting and parsing non-standard metadata blocks.
3. **Signature and Provenance Breakdown**: eBPF programs loaded into production kernels require cryptographic signatures (e.g., `IMA` or `module signing`). Weight artifacts require model provenance verification. Merging them forces a single compromised signature chain.

### Compositional Artifact Separation ([Proposed Architecture])
Under the compositional model, GGUF model files store **only** semantic intent weights and standard tool schemas. eBPF bytecode resides in independent, standard ELF object binaries maintained in an audited **Capability Registry**. The **Capability Broker** links model intent to eBPF execution at runtime via name-bound, policy-checked dispatch tables.

---

## 6. Capability Broker as Central New Object

The **Capability Broker** is the foundational new architectural component introduced by this synthesis. It acts as the explicit, trusted mediator between the probabilistic model runtime and the deterministic kernel substrate.

```text
               CAPABILITY BROKER INTERNAL SUBSYSTEMS

  LLM Intent ──► [ Schema & Syntax Validator ]
                        │
                        ▼
                 [ Semantic Authz Policy Engine ] ◄── Local Access Control Matrix
                        │
                        ▼
                 [ Capability Registry Dispatcher ] ──► Map Lookup / Program Link
                        │
                        ▼
                 [ Event Summarizer & Filter ] ──► Sanitized Context Return
                        │
                        ▼
                 [ Out-of-Band Audit Logger ] ──► Append-Only File / Syslog
```

### Core Responsibilities of the Broker ([Proposed Architecture])
1. **Schema & Syntax Validation**: Intercepting model tool calls and validating arguments against JSON schemas. If a model generates malformed types (e.g., passing a string where an integer port is required), the Broker rejects the call at the user-space boundary without touching the kernel.
2. **Semantic Authorization & Policy Enforcement**: Evaluating whether the active session/user holds explicit authority to invoke the requested capability with the specified parameters.
3. **Capability Registry Dispatch**: Mapping abstract schema names (`inspect_network_sockets`) to specific, pre-compiled eBPF programs, and executing standard `bpf()` system calls (`BPF_MAP_LOOKUP_ELEM`, `BPF_LINK_CREATE`) on behalf of the application.
4. **Event Rate Limiting & Aggregation**: Intercepting high-frequency ring buffer streams generated by eBPF probes, applying sliding-window counters, and formatting raw kernel events into structured, low-token JSON summaries.
5. **Non-Repudiable Audit Logging**: Writing every model intent request, validation decision, dispatch event, and kernel result to an append-only, tamper-resistant log outside the reach of the model context window.

---

## 7. Dual Trust Boundaries

A central structural principle of this synthesis is the strict preservation of **Dual Trust Boundaries**. Model alignment must never be confused with machine safety.

```text
                       DUAL TRUST BOUNDARY MODEL

                      [ Model Output Generation ]
                                   │
                                   ▼
  ═══════════════════════════════════════════════════════════════════
  TRUST BOUNDARY 1: SEMANTIC AUTHORIZATION GATE (User Space Broker)
  Question: "Is this model session PERMITTED to request this action?"
  Mechanism: ACLs, Capabilities, Role-Based Access, Schema Rules
  Failure Mode: Rejection with Policy Error to LLM Context
  ═══════════════════════════════════════════════════════════════════
                                   │ (Passes Authz)
                                   ▼
                      [ eBPF Bytecode Load / Attach ]
                                   │
                                   ▼
  ═══════════════════════════════════════════════════════════════════
  TRUST BOUNDARY 2: EXECUTABLE SAFETY GATE (Kernel Verifier)
  Question: "Is this program GUARANTEED to be memory-safe & non-fatal?"
  Mechanism: Abstract Interpretation, DAG Check, Pointer Bounds
  Failure Mode: BPF Load Rejection with Verifier Error Log
  ═══════════════════════════════════════════════════════════════════
                                   │ (Passes Verifier)
                                   ▼
                      [ Supervisor Execution in Kernel ]
```

### Boundary 1: Semantic Authorization Gate ([Proposed Architecture])
* **Owner**: Capability Broker (User Space).
* **Responsibility**: Verifies permission, scope, and parameter legitimacy. It asks: *May this model session inspect port 8080 or process PID 1420 under current policy?*
* **Why the Verifier Cannot Handle This**: The Linux kernel verifier has no concept of application users, session roles, prompt injection, or business logic authorization.

### Boundary 2: Executable Safety Gate ([Established in Lineage Excavations])
* **Owner**: BPF Static Verifier (Kernel Space).
* **Responsibility**: Proves memory isolation, null-pointer safety, instruction termination bounds, and type correctness. It asks: *Will this bytecode dereference arbitrary kernel memory or cause an infinite loop?*
* **Why Model Alignment Cannot Handle This**: Fine-tuning or system prompts cannot mathematically prove that generated machine code won't trigger a kernel panic, race condition, or out-of-bounds read.

---

## 8. Maps and Event Streams as AI–Kernel Interface

The interaction between an LLM and the Linux kernel must not occur via raw memory access or unconstrained terminal text streams. Instead, **BPF Maps and Ring Buffers** serve as typed, stateful, and controlled observation channels.

```text
  [ Kernel Event (e.g., sys_enter_execve) ]
                     │
                     ▼
  [ Verified eBPF Program ] ──► Write to BPF Ring Buffer (BPF_MAP_TYPE_RINGBUF)
                                           │
                                           ▼
  [ Capability Broker ]    ◄── Poll Ring Buffer & Aggregate Events (100 Hz ──► 1 Hz)
         │
         ▼ (Sanitized JSON Summary)
  [ llama.cpp Model Context ] ──► "Executed 42 processes in 1s; top binary: /usr/bin/python"
```

### Structural Advantages of Map-Backed Observation ([Engineering Inference])
1. **Decoupled Asynchrony**: eBPF programs write to lockless ring buffers at nanosecond kernel event frequencies. The Capability Broker polls buffers asynchronously, windowing and aggregating thousands of raw events into concise metric summaries before presenting them to the model context.
2. **Context Flooding Mitigation**: Direct terminal or log streaming quickly overwhelms the finite context window of local LLMs (e.g., 4K–32K tokens in local GGUF deployments). BPF map aggregations (`BPF_MAP_TYPE_HASH`, `BPF_MAP_TYPE_PERCPU_ARRAY`) compress raw execution events into bounded statistical summaries.
3. **Typed Isolation**: BPF maps enforce fixed C-struct layouts. The model receives validated key-value dictionaries rather than raw, unparsed kernel memory pages.

---

## 9. Helpers and Attach Points as Constrained Machine ABI

Traditional agentic LLMs execute system interactions by invoking unconstrained shell environments (e.g., `/bin/bash` or `subprocess`). This exposes the full ambient authority of the host user account. In contrast, eBPF restricts execution to a **constrained, gated machine ABI**.

```text
  Unrestricted Shell Agent Path (High Danger):
  LLM ──► bash ──► arbitrary system calls, file mutation, network sockets, system reboot

  eBPF Capability Runtime Path (Constrained ABI):
  LLM ──► Broker ──► BPF Map Lookup / Attach ──► Gated Helper Table ──► Isolated Event
```

### Attach Point Boundaries ([Established in Lineage Excavations])
eBPF programs are bound to specific, immutable attach points (`BPF_PROG_TYPE_KPROBE`, `BPF_PROG_TYPE_TRACEPOINT`, `BPF_PROG_TYPE_XDP`, `BPF_PROG_TYPE_LSM`). An eBPF program attached to a network tracepoint physically cannot write to disk files or terminate arbitrary process trees unless explicit helper functions (`bpf_override_return` or LSM mutators) are exposed and authorized.

### Helper Function Gating ([Established in Lineage Excavations])
eBPF bytecode cannot call arbitrary kernel symbols. Execution is restricted to the kernel's helper function table (`bpf_map_lookup_elem`, `bpf_ktime_get_ns`, `bpf_probe_read_kernel`). This provides an unforgeable, instruction-level sandbox inside supervisor address space.

---

## 10. End-to-End Execution Example (Observation-First)

To demonstrate the concrete mechanics of the proposed runtime, we trace an end-to-end, observation-first execution flow:

```text
 [1. User Prompt] ──► "Monitor TCP connection latency on port 443 for 5 seconds."
        │
        ▼
 [2. llama.cpp / GGUF Model] Generates Structured Schema Call:
        {
          "capability": "observe_socket_latency",
          "parameters": { "port": 443, "duration_sec": 5 }
        }
        │
        ▼
 [3. Capability Broker Intercepts Request]
        ├─ A. Schema Check: Validates parameter types (port=int, duration=int).
        ├─ B. Policy Check: Confirms session token holds 'net_observe' authority.
        └─ C. Registry Lookup: Retrieves pre-compiled 'tcp_latency.bpf.o'.
        │
        ▼
 [4. Kernel Verification & Link]
        ├─ A. Broker submits bytecode via bpf(BPF_PROG_LOAD).
        ├─ B. Kernel Verifier proves safety and JIT-compiles code.
        └─ C. Broker links program to 'tcp_probe' tracepoint.
        │
        ▼
 [5. Event Aggregation & Return Path]
        ├─ A. Kernel eBPF probe populates BPF_MAP_TYPE_HASH with latency buckets.
        ├─ B. Broker polls map after 5 seconds and unlinks probe.
        └─ C. Broker formats summary JSON:
              { "port": 443, "total_conns": 128, "avg_rtt_ms": 14.2, "p99_rtt_ms": 42.1 }
        │
        ▼
 [6. LLM Context Ingestion]
        Model ingests JSON summary and responds to user:
        "Monitored port 443 for 5s: 128 connections observed with an average latency of 14.2ms."
```

---

## 11. Probabilistic vs Deterministic Boundary

The core thesis rests on maintaining an explicit, un-compromised boundary between probabilistic inference and deterministic verification.

```text
  PROBABILISTIC DOMAIN (Uncertain)       │    DETERMINISTIC DOMAIN (Guaranteed)
                                         │
  ┌──────────────────────────────────┐   │   ┌──────────────────────────────────┐
  │ - Token Sampling & Temperature   │   │   │ - BPF Verifier Abstract Interp.  │
  │ - Semantic Intent Formation      │   │   │ - Strict Schema Validation       │
  │ - Natural Language Synthesis     │ ──┼──►│ - BPF Map Key/Value Operations   │
  │ - Tool Selection Heuristics      │   │   │ - Cryptographic Policy Evaluation│
  │ - Flexible Fuzzy Reasoning       │   │   │ - Hardware JIT Register Math     │
  └──────────────────────────────────┘   │   └──────────────────────────────────┘
                                         │
```

### Analytical Boundary Criteria ([Engineering Inference])
* **Probabilistic Domain**: Model reasoning, context processing, natural language interaction, hypothesis formation, and candidate tool parameter generation. Operates under floating-point matrix multiplications, non-zero sampling temperatures, and statistical confidence.
* **Deterministic Domain**: Broker schema parsing, access control authorization checking, BPF bytecode verifier proofs, kernel map array indices, and JIT-compiled machine instruction execution. Operates under exact boolean logic, formal verification proofs, and deterministic kernel ABI contracts.

---

## 12. Security Model and Threat Analysis (Mandatory)

Integrating probabilistic AI models with supervisor-level kernel execution introduces critical threat surfaces that must be systematically mitigated.

```text
                          ATTACK VECTOR MAP

  [ Prompt Injection ] ──► Emits Malicious Capability Parameters
                                  │
                                  ▼
                         [ Capability Broker ] ◄── Intercepts & Rejects
                                  │
                                  ├─ Rejects invalid schema bounds
                                  ├─ Enforces rate limits
                                  └─ Evaluates POLA access policy
                                  │
                                  ▼
                         [ BPF Static Verifier ] ◄── Rejects
                                  │
                                  └─ Proves memory isolation & termination
                                  │
                                  ▼
                         [ Kernel Execution ]
```

### Detailed Threat Matrix & Mitigations

| Threat Vector | Attack Mechanism | Impact | Architectural Mitigation |
|:---|:---|:---|:---|
| **Indirect Prompt Injection** | Untrusted input in model context tricking LLM into invoking un-requested capabilities. | Unauthorized system introspection or state mutation. | **Broker Policy Isolation**: Capabilities require explicit caller session authorization tokens independent of model text state. |
| **Legitimate Capability, Malicious Parameters** | Model generates syntactically valid tool calls with extreme values (e.g., target PID 1, duration=10^9). | Denial of service, system resource exhaustion. | **Strict Schema Bounds Enforcement**: Broker schema specs enforce hard numerical boundaries (`min`, `max`, enum allowlists) before dispatch. |
| **Broker Process Compromise** | Attacker exploits vulnerability in user-space Broker binary. | Escalation to host application privileges. | **Broker Sandboxing**: Broker runs in isolated user namespace with dropped Linux capabilities (`CAP_SYS_ADMIN` restricted via `CAP_BPF`). |
| **Kernel Verifier Flaw / CVE** | Malicious eBPF program exploits kernel verifier bug to achieve arbitrary kernel write. | Complete supervisor-mode kernel compromise. | **Fixed Capability Registry**: Model cannot generate or upload raw eBPF bytecode. Only pre-compiled, signed registry binaries are permitted. |
| **Sensitive Telemetry Leakage** | eBPF probe captures sensitive data (passwords, encryption keys) from kernel memory and returns it to LLM context. | Privacy leak, credential exposure. | **Least-Privilege Return Schemas**: Broker scrubs and aggregates telemetry data, stripping raw memory buffers before context insertion. |
| **Context Flooding DoS** | High-frequency kernel event streams flood LLM prompt context with millions of tokens. | Runtime stall, context window exhaustion, excessive memory costs. | **Broker Event Aggregators**: Mandatory sliding-window rate limiters and map-based statistical reducers. |
| **Over-Privilege via Observation** | Read-only observation capability exposes internal system layout enabling secondary exploits. | Information disclosure, attack surface mapping. | **Fine-Grained Role-Based Access Control**: Strict scope isolation per session key. |

### Derived Mandatory Design Rules ([Proposed Architecture])
1. **Fixed Registry Before Generative Code**: Models are strictly restricted to selecting pre-verified capability programs from an audited registry. Dynamic generation of eBPF C code by LLMs is forbidden in production environments.
2. **Least-Privilege Return Schemas**: Raw kernel structure dumps (`struct task_struct`, `struct sk_buff`) are never returned to the model. Return schemas must expose only aggregated, non-sensitive metrics.
3. **Out-of-Band Audit Logging**: Audit trails must be written directly to secure system storage outside the model's read/write context.
4. **No Model-Authored Policy**: Authorization policy matrices must be defined by human system administrators in static configuration files, never generated dynamically by the model.

---

## 13. Constraint Migration Reading

The emergence of the proposed AI capability runtime is explained through the lens of **[Constraint Migration](../patterns/constraint-migration.md)**:

```text
                               CONSTRAINT MIGRATION PATH

  Cloud API Latency & Privacy Boundaries (2022)
       │
       ▼
  Local Model Execution & Memory-Bandwidth Bottlenecks (March 2023: llama.cpp / GGUF)
       │
       ▼
  Unconstrained Agentic Shell Access Risks (2023–2024: Bash Agent Compromises)
       │
       ▼
  PROPOSED SOLUTION: Verifier-Constrained In-Kernel Capability Runtimes (eBPF + Broker)
```

1. **Cloud API & Privacy Bottlenecks (2022–2023)**: Remote API dependencies created privacy and latency barriers, driving the migration toward local model execution ([llama.cpp](../excavations/llama-cpp.md)).
2. **Local Memory-Bandwidth & Resource Limits (2023)**: Local LLMs were constrained by system RAM bandwidth, resolved by block-wise integer quantization and memory-mapped GGUF containers.
3. **Agentic Authority Wall (2023–2024)**: Giving local models unconstrained shell tools (`/bin/bash`) resulted in prompt-injection exploits, accidental file deletion, and arbitrary process termination.
4. **The Verified Substrate Pivot (Proposed)**: System safety constraints force the migration from unconstrained user-space shell tools toward **verifier-enforced in-kernel capability execution**, using eBPF maps and helpers to provide auditable machine interaction.

---

## 14. Recurring Ideas and Pattern Links

This synthesis maps onto several fundamental Digital Archaeology patterns:

* **[Constraint Migration](../patterns/constraint-migration.md)**: Demonstrates how shifting bottlenecks (from compute availability to security boundaries) resurrect abandoned low-level safety models.
* **[Recurring Ideas](../patterns/recurring-ideas.md)**: Re-applies the classic operating system pattern of **restricted in-system bytecode execution** (cBPF $\to$ eBPF $\to$ WebAssembly) as a safety governor for probabilistic agents.
* **[Capability-Based Security](capability-based-security.md) & [Capability Systems](../excavations/capability-systems.md)**: Adapts the classical KeyKOS/CHERI unforgeable token model to modern local AI tool-use, enforcing the Principle of Least Authority.
* **[Heterogeneous Revival](../patterns/heterogeneous-revival.md)**: Combines modern AI local runtimes ([llama.cpp](../excavations/llama-cpp.md)) with verified kernel virtual machines ([eBPF](../excavations/ebpf.md)) into a unified hybrid substrate.

---

## 15. Comparative Analysis

The table below contrasts ordinary LLM tool calling, unrestricted shell/root agents, and the proposed GGUF + Broker + eBPF capability runtime:

| Dimension | Normal LLM Tools (JSON/APIs) | Shell / Root Agent (`/bin/bash`) | Proposed GGUF + Broker + eBPF |
|:---|:---|:---|:---|
| **Trust Boundary** | Application user space (Soft JSON API contracts). | Ambient authority of user account (Unconstrained OS access). | **Dual Trust Boundary** (User-space Broker Policy + Kernel Verifier Proofs). |
| **Kernel Exposure** | Indirect via user-space application libraries. | Direct, unmonitored system call exposure. | **Gated Kernel Hook Surface** (`XDP`, `tracepoints`, `LSM` via verified helpers). |
| **Auditability** | High-level application logs (vulnerable to model manipulation). | Fragile shell history logs (easily bypassed or erased). | **Non-Repudiable In-Kernel Audit** (Ring-buffer logs outside model context). |
| **Portability** | Bound to external cloud APIs or local Python runtimes. | Posix shell-dependent; non-portable across platform ABIs. | **High Portability** (GGUF `mmap` containers + eBPF CO-RE/BTF relocations). |
| **Expressiveness** | High semantic flexibility; low real-time system visibility. | Total, un-monitored system expressiveness. | **Constrained High-Precision Substrate** (Real-time telemetry & LSM security). |
| **Failure Modes** | Hallucinated API calls, malformed JSON schemas. | Shell injection, accidental `rm -rf`, system crash. | **Safe Rejection** (Broker schema drop or verifier bytecode load failure). |

---

## 16. Reconstruction Roadmap (Research-Safe Order)

To validate this proposed architecture without creating security risks, we outline a six-phase, research-safe reconstruction roadmap:

```text
  Phase 1: Mock Broker + Fixed Schemas + Simulated Events (No Kernel)
     │
     ▼
  Phase 2: Single Read-Only eBPF Observer + Ring Buffer ──► Broker ──► Context
     │
     ▼
  Phase 3: Map-Backed Aggregation (Hash/Array Summaries)
     │
     ▼
  Phase 4: Event-Driven Context Updates with Rate Limiting & Sampling
     │
     ▼
  Phase 5: Model-Generated Parameters under Strict Schema Bounds Validation
     │
     ▼
  Phase 6 [SPECULATIVE RESEARCH FRONTIER]: Model-Assisted eBPF Generation
          (Strictly gated by Verifier + Mandatory Human-in-the-Loop Review)
```

* **Phase 1 (Mock Sandbox)**: Implement a pure Python/C++ mock Broker simulating eBPF map lookups and schema validation without loading actual kernel bytecode.
* **Phase 2 (Read-Only Observer)**: Integrate a single read-only eBPF tracepoint program (`sys_enter_execve`) outputting to a BPF ring buffer, consumed by the Broker and formatted for llama.cpp context.
* **Phase 3 (Map Aggregation)**: Implement kernel-side map aggregation (`BPF_MAP_TYPE_HASH`) to summarize event counts in kernel space before polling.
* **Phase 4 (Dynamic Sampling)**: Add adaptive sliding-window rate limiters to the Broker to handle high-concurrency event bursts gracefully.
* **Phase 5 (Bounded Parameterization)**: Allow the local model to generate dynamic filter parameters (e.g., target port numbers or user IDs) checked strictly against Broker schema limits.
* **Phase 6 (Speculative Frontier)**: Research-only exploration of LLM-generated eBPF C code, strictly gated by Clang compilation, static BPF verification, container sandboxing, and explicit human authorization before kernel submission.

---

## 17. Knowledge-Graph Proposals

To integrate this synthesis into the Digital Archaeology Knowledge Graph (`modern-relevance/knowledge_graph.json`), we propose the following honest, non-inflated relationships:

```json
[
  {
    "source": "ai_capability_runtime",
    "target": "tool_calling",
    "relationship": "extends"
  },
  {
    "source": "ai_capability_runtime",
    "target": "llama_cpp",
    "relationship": "loads_model_via"
  },
  {
    "source": "ai_capability_runtime",
    "target": "ebpf",
    "relationship": "uses_verified_substrate"
  },
  {
    "source": "capability_broker",
    "target": "ai_capability_runtime",
    "relationship": "mediates_dispatch_for"
  },
  {
    "source": "gguf",
    "target": "ebpf",
    "relationship": "architecturally_composable_with"
  }
]
```

### Expressly Forbidden Edges ([Epistemic Discipline])
* `GGUF` **contains** `eBPF` *(False: Formats are distinct and separate).*
* `LLM` **executes_in** `kernel` *(False: Neural inference runs in user space/accelerator RAM).*
* `eBPF` **implements** `alignment` *(False: Alignment is statistical model training; eBPF is executable bytecode verification).*

---

## 18. Research Questions

1. **Can eBPF map aggregation scale to maintain low-latency LLM context freshness during high-concurrency kernel event bursts?**
2. **How do BPF Static Verifier exploration limits constrain the complexity of parameter-driven eBPF probes in local capability runtimes?**
3. **What minimum user-space sandbox primitives are required for the Capability Broker process to prevent privilege escalation if the Broker itself is compromised?**
4. **Can fine-grained LSM-BPF hooks effectively restrict local AI agents from accessing sensitive user files while preserving read-only diagnostic visibility?**

---

## 19. Limitations and Uncertainties

* **Linux Kernel Lock-In**: eBPF is deeply coupled to the Linux kernel ABI (`vmlinux` BTF, `struct pt_regs`). Implementing this capability runtime on macOS or Windows requires emulation layers or platform-specific driver abstractions.
* **Local Inference Memory Pressure**: Running a 7B/13B parameter GGUF model alongside active eBPF ring buffer pollers and Broker daemons imposes memory and CPU contention on resource-constrained edge devices.
* **Verifier Rejection Overhead**: BPF verifier path exploration can reject valid, complex eBPF programs, creating developer friction when expanding capability registries.

---

## 20. Bibliography

1. McCanne, S., & Jacobson, V. (1993). *The BSD Packet Filter: A New Architecture for User-level Packet Capture*. Proceedings of the USENIX Winter 1993 Conference.
2. Starovoitov, A. (2014). *Extended BPF Architectural Specifications and Kernel Commit Logs*. Linux Kernel Mainline Repository.
3. Gerganov, G. (2023). *llama.cpp: Port of Facebook's LLaMA model in pure C/C++*. GitHub Repository.
4. Gregg, B. (2019). *BPF Performance Tools: Linux System and Application Observability*. Addison-Wesley.
5. Watson, R. N. M., et al. (2015). *Fast Capability-Based Memory Protection using CHERI*. Proceedings of the IEEE Symposium on Security and Privacy (S&P).
6. Hardy, N. (1985). *KeyKOS Architecture*. Operating Systems Review, 19(4), 8-25.
7. Open-Source Digital Archaeology Initiative. (2026). *eBPF Substrate Excavation*. `excavations/ebpf.md`.
8. Open-Source Digital Archaeology Initiative. (2026). *llama.cpp Excavation*. `excavations/llama-cpp.md`.
9. Open-Source Digital Archaeology Initiative. (2026). *Capability-Based Security Synthesis*. `synthesis/capability-based-security.md`.

---

## 21. Cross-Links

* **[Large Language Models Excavation](../excavations/large-language-models.md)** — Neural sequence prediction and tool-calling interfaces.
* **[llama.cpp Excavation](../excavations/llama-cpp.md)** — Quantization-first execution and GGUF containers.
* **[eBPF Substrate Excavation](../excavations/ebpf.md)** — In-kernel virtual machines, static verifiers, and BPF maps.
* **[Linux Substrate Excavation](../excavations/linux.md)** — Kernel system call interfaces and event hooks.
* **[Capability-Based Security Synthesis](capability-based-security.md)** — Hardware and software object capabilities.
* **[Constraint Migration Pattern](../patterns/constraint-migration.md)** — Physical and architectural bottleneck shifts.
* **[Recurring Ideas Pattern](../patterns/recurring-ideas.md)** — Cyclical return of restricted in-system VM runtimes.
* **[Heterogeneous Revival Pattern](../patterns/heterogeneous-revival.md)** — Co-design of hybrid execution substrates.

---

**Last updated**: August 26, 2026
