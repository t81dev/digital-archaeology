# Digital Archaeology Annotated Bibliography

Welcome to the **Digital Archaeology Annotated Bibliography**. This directory serves as the academically rigorous, primary-source-backed bedrock supporting all 35 excavations, synthesis essays, and modern-relevance assessments within the repository.

By prioritizing original patents, technical manuals, seminal conference papers, and developer-level specifications over secondary popular accounts, the project maintains an authoritative and precise record of computer science and systems history.

---

## Directory Organization

The bibliography is partitioned into three specialized reference documents:

1. **[Seminal Books](books.md)**: Annotates 25 monumental textbooks, research monographs, and manual codices spanning hardware architectures, capability-based security, programming language runtimes, and physical physical/mathematical foundations.
2. **[Landmark Research Papers](papers.md)**: Indexes 36 foundational publications, technical reports, and academic papers that originally introduced or rigorously analyzed non-von Neumann models, distributed single-level-store environments, and post-CMOS computing paradigms.
3. **[Technical & Historical Archives](archives.md)**: Catalogues 16 essential institutional databases, patent search collections, digitized retrocomputing manual repositories (e.g., Bitsavers, CHM), and machine-specific community history registries.

---

## Academic Citation & Entry Style

Every entry in this bibliography utilizes a standardized, machine-friendly, and human-readable template to ensure clarity, completeness, and instant cross-referencing:

```markdown
#### N. *Title of the Source*
* **Authors**: Full list of designers, engineers, or academic researchers.
* **Published**: Journal, Conference, or Publisher, Year (with Volume/Issue details if applicable).
* **Relevance**: [Excavation Name](../excavations/multics.md), [Another](../excavations/plan-9.md)
* **Description**: A 2-to-4 sentence precise summary explaining the source's technical contribution and why it is foundational for Digital Archaeology.
```

*Example Entry*:
```markdown
#### 14. *The Protection of Information in Computer Systems*
* **Authors**: Jerome H. Saltzer, Michael D. Schroeder
* **Published**: *Proceedings of the IEEE*, 1975 (Volume 63, Issue 9)
* **Relevance**: [Multics](../excavations/multics.md), [Capability Systems](../excavations/capability-systems.md)
* **Description**: A classic system security paper outlining design principles for secure operating systems, drawing heavily on lessons from Multics and early descriptor-based memory protection.
```

---

## Relative Link Mechanics

To bypass directory traversal limitations and maintain structural sanity across different documentation environments (such as MkDocs, GitHub, and local editors), **all internal links are strictly relative**.

- Relevance links from this directory point upward and into the excavations: `../excavations/` (e.g. `[Multics](../excavations/multics.md)`).
- Excavation and synthesis files link directly to bibliography components: `[Recommended Books](../bibliography/books.md)` or `[Landmark Papers](../bibliography/papers.md)`.
- A machine-readable knowledge graph mapping these relationships dynamically is compiled in `modern-relevance/knowledge_graph.json` via the automated pipeline.

---

## Core Lineage Mapping

Each bibliography category directly feeds into one or more of our six core architectural lineages:

| Lineage | Supported Excavation Files | Key Primary Bibliography Sources |
| :--- | :--- | :--- |
| **Spatial & Dataflow** | `dataflow-computing.md`, `edge-architecture.md`, `systolic-arrays.md`, `transputers.md` | Dennis (1975), Arvind (1980), Sankaralingam (2003), Gurd (1985), Mead & Conway (1980) |
| **Neuro-Stochastic** | `neuromorphic-hardware.md`, `stochastic-computing.md`, `associative-processors.md` | Carver Mead (1990), Brian Gaines (1969), Kenneth Batcher (1983) |
| **Capability & Security** | `capability-systems.md`, `burroughs-large-systems.md`, `intel-iapx-432.md` | Henry Levy (1984), Saltzer & Schroeder (1975), Watson (2014), Wilkes & Needham (1979) |
| **Physical & Reversible** | `analog-computing.md`, `optical-computing.md`, `reversible-computing.md`, `balanced-ternary.md` | Rolf Landauer (1961), Charles Bennett (1973), Fredkin & Toffoli (1982), David Rine (1977), Alan Huang (1984) |
| **Distributed & SLS OS** | `plan-9.md`, `inferno.md`, `linda-tuple-spaces.md`, `multics.md` | Rob Pike (1995), David Gelernter (1985), Elliott Organick (1972) |
| **Superconducting** | `superconducting-cryogenic.md` | Likharev & Semenov (1991), Van Duzer & Turner (1981) |

---

## Contribution Guidelines

We enforce a strict policy of academic accuracy:
- **No invented citations**: All patents, manual identifiers, volume/issue numbers, and publication details must be verified.
- **Earliest authoritative source**: Favor original workshop proceedings or first-edition technical reports over modern pop-science articles or secondary wiki pages.
- **Linter compliance**: Ensure all additions maintain perfect relative Markdown pathway integrity by running:
  ```bash
  python3 tools/verify_excavations.py
  ```
