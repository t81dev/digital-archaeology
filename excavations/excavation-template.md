# [Topic Name]: [Subhead / Core Abstraction Statement]

> A single-sentence italicized thesis summarizing the computational model, historical constraint, and modern migration vector.

---

# Excavation Template Overview & Dual-Schema Structure

This template defines the standardized structural options for conducting excavations within the Digital Archaeology repository. Authors must choose between two complementary schemas depending on the nature of the subject under investigation:

1. **Classic Architecture Schema**: Optimized for hardware ISAs, number systems, execution models, physical logic paradigms, and discrete computing machinery (e.g., [Balanced Ternary](balanced-ternary.md), [Residue Number System](residue-number-system.md), [LNS](logarithmic-number-system.md)).
2. **Platform Substrate Schema**: Optimized for software platforms, runtimes, operating system kernels, distribution infrastructure, and developer ecosystems (e.g., [Gentoo](gentoo.md), [Portage](portage.md), [WebKit / Safari](safari.md), [Winamp](winamp.md), [Cursor IDE](cursor-ide.md)).

---

# Schema Option A: Classic Architecture Schema

```markdown
# [Technology Name]

> [Core Thesis / Architectural Paradigm]

---

## Summary
[Concise executive summary of the technology, its primary purpose, and its architectural significance.]

## Historical Context
[Origin environment, key inventors, physical constraints, and driving historical problems.]

## Technical Overview
[Detailed explanation of representation, internal mechanics, operational formulas, and core architectural abstractions.]

## Difficult Operations & Engineering Workarounds
[Known limitations, mathematical/physical edge cases, and historical workarounds.]

## Conversion & Hardware Realization
[Implementation paradigms, silicon/vacuum tube/optical layouts, and translation costs.]

## Why It Didn't Win / Reasons for Decline
[Ecosystem lock-in, carry-lookahead breakthroughs, manufacturing economics, or Moore's Law dynamics.]

## Modern Relevance & Revival Pathways
[Contemporary applications in AI, cryptography, homomorphic encryption, or non-CMOS computing.]

## Knowledge-Graph Relationships
[Formal taxonomy linking entities, dependencies, and constraints.]

## Bibliography
1. Author, A. (Year). *Title of Work*. Publisher / Journal.

## Excavation Scorecard

| Category | Rating | Rationale |
| :--- | :--- | :--- |
| Historical Importance | ★★★★☆ | Brief description of historical impact. |
| Technical Innovation | ★★★★★ | Brief description of technical elegance or novelty. |
| Commercial Success | ★★☆☆☆ | Brief description of market adoption or failure. |
| Modern Potential | ★★★★★ | Brief description of current applicability. |
| AI Synergy | ★★★★☆ | Brief description of AI/ML acceleration relevance. |
| Difficulty to Recreate | ★★★☆☆ | Brief description of reconstruction complexity. |
```

---

# Schema Option B: Platform Substrate Schema

```markdown
# [Platform Name]: [Subhead / Architectural Substrate Definition]

> [Core Thesis / Substrate Paradigm]

---

## Historical Context
[Foundational environment, ecosystem drivers, socio-technical context.]

## Archaeological Scope
[System boundary, modular component map, operational tiers.]

### 1. [Subsystem / Layer 1]
### 2. [Subsystem / Layer 2]
### 3. [Subsystem / Layer 3]

## Historical Lineage
[Key historical transitions, version shifts, and architectural evolutions.]

## Architectural Artifacts
[Primary code artifacts, file formats, ABI boundaries, and configuration interfaces.]

## Extracted Abstractions
[Decoupled engineering principles extracted from the platform for modern re-use.]

## [Platform] as a Computational / Platform Machine
[Behavioral specification, execution state machine, lifecycle model.]

## Ecosystem Lock-In & Socio-Technical Persistence
[Lock-in drivers, switching costs, ecosystem network effects, and lock-out mechanisms.]

## Economic / Practical Failure vs Technical Limitation
[Disentangling technical boundaries from economic and market realities.]

## Historical Counterfactuals
[Analysis of alternative historical trajectories and untaken paths.]

## Compare [Platform] with Other Computational Lineages
[Comparative matrix evaluating tradeoffs against contemporary alternatives.]

## Constraint Migration
[Evolution of design constraints across physical, memory, and network boundaries.]

## Recurring Ideas & Heterogeneous Survival
[Resurfacing concepts in modern software systems and hybrid runtimes.]

## Modern Relevance
[Current production applications, descendant architectures, and modern platform influence.]

## Reconstruction Proposal
[Specification for zero-dependency simulator or behavioral reconstruction in `reconstructions/`.]

## Knowledge-Graph Relationships
[Formal taxonomy linking entities, dependencies, and constraints.]

## Research Questions
[Unresolved questions, historical ambiguities, or potential investigation paths.]

## Limitations and Uncertainties
[Known bounds of the investigation and archival gaps.]

## Excavation Scorecard

| Category | Rating | Rationale |
| :--- | :--- | :--- |
| Historical Importance | ★★★★★ | Brief description of platform significance. |
| Technical Innovation | ★★★★☆ | Brief description of substrate innovation. |
| Commercial Success | ★★★★★ | Brief description of commercial footprint. |
| Modern Potential | ★★★★☆ | Brief description of modern applicability. |
| AI Synergy | ★★★★☆ | Brief description of AI/agentic integration. |
| Difficulty to Recreate | ★★★★☆ | Brief description of reconstruction complexity. |

## Bibliography
1. Author, A. (Year). *Title of Work*. Publisher / Journal.
```

---

# Mandatory Scorecard Formatting Rules

All excavations **must** conclude with the exact 6-category scorecard table format shown below. The linter enforces strict compliance with these rules:
1. Category names in column 1 **must not be bolded** (e.g. `Historical Importance`, NOT `**Historical Importance**`).
2. Star ratings in column 2 **must contain exactly 5 unicode characters** composed of `★` (filled) and `☆` (empty).
3. Required categories (in exact order):
   - `Historical Importance`
   - `Technical Innovation`
   - `Commercial Success`
   - `Modern Potential`
   - `AI Synergy`
   - `Difficulty to Recreate`

| Category | Rating | Rationale |
| :--- | :--- | :--- |
| Historical Importance | ★★★☆☆ | [Rationale statement] |
| Technical Innovation | ★★★☆☆ | [Rationale statement] |
| Commercial Success | ★★★☆☆ | [Rationale statement] |
| Modern Potential | ★★★☆☆ | [Rationale statement] |
| AI Synergy | ★★★☆☆ | [Rationale statement] |
| Difficulty to Recreate | ★★★☆☆ | [Rationale statement] |
