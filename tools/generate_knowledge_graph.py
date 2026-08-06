#!/usr/bin/env python3
"""
Dynamic Knowledge Graph Generator for AI-Assisted Ingestion.
Parses all 35 excavations, the glossary, and the comparative index to compile
a fully structured machine-readable JSON database for LLMs and autonomous agents.
"""

import os
import re
import json

class KnowledgeGraphGenerator:
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        self.data = {
            "metadata": {
                "title": "Digital Archaeology Knowledge Graph",
                "description": "A comparative research database of forgotten and alternative computing paradigms.",
                "version": "1.1.0",
                "last_updated": "2026-08-26"
            },
            "glossary": [],
            "comparative_index": {
                "execution_models": {},
                "memory_protection_models": {},
                "concurrency_models": {}
            },
            "excavations": [],
            "synthesis_essays": [],
            "reconstructions": []
        }

    def generate(self):
        print("\n=== Generating AI-Assisted Knowledge Graph JSON Database ===")
        self.parse_glossary()
        self.parse_comparative_index()
        self.parse_excavations()
        self.parse_synthesis_essays()
        self.parse_reconstructions()

        # Write to target path
        target_dir = os.path.join(self.root_dir, "modern-relevance")
        os.makedirs(target_dir, exist_ok=True)
        target_file = os.path.join(target_dir, "knowledge_graph.json")

        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        print(f"✓ Successfully generated: {target_file}")
        return True

    def parse_glossary(self):
        print("Parsing GLOSSARY.md...")
        filepath = os.path.join(self.root_dir, "GLOSSARY.md")
        if not os.path.exists(filepath):
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract glossary list items: * **Term**: definition
        pattern = re.compile(r'^\s*\*\s*\*\*([^*]+)\*\*:\s*(.*)$', re.MULTILINE)
        matches = pattern.findall(content)

        for term, definition in matches:
            # Strip markdown links from definition if any
            clean_def = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', definition)
            self.data["glossary"].append({
                "term": term.strip(),
                "definition": clean_def.strip()
            })

    def parse_comparative_index(self):
        print("Parsing COMPARATIVE_INDEX.md...")
        filepath = os.path.join(self.root_dir, "COMPARATIVE_INDEX.md")
        if not os.path.exists(filepath):
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # We can extract the markdown tables for Execution, Memory, and Concurrency
        # Let's parse tables using basic markdown table parser
        sections = {
            "execution_models": "## 1. Index by Execution Model",
            "memory_protection_models": "## 2. Index by Memory & Protection Model",
            "concurrency_models": "## 3. Index by Concurrency & Communication Model"
        }

        for key, section_header in sections.items():
            pos = content.find(section_header)
            if pos == -1:
                continue

            # Find next header or end
            next_header = content.find("##", pos + len(section_header))
            section_content = content[pos:next_header] if next_header != -1 else content[pos:]

            # Find table rows: | Model | Description | Mapped Excavations |
            row_pattern = re.compile(r'^\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', re.MULTILINE)
            rows = row_pattern.findall(section_content)

            for model_name, desc, mapped in rows:
                # Clean up mapped excavations names
                excavation_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', mapped)
                mapped_ids = [os.path.basename(link).replace(".md", "") for text, link in excavation_links]

                self.data["comparative_index"][key][model_name.strip()] = {
                    "description": desc.strip(),
                    "mapped_excavations": mapped_ids
                }

    def parse_excavations(self):
        print("Parsing excavations...")
        excavations_dir = os.path.join(self.root_dir, "excavations")
        if not os.path.exists(excavations_dir):
            return

        for file in sorted(os.listdir(excavations_dir)):
            if not file.endswith(".md") or file in ("README.md", "excavation-template.md"):
                continue

            filepath = os.path.join(excavations_dir, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # 1. Parse Title (First H1)
            title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else file.replace(".md", "")

            # 2. Parse Summary
            summary_match = re.search(r'##\s*Summary\s*\n\s*(.*?)\n\s*(?:---|\n##)', content, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""
            # Clean up blockquote markdown if present
            summary = re.sub(r'^>\s*', '', summary, flags=re.MULTILINE)

            # 3. Parse Scorecard
            scorecard = {}
            row_pattern = re.compile(r'^\s*\|\s*([^|]+)\s*\|\s*([★☆]{5})\s*\|\s*([^|]*)\s*\|?$', re.MULTILINE)
            scorecard_rows = row_pattern.findall(content)
            for cat, rating, notes in scorecard_rows:
                scorecard[cat.strip()] = {
                    "stars": rating.strip(),
                    "numeric": rating.count('★'),
                    "rationale": notes.strip()
                }

            # 4. Parse Modern Relevance
            relevance_match = re.search(r'##\s*Modern Relevance\s*\n\s*(.*?)\n\s*(?:---|\n##)', content, re.DOTALL)
            relevance = relevance_match.group(1).strip() if relevance_match else ""

            # 5. Parse References
            refs_match = re.search(r'##\s*References\s*\n\s*(.*?)\n\s*(?:---|\n##|$)', content, re.DOTALL)
            references = []
            if refs_match:
                # Find all list items starting with - or * or numbers
                ref_items = re.findall(r'^\s*[\-\*\d\.]+\s*(.+)$', refs_match.group(1), re.MULTILINE)
                references = [r.strip() for r in ref_items]

            self.data["excavations"].append({
                "id": file.replace(".md", ""),
                "title": title,
                "path": f"excavations/{file}",
                "summary": summary,
                "scorecard": scorecard,
                "modern_relevance": relevance,
                "references": references
            })

    def parse_synthesis_essays(self):
        print("Parsing synthesis essays and scorecard...")
        synthesis_dir = os.path.join(self.root_dir, "synthesis")
        essays = []
        if os.path.exists(synthesis_dir):
            for file in sorted(os.listdir(synthesis_dir)):
                if not file.endswith(".md") or file == "README.md":
                    continue
                filepath = os.path.join(synthesis_dir, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else file.replace(".md", "")

                # Get first paragraph or blockquote as summary
                summary_match = re.search(r'^(?:>.*?|[A-Za-z].*?)(?:\n|$)', content, re.MULTILINE)
                summary = summary_match.group(0).strip().replace("> ", "") if summary_match else ""

                essays.append({
                    "id": file.replace(".md", ""),
                    "title": title,
                    "path": f"synthesis/{file}",
                    "summary": summary
                })

        # Also parse modern-relevance/revival-readiness.md
        readiness_path = os.path.join(self.root_dir, "modern-relevance", "revival-readiness.md")
        if os.path.exists(readiness_path):
            with open(readiness_path, 'r', encoding='utf-8') as f:
                content = f.read()
            title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else "Modern Revival Readiness Scorecard"
            essays.append({
                "id": "revival-readiness",
                "title": title,
                "path": "modern-relevance/revival-readiness.md",
                "summary": "A quantitative scorecard and high-density synthesis evaluating the commercial and technical revival readiness of the four core lineages under sub-5nm CMOS constraints."
            })

        self.data["synthesis_essays"] = essays

    def parse_reconstructions(self):
        print("Parsing reconstructions and simulators...")
        reconstructions_dir = os.path.join(self.root_dir, "reconstructions")
        recons = []
        if os.path.exists(reconstructions_dir):
            for folder in sorted(os.listdir(reconstructions_dir)):
                folder_path = os.path.join(reconstructions_dir, folder)
                if not os.path.isdir(folder_path) or folder in ("__pycache__", "synthesizable-hardware", "co-simulation"):
                    continue

                # Look for a .py file that serves as simulator or test files
                py_files = [f for f in os.listdir(folder_path) if f.endswith(".py") and not f.startswith("test_")]
                if not py_files:
                    continue
                entry_point = py_files[0]

                # Construct description
                desc = f"Executable simulator for the {folder.replace('-', ' ').title()} paradigm."
                if folder == "plan9-9p":
                    desc = "Stateful 9P/Styx protocol and private distributed namespace simulator."
                elif folder == "systolic-array":
                    desc = "Cycle-accurate Weight-Stationary and Output-Stationary systolic matrix multiplier with energy proxy counters."
                elif folder == "neuromorphic-spiking":
                    desc = "Event-driven Spiking Neural Network (SNN) simulator modeling Leaky Integrate-and-Fire (LIF) dynamics, Address-Event Representation (AER), and Spike-Timing-Dependent Plasticity (STDP) learning rules."
                elif folder == "cryogenic-superconducting":
                    desc = "Picosecond-accurate Rapid Single Flux Quantum (RSFQ) pulse logic timing and thermodynamic cooling penalty simulator."

                recons.append({
                    "id": folder,
                    "title": folder.replace("-", " ").title(),
                    "path": f"reconstructions/{folder}/",
                    "entry_point": f"reconstructions/{folder}/{entry_point}",
                    "description": desc
                })

            # Add synthesizable-hardware and co-simulation manually as they are special
            recons.append({
                "id": "synthesizable-hardware",
                "title": "Synthesizable Hardware Blueprints",
                "path": "reconstructions/synthesizable-hardware/",
                "entry_point": "reconstructions/synthesizable-hardware/",
                "description": "Synthesizable SystemVerilog models of a 3-trit Balanced Ternary ALU and Tagged RAM Capability Bounds Checker."
            })
            recons.append({
                "id": "co-simulation",
                "title": "Multi-Architecture Co-Simulation Fabric",
                "path": "reconstructions/co-simulation/",
                "entry_point": "reconstructions/co-simulation/orchestrator.py",
                "description": "Cross-architecture co-simulator orchestrating a hybrid AI statistical pipeline, synchronous CSP channels, and dynamic dataflow blocks."
            })
            recons.append({
                "id": "experiments-runner",
                "title": "Multi-Paradigm Experiments Runner",
                "path": "reconstructions/co-simulation/",
                "entry_point": "reconstructions/co-simulation/experiments.py",
                "description": "Demonstration runner executing three concrete architectural experiments: cryogenic systolic array mapping, reversible storage loops uncomputation, and 9P sandboxed capabilities enforcement."
            })

        self.data["reconstructions"] = recons


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generator = KnowledgeGraphGenerator(repo_root)
    generator.generate()
