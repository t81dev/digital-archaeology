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
                "version": "1.0.0",
                "last_updated": "2026-08-02"
            },
            "glossary": [],
            "comparative_index": {
                "execution_models": {},
                "memory_protection_models": {},
                "concurrency_models": {}
            },
            "excavations": []
        }

    def generate(self):
        print("\n=== Generating AI-Assisted Knowledge Graph JSON Database ===")
        self.parse_glossary()
        self.parse_comparative_index()
        self.parse_excavations()

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


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generator = KnowledgeGraphGenerator(repo_root)
    generator.generate()
