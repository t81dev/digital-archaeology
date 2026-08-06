# Mixed-Radix Computing

> *Using different number systems and arithmetic representations within the same machine — moving beyond the binary monoculture.*

---

## Summary

Mixed-radix computing refers to heterogeneous systems that combine multiple numerical representations (binary, ternary, quaternary, posits, logarithmic, residue numbers, etc.) rather than forcing everything into a single base. Different parts of the system use the representation best suited to their workload.

This approach leverages the strengths of specialized arithmetic while maintaining compatibility with existing binary infrastructure.

---

## Historical Context

Most historical machines committed to a single number system (almost always binary after the 1960s). However, several experimental systems explored alternatives:

- Balanced ternary (Setun)
- Decimal machines
- Residue Number Systems (RNS)
- Early proposals for hybrid analog-digital or multi-valued logic

These efforts were largely abandoned due to manufacturing complexity and ecosystem pressure. Today, the constraints have shifted.

---

## Modern Relevance

Modern hardware and AI workloads create fertile ground for mixed-radix designs:

- **Transistors are cheap**, but data movement and power are expensive.
- **AI accelerators** already use specialized low-precision formats (INT8, FP16, BF16, INT4, etc.).
- **Domain-specific architectures** justify the complexity of multiple representations.
- **Heterogeneous systems** (CPU + GPU + NPU + FPGA) already mix different execution models — extending this to number systems is a natural evolution.

---

## Opportunities

### Within AI Systems
- Binary for control logic and high-precision training.
- Ternary or multi-valued logic for low-precision inference or activation functions.
- Logarithmic or posit formats for better dynamic range in certain layers.
- Stochastic or approximate computing in noise-tolerant parts of the network, evaluated via our [Stochastic Computing Simulator](../reconstructions/stochastic-computing/).

### Hybrid Numerical Units
- A CPU with binary main ALUs + attached mixed-radix coprocessors.
- FPGA-based accelerators that switch between or combine multiple radices.
- Memory systems that store data in compressed or alternative formats while presenting binary interfaces.

### Specific Historical Revivals
- **Balanced Ternary** as a specialized arithmetic unit for symmetric operations or certain neural computations. Play with three-state balanced arithmetic modeling using our [ternary_sim.py](../reconstructions/mixed-radix-sim/ternary_sim.py) simulator or study the RTL in [ternary_alu.sv](../reconstructions/synthesizable-hardware/ternary_alu.sv).
- **Dataflow engines** using non-binary representations internally, such as the [Dataflow Simulator](../reconstructions/dataflow-engine/).
- **Transputer-like nodes** with custom arithmetic tuned per node type.

---

## Advantages

- Better performance-per-watt for targeted workloads.
- More efficient representation of data (e.g., higher information density in ternary).
- Natural fit for hybrid symbolic-numeric AI systems.
- Incremental adoption path — can be added as accelerators rather than full CPU replacement.

---

## Challenges

- **Data conversion overhead** between radices.
- Increased design and verification complexity.
- Toolchain and compiler support (most compilers assume binary).
- Debugging difficulty in heterogeneous numerical environments.
- Standards and ecosystem fragmentation.

---

## Lessons Learned

The long dominance of binary was largely an accident of history and manufacturing, not proof of universal superiority. As specialization becomes the dominant strategy in high-value domains (especially AI), mixed-radix computing becomes not only viable but attractive.

It represents a mature evolution of the “Forgotten Abstractions” pattern: instead of replacing binary entirely, we intelligently combine multiple systems where each excels.

This approach may be one of the most practical ways to bring historical numerical innovations into mainstream computing.

---

## Related Excavations
- [Balanced Ternary](../excavations/balanced-ternary.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Lisp Machines](../excavations/lisp-machines.md)
- [Transputers](../excavations/transputers.md)

## Related Patterns
- Forgotten Abstractions
- Recurring Ideas
- Economic Failures

---

## References
- Research on Posit arithmetic, multiple-valued logic (MVL), and hybrid number systems in AI.
- Papers on heterogeneous computing and domain-specific accelerators.
- Historical analyses of Setun and other non-binary machines.
- Modern FPGA implementations of mixed-radix systems.