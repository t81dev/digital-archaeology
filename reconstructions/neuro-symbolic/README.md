# Neuro-Symbolic Logic Inference Solver

> *An executable model of a hybrid AI architecture combining statistical perception (neural network outputs) with deterministic symbolic logic (forward-chaining reasoning engine).*

---

## Background

Modern Artificial Intelligence is dominated by **statistical deep learning** (neural networks and large language models). While highly capable at pattern recognition, perception, and natural language generation, these systems suffer from key drawbacks:
- **Hallucinations**: They can generate confident, yet factually incorrect or illogical claims.
- **Unverifiable Reasoning**: Their internal decision-making is a black box of high-dimensional weights, making them difficult to audit or explain.
- **Lack of Guardrails**: It is hard to mathematically guarantee that a neural network will never violate legal, safety, or business constraints.

**Neuro-[Symbolic AI](../../excavations/symbolic-ai.md)** is a hybrid paradigm that combines:
1. **The Statistical/Neural Layer (Perception)**: Excels at processing messy, raw sensor inputs (images, audio, unstructured text) and outputs probabilistic confidence scores (e.g., "92% confidence there is a package on the porch").
2. **The Symbolic/Logic Layer (Reasoning & Guardrails)**: Processes explicit, structured concepts using formal logic rules. It executes deterministic operations (like forward-chaining deduction) to guarantee logical, verifiable, and explainable decisions.

---

## Features of This Simulator

This simulator implements a complete, interactive Neuro-Symbolic system:
1. **Statistical Perception Engine**: A mock neural network that classifies video feeds of a smart-home front door (outputting confidence scores for objects, actions, and identities).
2. **Symbolic Fact Compiler**: Translates continuous confidence scores into discrete logical facts using configurable thresholding (e.g., if `confidence > 0.8` then assert fact).
3. **Forward-Chaining Logic Engine**: An expert system that matches compiled facts against a declarative Knowledge Base of rules. It iteratively derives new logical facts until a terminal action or decision is reached.
4. **Interactive Guardrail Engine**: Enforces strict safety rules (e.g., "NEVER unlock the door if an unknown person is present, even if the authorized user's face is recognized at 50% confidence").
5. **Detailed Decision Audit Trace**: Generates a complete mathematical explanation (step-by-step logical proof) of how the final action was deduced, demonstrating 100% explainability.

---

## How to Run

Execute the script from the repository root:

```bash
python3 reconstructions/neuro-symbolic/neuro_symbolic_sim.py
```

The script runs various interactive scenarios (package delivery, intrusion detection, authorized user entry with high noise) and prints the step-by-step decision auditing logs to the console.
