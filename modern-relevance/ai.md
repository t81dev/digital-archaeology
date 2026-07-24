# AI

> *Modern artificial intelligence creates new opportunities to re-evaluate forgotten computing architectures and ideas.*

---

## Summary

The explosive growth of AI — particularly deep learning, hybrid neuro-symbolic systems, and large-scale training — has dramatically changed the constraints that doomed many historical ideas. What was impractical or uneconomical in the 1960s–1990s can become compelling when compute is abundant, specialized hardware is feasible, and the value of new capabilities is extremely high.

This page examines how the ideas excavated in this project intersect with contemporary AI research and engineering.

---

## Why AI Changes the Equation

Modern AI workloads differ fundamentally from traditional general-purpose computing:

- Extreme parallelism and data movement are central.
- Approximate computing is often acceptable.
- Enormous investment justifies custom silicon and novel number systems.
- Hybrid symbolic + statistical approaches are regaining traction.
- Energy efficiency and specialized operations have become critical.

These shifts reopen the door for architectures and techniques that previously lost out to binary von Neumann dominance.

---

## Relevance of Excavated Ideas

### Balanced Ternary
Ternary logic and balanced representations may offer advantages in low-precision AI inference or probabilistic computing. The natural symmetry around zero could benefit certain activation functions or signed arithmetic common in neural networks. With cheap transistors and FPGA prototyping, mixed-radix or ternary co-processors are more realistic today.

### Dataflow Computing
Deep learning is inherently dataflow-oriented. Modern frameworks (TensorFlow, PyTorch, JAX) compile models into dataflow graphs. Many AI accelerators (Google TPU, Grok chips, Graphcore IPUs, Cerebras) use dataflow-inspired scheduling and execution. The old dream of efficient dataflow hardware is partially realized in today’s AI silicon.

### Lisp Machines
The resurgence of interest in symbolic AI, neuro-symbolic hybrids, and differentiable programming revives demand for efficient symbolic manipulation. Lessons from Lisp Machines — tagged architectures, hardware garbage collection, seamless language-hardware integration, and powerful interactive environments — remain relevant for building next-generation AI development systems and knowledge engines.

### Transputers
The Transputer’s emphasis on lightweight processes and efficient message passing directly prefigures modern actor models, Go’s concurrency, and distributed training systems. Network-on-chip designs and many-core AI chips (e.g., SpiNNaker for neuromorphic computing) echo Transputer philosophy. Communication remains the bottleneck in large-scale AI training — a problem the Transputer tackled head-on.

---

## Emerging Opportunities

- **Alternative number systems** — Posits, logarithmic number systems, balanced ternary, and stochastic computing for more efficient low-precision AI.
- **Neuromorphic & event-based systems** — Dataflow and asynchronous designs that align with spiking neural networks.
- **Symbolic & hybrid architectures** — Hardware support for fast inference over knowledge graphs and logical reasoning.
- **Reconfigurable computing** — FPGAs and CGRA for rapid experimentation with exotic architectures tailored to new AI paradigms.
- **Massively parallel fine-grained concurrency** — Hardware support for millions of lightweight processes or agents.

---

## Lessons for AI Development

1. **History is worth revisiting** — Many “failed” ideas were limited by economics and technology of their time, not fundamental flaws.
2. **Specialization wins in AI** — The high value of AI capabilities justifies domain-specific architectures more than general-purpose computing ever did.
3. **Software-hardware co-design** — Deep integration (as seen in Lisp Machines and Transputers) can yield massive productivity and efficiency gains.
4. **Communication and data movement** — Often more important than raw arithmetic throughput.
5. **Diversity of representations** — Binary is not sacred. AI may drive wider exploration of number systems and execution models.

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
- Ecosystem Lock-In

---

## References
- Surveys on alternative number systems in AI hardware (Posits, ternary, logarithmic).
- Papers on neuro-symbolic AI and hybrid architectures.
- Documentation from modern AI accelerators (TPU, IPU, Grok, etc.).
- Historical comparisons between dataflow machines and contemporary graph execution engines.