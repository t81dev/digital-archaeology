#!/usr/bin/env python3
"""
Automated Cross-Reference Generator for Digital Archaeology.
Parses markdown files and uses terms from the glossary, excavations, patterns,
and synthesis essays to automatically inject relative markdown links.
"""

import os
import re
import sys
import json
import argparse

# Regex to identify "untouchable" sections of markdown
UNTOUCHABLE_REGEX = re.compile(
    r'(?P<fenced_code>```[\s\S]*?```)'
    r'|(?P<inline_code>`[^`\n]*?`)'
    r'|(?P<md_link>\[[^\]]*?\]\([^)]*?\))'
    r'|(?P<html_tag><[^>]*?>)'
)


def tokenize(content: str) -> list:
    """Splits markdown content into 'text' tokens and 'untouchable' tokens."""
    tokens = []
    last_end = 0
    for m in UNTOUCHABLE_REGEX.finditer(content):
        start, end = m.span()
        if start > last_end:
            tokens.append(("text", content[last_end:start]))
        tokens.append(("untouchable", content[start:end]))
        last_end = end
    if last_end < len(content):
        tokens.append(("text", content[last_end:]))
    return tokens


def build_vocabulary(root_dir: str) -> dict:
    """Loads all glossary terms, excavations, synthesis essays, and patterns as a mapping of term -> relative_path."""
    kg_path = os.path.join(root_dir, "modern-relevance", "knowledge_graph.json")
    if not os.path.exists(kg_path):
        # Fallback/generate if missing
        try:
            from tools.generate_knowledge_graph import KnowledgeGraphGenerator
            generator = KnowledgeGraphGenerator(root_dir)
            generator.generate()
        except ImportError:
            pass

    vocabulary = {}

    if os.path.exists(kg_path):
        with open(kg_path, 'r', encoding='utf-8') as f:
            kg = json.load(f)

        # 1. Glossary Terms -> GLOSSARY.md
        for item in kg.get("glossary", []):
            term = item["term"]
            vocabulary[term] = "GLOSSARY.md"

        # 2. Excavations -> excavations/<file>.md
        for item in kg.get("excavations", []):
            title = item["title"]
            path = item["path"]
            vocabulary[title] = path

        # 3. Synthesis Essays -> synthesis/<file>.md
        for item in kg.get("synthesis_essays", []):
            title = item["title"]
            path = item["path"]
            vocabulary[title] = path

    # 4. Patterns -> patterns/<file>.md
    patterns_dir = os.path.join(root_dir, "patterns")
    if os.path.exists(patterns_dir):
        for file in os.listdir(patterns_dir):
            if file.endswith(".md") and file != "README.md":
                path = os.path.join(patterns_dir, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                    vocabulary[title] = f"patterns/{file}"

    # Also add manually some common high-value terms if missing
    additional_terms = {
        "9P Protocol": "GLOSSARY.md",
        "Active Messages": "GLOSSARY.md",
        "Analog Computing": "excavations/analog-computing.md",
        "Balanced Ternary": "excavations/balanced-ternary.md",
        "Capability Systems": "excavations/capability-systems.md",
        "Cellular Automata Hardware": "excavations/cellular-automata-hardware.md",
        "Constraint Migration": "patterns/constraint-migration.md",
        "Dataflow Computing": "excavations/dataflow-computing.md",
        "Economic Failures": "patterns/economic-failures.md",
        "Ecosystem Lock-In": "patterns/ecosystem-lockin.md",
        "Forgotten Abstractions": "patterns/forgotten-abstractions.md",
        "Heterogeneous Revival": "patterns/heterogeneous-revival.md",
        "Lisp Machines": "excavations/lisp-machines.md",
        "Multics": "excavations/multics.md",
        "Neuromorphic Hardware": "excavations/neuromorphic-hardware.md",
        "Occam": "excavations/occam.md",
        "Optical Computing": "excavations/optical-computing.md",
        "Plan 9": "excavations/plan-9.md",
        "Project Xanadu": "excavations/project-xanadu.md",
        "Recurring Ideas": "patterns/recurring-ideas.md",
        "Reversible Computing": "excavations/reversible-computing.md",
        "Smalltalk": "excavations/smalltalk.md",
        "Stochastic Computing": "excavations/stochastic-computing.md",
        "Superconducting & Cryogenic Microarchitectures": "excavations/superconducting-cryogenic.md",
        "Symbolic AI": "excavations/symbolic-ai.md",
        "Systolic Arrays": "excavations/systolic-arrays.md",
        "Transputers": "excavations/transputers.md",
        "Vector Supercomputing": "excavations/vector-supercomputing.md",
        "VLIW/EPIC Architectures": "excavations/vliw-epic.md",
        "Wafer-Scale Integration": "excavations/wafer-scale-integration.md",
        "BeOS / Haiku": "excavations/beos-haiku.md",
        "Burroughs Large Systems": "excavations/burroughs-large-systems.md",
        "Intel iAPX 432": "excavations/intel-iapx-432.md",
        "Linda Tuple Spaces": "excavations/linda-tuple-spaces.md"
    }

    for term, path in additional_terms.items():
        if term not in vocabulary:
            vocabulary[term] = path

    return vocabulary


def compute_relative_path(source_file_dir: str, target_path: str) -> str:
    """Computes the correct relative path from source_file_dir to target_path."""
    if not source_file_dir or source_file_dir == ".":
        return target_path
    rel = os.path.relpath(target_path, source_file_dir)
    return rel.replace(os.sep, '/')


def process_content(content: str, vocabulary: dict, source_file_path: str, root_dir: str) -> tuple:
    """
    Parses content, computes and injects relative links for matched terms.
    Returns (new_content, num_changes).
    """
    # 1. Filter vocabulary to prevent self-referencing links
    source_rel_path = os.path.relpath(source_file_path, root_dir).replace(os.sep, '/')
    filtered_vocab = {k: v for k, v in vocabulary.items() if v != source_rel_path}

    if not filtered_vocab:
        return content, 0

    # Sort terms by length in descending order to match longest first
    sorted_terms = sorted(filtered_vocab.keys(), key=len, reverse=True)
    vocab_lower = {k.lower(): v for k, v in filtered_vocab.items()}

    # Compile regex pattern to match whole words of any sorted term
    escaped_terms = [re.escape(term) for term in sorted_terms]
    # Use word boundary checks. Note: handles non-alphanumeric correctly.
    pattern_str = r'\b(' + '|'.join(escaped_terms) + r')\b'
    term_regex = re.compile(pattern_str, re.IGNORECASE)

    source_file_dir = os.path.dirname(source_file_path)
    # Compute relative dir path relative to root_dir
    rel_source_dir = os.path.relpath(source_file_dir, root_dir)

    tokens = tokenize(content)
    new_tokens = []
    num_changes = 0

    def replace_callback(match):
        nonlocal num_changes
        matched_text = match.group(0)
        term_key = matched_text.lower()
        target_path = vocab_lower[term_key]

        # Compute proper relative path
        rel_link_path = compute_relative_path(rel_source_dir, target_path)
        num_changes += 1
        return f"[{matched_text}]({rel_link_path})"

    for token_type, token_val in tokens:
        if token_type == "text":
            replaced_val = term_regex.sub(replace_callback, token_val)
            new_tokens.append(replaced_val)
        else:
            new_tokens.append(token_val)

    return "".join(new_tokens), num_changes


def main():
    parser = argparse.ArgumentParser(
        description="Automated Cross-Reference Generator: Injects relative markdown links for excavations, patterns, synthesis, and glossary terms."
    )
    parser.add_argument("--file", type=str, help="Process a specific markdown file.")
    parser.add_argument("--dir", type=str, help="Process all markdown files in a directory.")
    parser.add_argument("--all", action="store_true", help="Process all markdown files in the repository.")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode. Identifies changes but does not write to files.")

    args = parser.parse_args()

    # Locate repo root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)

    # Build vocabulary
    vocabulary = build_vocabulary(root_dir)
    print(f"Built cross-reference vocabulary with {len(vocabulary)} terms.")

    # Collect target files
    target_files = []
    if args.file:
        if os.path.exists(args.file):
            target_files.append(os.path.abspath(args.file))
        else:
            print(f"Error: File '{args.file}' does not exist.")
            sys.exit(1)
    elif args.dir:
        if os.path.exists(args.dir) and os.path.isdir(args.dir):
            for root, _, files in os.walk(args.dir):
                for file in files:
                    if file.endswith(".md"):
                        target_files.append(os.path.abspath(os.path.join(root, file)))
        else:
            print(f"Error: Directory '{args.dir}' does not exist or is not a directory.")
            sys.exit(1)
    elif args.all:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('docs_source', 'site', 'node_modules')]
            for file in files:
                if file.endswith(".md"):
                    target_files.append(os.path.abspath(os.path.join(root, file)))
    else:
        parser.print_help()
        sys.exit(0)

    print(f"Found {len(target_files)} markdown files to process.")

    total_changes = 0
    modified_files_count = 0

    for file_path in target_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        new_content, changes = process_content(content, vocabulary, file_path, root_dir)

        if changes > 0:
            modified_files_count += 1
            total_changes += changes
            rel_file_path = os.path.relpath(file_path, root_dir)
            print(f"  - {rel_file_path}: Found {changes} cross-reference matches.")

            if not args.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

    mode_str = " (DRY RUN - no files written)" if args.dry_run else ""
    print(f"\nCompleted cross-referencing! Modified {modified_files_count}/{len(target_files)} files with {total_changes} links injected{mode_str}.")


if __name__ == "__main__":
    main()
