# Systolic Arrays

> Regular, pipelined grids of simple processing elements where data flows rhythmically through the architecture like blood through the heart—highly efficient for dense, compute-bound workloads such as matrix operations.

---

## Summary

Systolic arrays are a class of parallel computing architectures consisting of a grid (usually 1D or 2D) of modestly capable processing elements (PEs) connected locally. Data and partial results flow synchronously through the array in a rhythmic, pipelined fashion, with each PE performing a small operation (e.g., multiply-accumulate) on passing values and forwarding results to neighbors. 

Proposed by H.T. Kung and Charles E. Leiserson in the late 1970s, systolic arrays were designed to exploit VLSI fabrication for high-throughput, low-overhead computation on regular dataflows. They excel at algorithms with high data locality and repetitive operations, such as matrix multiplication, convolution, filtering, and linear algebra. While dedicated systolic hardware saw limited commercial success outside specialized domains (signal processing, radar, early image processing), the underlying principles heavily influence modern tensor cores in GPUs, AI accelerators (e.g., Google TPU variants), and coarse-grained reconfigurable arrays.

---

## Historical Context & Concrete Metrics

The late 1970s marked a peak of research into parallel architectures as researchers sought alternatives to von Neumann bottlenecks amid the rise of VLSI. In their seminal 1978–1982 papers, H.T. Kung and Charles E. Leiserson formalized systolic algorithms and architectures, showing how complex computations could be decomposed into localized, rhythmic data movements that map elegantly onto silicon grids.

### Key Historical Milestones & Metrics

1. **CMU Warp (1984–1986)**:
   - **Form Factor**: A 10-node linear systolic array developed by Carnegie Mellon University and built by GE and Honeywell.
   - **Throughput**: Achieved 100 MFLOPS (10 MFLOPS per PE).
   - **Technology**: Built using off-the-shelf components, including Weitek floating-point chips.
   - **Power & Size**: A full Warp machine, including host and interface units, consumed several kilowatts and filled a standard 19-inch rack.
   - **Application**: Real-time road tracking for the CMU Terregator autonomous vehicle.

2. **Intel-CMU iWarp (1988–1990)**:
   - **Fabrication Node**: 1.2-micron CMOS technology.
   - **Transistor Count**: ~600,000 transistors per single-chip PE.
   - **PE Performance**: 20 MFLOPS (single/double precision) and 20 MIPS integer per node.
   - **Interconnect Bandwidth**: Four bidirectional physical links, each operating at 40 MB/s, yielding 320 MB/s aggregate bandwidth per component.
   - **System Scalability**: Typically configured as an 8x8 (64-PE) grid achieving 1.28 GFLOPS peak performance.

3. **Hughes Aircraft Radar Systolic Processor (1980s)**:
   - Developed for real-time synthetic aperture radar (SAR) and signal processing, highlighting the extreme throughput-to-volume advantages in aerospace applications.

The general-purpose computing ecosystem of the 1990s temporarily eclipsed these systems as rapid single-core CMOS scaling (Moore's Law) and massive caches outpaced custom spatial processors in general-purpose software compatibility.

---

## Technical Overview

A systolic array replaces centralized control and global memory buses with a spatial network of identical (or near-identical) processing elements. Data streams through the array in lockstep, synchronized by a global clock (or locally in wavefront variants).

### Processing Element (PE) Schematic

Each Processing Element (PE) typically contains internal registers to buffer operands ($a$, $b$), an accumulator ($c$), and a multiply-accumulate (MAC) core.

```
            b_in (from Top)
                 │
                 ▼
          ┌──────────────┐
  a_in ──►│   Multiply   │──► a_out (to Right)
 (from    │  Accumulate  │   (Buffered)
  Left)   │   (MAC)      │
          └──────────────┘
                 │
                 ▼
            b_out (to Bottom)
            (Buffered)
```

### Dataflow Topologies & Matrix Multiplication

#### 1. Weight-Stationary (WS) Dataflow
Weights ($W$) are pre-loaded into the PEs and remain stationary. Inputs ($X$) stream from the left, and partial sums ($Y$) stream from the top (or accumulate locally in registers).
- **Advantage**: Zero weight-movement energy during calculation; ideal when the same weight matrix is reused across many inputs (e.g., CNN inference).
- **Disadvantage**: Output accumulation or weight-loading overhead.

#### 2. Output-Stationary (OS) Dataflow
Accumulators ($Y$) remain stationary in local PE registers. Inputs ($X$) stream from the left, and weights ($W$) stream from the top.
- **Advantage**: Minimized partial-sum read/write energy.
- **Disadvantage**: Accumulators must eventually be read out of the array.

#### 3. Input-Stationary (IS) / Data-Stationary Dataflow
Inputs ($X$) remain stationary. Weights ($W$) and partial sums ($Y$) stream through the array.

```mermaid
graph TD
    subgraph 2D Systolic Array (Weight-Stationary Example)
    PE00[PE_0,0 <br> W_0,0] -->|X_0,0| PE01[PE_0,1 <br> W_0,1]
    PE10[PE_1,0 <br> W_1,0] -->|X_1,0| PE11[PE_1,1 <br> W_1,1]

    InY0[Y_in 0] -->|Y| PE00
    InY1[Y_in 1] -->|Y| PE01

    PE00 -->|Y| PE10
    PE01 -->|Y| PE11

    PE10 --> OutY0[Y_out 0]
    PE11 --> OutY1[Y_out 1]
    end
```

---

## Innovations & Core Architectural Claims

- **Optimal Data Reuse**: By piping data directly from PE to PE, a single memory read feeds multiple operations. This achieves the theoretical maximum of the compute-to-memory ratio ($O(N)$ operations for $O(N)$ memory transfers).
- **High Area Efficiency**: Centralized instruction decoders, rename tables, and complex bypass networks of von Neumann processors are omitted. Almost all silicon area is dedicated to arithmetic logic (ALUs).
- **Strictly Local Communication**: No global wires stretch across the chip, removing RC delay bottlenecks and enabling higher operating frequencies at lower power.
- **Algorithmic-System Co-Design**: Promoted "systolic mapping algorithms" where nested loops are systematically projected onto physical multi-dimensional space-time manifolds.

---

## Limitations & Contemporary Bottlenecks

- **Rigidity and Workload Sensitivity**: Best for highly regular, dense linear algebra. Struggles with sparse matrices, irregular control flow (if-else branches), and dynamic loop boundaries.
- **Boundary I/O Bottleneck**: The array throughput is bounded by the speed at which the boundary PEs can be fed from external memory or host buses.
- **Programming Complexity**: Mapping arbitrary mathematical formulas to a rigid spatial grid required manual, compiler-unfriendly spatial scheduling.
- **Fill/Drain Overhead**: Before computation reaches peak efficiency, the pipeline must be "filled" (latency of $O(W+H)$ cycles), and afterwards "drained," reducing utilization on small batch sizes.

---

## Modern Relevance

### Historical Fact
In the 1980s and 1990s, the standalone systolic array failed commercially. General-purpose CPUs powered by RISC pipelines and multi-level cache hierarchies scaled rapidly due to massive market demand, eclipsing specialized accelerators. The difficulty of writing software for specialized systolic engines further isolated them to military, high-end radar, and specialized image processing niches.

### Modern Evaluation
In the post-Moore's Law era, the "Memory Wall" and "Power Wall" have made data movement the dominant consumer of energy and time. Simultaneously, deep learning consolidated 90%+ of AI workloads into a single operation: General Matrix Multiplication (GEMM).

These two factors completely inverted the historical economic constraints:
- **Google TPU v1 (2016)**: Adopted a 256x256 8-bit systolic array running at 700 MHz, delivering 92 TeraOPS peak while drawing only 75W.
- **NVIDIA Tensor Cores (Volta onwards)**: Internally utilize spatial micro-systolic-like pipelines to perform dense FP16/INT8 matrix-multiply-accumulate operations within GPU streaming multiprocessors.
- **Cerebras Wafer-Scale Engine**: Implements a wafer-scale spatial mesh of 850,000+ cores utilizing dataflow-driven, systolic-style routing.

The modern consensus is that **systolic arrays did not lose the architectural war—they were simply waiting for a workload of sufficient scale to justify their specialization.**

---

## Related Technologies

### Related Excavations
- **[Dataflow Computing](../excavations/dataflow-computing.md)**: Shares the data-driven execution paradigm but usually lacks the rigid physical layout of systolic arrays.
- **[Connection Machine](../excavations/connection-machine.md)**: A fine-grained parallel computer, though relying on dynamic routing rather than static rhythmic pipelines.
- **[Transputers](../excavations/transputers.md)**: Multi-processor nodes, but optimized for message-passing concurrency (CSP) rather than sub-instruction lockstep spatial math.
- **[Vector Supercomputing](../excavations/vector-supercomputing.md)**: Relies on deep pipelines of execution units, but feeds from centralized vector registers rather than point-to-point spatial PE networks.

### Related Synthesis & Patterns
- **[The Return of Spatial Computing](../synthesis/return-of-spatial-computing.md)**: Analyzes how modern GEMM accelerators are physical reincarnations of the systolic concept.
- **[Constraint Migration](../patterns/constraint-migration.md)**: Describes how the rise of the Memory Wall revived spatial data-reuse architectures.
- **[Heterogeneous Revival](../patterns/heterogeneous-revival.md)**: Details the placement of systolic arrays as coprocessors (NPUs/TPUs) rather than standalone CPUs.
- **[Modern Relevance: AI](../modern-relevance/ai.md)**: Explains the ultimate synergy between deep learning workloads and systolic math.
- **[Modern Relevance: FPGA Prototyping](../modern-relevance/fpga.md)**: Showcases reconfigurable hardware as a deployment platform for custom systolic arrays.

---

## Scorecard

| Category | Rating | Rationale |
| --- | --- | --- |
| Historical Importance | ★★★★☆ | Foundational VLSI concept that proved spatial scalability. |
| Technical Innovation | ★★★★★ | Shifted computing paradigm from control-centric to dataflow-centric. |
| Commercial Success | ★★☆☆☆ | Originally restricted to DSP and defense niches; failed as general-purpose engines. |
| Modern Potential | ★★★★★ | Absolute core to modern AI chips, Tensor Processing Units, and edge silicon. |
| AI Synergy | ★★★★★ | The optimal physical layout for dense matrix multiplication and deep learning operations. |
| Difficulty to Recreate | ★★★★☆ | Simple in logic, but designing high-performance clocking and spatial interconnects is highly complex. |

---

## References (Selected)

- **Kung, H.T. and Leiserson, C.E.** (1978). "Systolic Arrays (for VLSI)". *Sparse Matrix Proceedings*, Carnegie Mellon University. (The original paper introducing the concept).
- **Kung, H.T.** (1982). "Why Systolic Architectures?". *IEEE Computer*, 15(1), 37-46.
- **Annaratone, M., Bitz, E., Deutch, J., Hamey, L., Kung, H. T., Maulik, P. C., Tseng, P. S., & Webb, J. A.** (1987). "The Warp Computer: Architecture, Implementation, and Performance". *IEEE Transactions on Computers*, C-36(12), 1523-1538.
- **Borkar, S., et al.** (1988). "iWarp: An integrated solution to high-speed parallel computing". *Supercomputing '88 Proceedings*.
- **Jouppi, N. P., et al.** (2017). "In-datacenter performance analysis of a tensor processing unit". *ISCA '17 Proceedings*. (Detailing Google TPU v1's systolic array).
