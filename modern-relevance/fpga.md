# FPGA Prototyping & Reconfigurable Computing

> *Modern programmable logic as a time machine for testing forgotten architectures.*

---

## Summary

Field-Programmable Gate Arrays (FPGAs) have evolved from niche glue logic devices into powerful platforms for hardware experimentation. They provide an unprecedented ability to test and iterate on historical computing ideas without the enormous cost and risk of building custom ASICs.

For Digital Archaeology, FPGAs serve as one of the most practical tools for moving from theoretical reconstruction to working prototypes.

---

## Historical Context

Early FPGAs (1980s–1990s) were relatively small and slow, limiting them to simple glue logic or small state machines. Modern FPGAs (Xilinx/AMD UltraScale+, Intel Stratix/Agilex, Lattice, etc.) offer:

- Millions of logic elements
- High-speed transceivers
- Massive on-chip memory (BRAM + UltraRAM)
- DSP slices and AI-optimized blocks
- Partial reconfiguration and dynamic function exchange

This leap in capacity makes it feasible to implement complex historical architectures that were previously only theoretical or limited to small demonstrations.

---

## Modern Relevance

FPGAs have become a bridge between forgotten ideas and practical evaluation:

### Key Advantages for Digital Archaeology

- **Rapid prototyping** — Implement Balanced Ternary, dataflow processors, or Transputer-like networks in days or weeks instead of years.
- **Low cost experimentation** — Test radical designs without tape-out expenses.
- **Mixed-radix and exotic arithmetic** — Easy to build custom number systems (ternary, posits, logarithmic, residue numbers).
- **Fine-grained parallelism** — Natural platform for dataflow, tagged architectures, and lightweight process models.
- **Hybrid systems** — Combine a soft-core RISC-V or ARM with custom accelerators on the same chip.
- **Realistic performance measurement** — Obtain actual timing, power, and resource usage data.

---

## Promising Use Cases

- **Balanced Ternary processors** — Full implementation with evaluation against binary equivalents.
- **Dataflow architectures** — Modern reincarnations of MIT Tagged-Token or Manchester-style machines.
- **Lisp Machine subsets** — Hardware support for tagged memory, fast GC, and symbolic operations.
- **Transputer-inspired networks** — Mesh or torus networks of lightweight cores with CSP-style communication.
- **Mixed hardware** — Binary control plane + ternary/dataflow numerical plane.
- **Neuromorphic & spiking systems** — Exploring alternatives to standard deep learning hardware.

---

## Current Limitations & Challenges

- **Clock speed gap** — FPGAs still run slower than modern ASICs (typically 100–500 MHz vs. GHz+).
- **Toolchain complexity** — Steep learning curve compared to software development.
- **Resource efficiency** — Implementing certain structures (e.g., wide memory buses) can be expensive on FPGA fabric.
- **Programming model** — HDLs (Verilog/VHDL) or high-level synthesis tools still lag behind software productivity.

Despite these limitations, FPGAs remain the best practical platform available for architectural exploration.

---

## Lessons Learned

1. Many historical ideas failed due to manufacturing constraints that FPGAs largely bypass.
2. Reconfigurability itself is a powerful feature — the ability to change architecture at runtime opens new possibilities.
3. FPGAs accelerate the “Evaluate” and “Synthesize” steps of the Digital Archaeology methodology.
4. The barrier between “academic curiosity” and “working prototype” has never been lower.

As FPGA tools improve (especially with better high-level synthesis and AI-assisted design), the pace of meaningful architectural rediscovery will only increase.

---

## Related Excavations
- [Balanced Ternary](../excavations/balanced-ternary.md)
- [Dataflow Computing](../excavations/dataflow-computing.md)
- [Lisp Machines](../excavations/lisp-machines.md)
- [Transputers](../excavations/transputers.md)
- [Systolic Arrays](../excavations/systolic-arrays.md)
- [Connection Machine](../excavations/connection-machine.md)

## Related Patterns
- Forgotten Abstractions
- Recurring Ideas
- Economic Failures

---

## References
- AMD Xilinx & Intel FPGA documentation and whitepapers.
- Academic projects implementing historical architectures on modern FPGAs.
- High-Level Synthesis (HLS) tools research.
- Papers on reconfigurable computing architectures.