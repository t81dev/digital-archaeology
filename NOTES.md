## Repository Structure

```text
digital-archaeology/
│
├── README.md
├── CONTRIBUTING.md
├── LICENSE
│
├── excavations/
│   ├── README.md
│   ├── balanced-ternary.md
│   ├── capability-systems.md
│   ├── dataflow-computing.md
│   ├── lisp-machines.md
│   ├── transputers.md
│   └── ...
│
├── patterns/
│   ├── README.md
│   ├── forgotten-abstractions.md
│   ├── economic-failures.md
│   ├── ecosystem-lockin.md
│   └── recurring-ideas.md
│
├── modern-relevance/
│   ├── ai.md
│   ├── fpga.md
│   ├── mixed-radix.md
│   ├── coprocessors.md
│   └── symbolic-computing.md
│
├── timelines/
│   ├── computing.md
│   ├── ai.md
│   └── hardware.md
│
└── bibliography/
    ├── books.md
    ├── papers.md
    └── archives.md
```

## Standard Excavation Format

Every topic should follow the same structure.

```markdown
# Project Name

## Summary

Two or three paragraphs describing what it was.

---

## Historical Context

When?
Who?
Why?

---

## Technical Overview

Architecture

Strengths

Weaknesses

Innovations

---

## Why It Didn't Win

Economic?

Manufacturing?

Software?

Timing?

Politics?

---

## Modern Relevance

Could AI change this?

Would GPUs help?

Would FPGAs help?

Could custom silicon help?

---

## Lessons Learned

Bullet list

---

## References
```

That consistency makes it easy to compare very different technologies.

## A Taxonomy of Discoveries

Instead of organizing by year, organize by *what was discovered*.

* Architectures
* Operating Systems
* Programming Languages
* AI
* Hardware
* Mathematics
* Human-Computer Interaction
* Networking
* Security
* Storage
* Visualization
* Robotics
* Simulation

People tend to think chronologically, but researchers often ask conceptual questions.

## A Rating System

Every excavation could end with a scorecard.

| Category               | Rating |
| ---------------------- | ------ |
| Historical Importance  | ★★★★★  |
| Technical Innovation   | ★★★★★  |
| Commercial Success     | ★☆☆☆☆  |
| Modern Potential       | ★★★★★  |
| AI Synergy             | ★★★★★  |
| Difficulty to Recreate | ★★★☆☆  |

That would make cross-comparisons much easier.

## An "Unearthed Artifacts" Section

This is where the project becomes more than a wiki.

For every excavation, identify:

* Forgotten algorithms
* Lost design patterns
* Elegant abstractions
* Interesting engineering trade-offs
* Ideas worth reviving
* Ideas worth avoiding

This turns history into a source of actionable engineering insights.

## Long-Term Vision

Over time, the repository could evolve into a curated knowledge base that answers questions such as:

* Which ideas failed only because hardware wasn't ready?
* Which concepts deserve reimplementation with modern tools?
* Which architectural patterns keep reappearing across decades?
* Which abandoned systems anticipated today's AI workloads?
* What can we still learn from paths computing didn't take?

The result would be more than a collection of Markdown files. It would become a map of computing's unrealized possibilities—a place where historical artifacts are examined not just for what they were, but for what they might still become.
