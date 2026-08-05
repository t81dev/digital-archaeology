#!/usr/bin/env python3
"""
Automated Excavation Verification and Link Integrity Linter.
Validates repository link integrity, scorecard compliance, and taxonomy checks.
"""

import os
import re
import sys
import collections

# Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

REQUIRED_SCORECARD_CATEGORIES = {
    "Historical Importance",
    "Technical Innovation",
    "Commercial Success",
    "Modern Potential",
    "AI Synergy",
    "Difficulty to Recreate"
}

def log_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def log_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def log_error(msg):
    print(f"{RED}✗ {msg}{RESET}")


class RepoLinter:
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        self.errors = []
        self.warnings = []

    def report_error(self, filepath, message):
        rel_path = os.path.relpath(filepath, self.root_dir)
        self.errors.append((rel_path, message))

    def report_warning(self, filepath, message):
        rel_path = os.path.relpath(filepath, self.root_dir)
        self.warnings.append((rel_path, message))

    def run_all_checks(self):
        print(f"\n=== Running Repository Verification Suite in '{self.root_dir}' ===")
        all_md_files = []
        for root, dirs, files in os.walk(self.root_dir):
            # Skip hidden directories, docs_source, and site
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('docs_source', 'site')]
            for file in files:
                if file.endswith(".md"):
                    all_md_files.append(os.path.join(root, file))

        # 1. Check Link Integrity
        self.check_links(all_md_files)

        # 2. Check Scorecards in Excavations
        self.check_scorecards()

        # 3. Check GLOSSARY Referencing & Completeness
        self.check_glossary_referencing()

        # 4. Check Comparative Index Integration Mapping
        self.check_comparative_index_mapping()

        # Print report
        print("\n" + "=" * 50)
        print("                VERIFICATION REPORT")
        print("" + "=" * 50)

        if self.warnings:
            print(f"\n{YELLOW}Warnings ({len(self.warnings)}):{RESET}")
            for path, msg in self.warnings:
                print(f"  {YELLOW}[WARNING]{RESET} {path}: {msg}")

        if self.errors:
            print(f"\n{RED}Errors ({len(self.errors)}):{RESET}")
            for path, msg in self.errors:
                print(f"  {RED}[ERROR]{RESET} {path}: {msg}")
            print(f"\n{RED}Verification FAILED with {len(self.errors)} errors.{RESET}\n")
            return False
        else:
            log_success("All repository integrity, scorecard, and glossary checks passed successfully!\n")
            return True

    def check_links(self, md_files):
        print("\n1. Verifying Markdown Link Integrity...")
        # Match standard markdown links: [text](link)
        # Exclude images starts with !
        link_pattern = re.compile(r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)')

        for filepath in md_files:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            file_dir = os.path.dirname(filepath)
            matches = link_pattern.findall(content)

            for text, link in matches:
                # Trim anchor fragments or query params
                clean_link = link.split('#')[0].split('?')[0].strip()

                if not clean_link:
                    # Self-anchor link like [text](#anchor), skip validation
                    continue

                if clean_link.startswith(("http://", "https://", "mailto:", "ftp:")):
                    # External link, skip validation but check syntax if any
                    continue

                # Rule check: Do not use workspace-absolute paths (starting with /)
                if clean_link.startswith("/"):
                    self.report_error(
                        filepath,
                        f"Workspace-absolute path found in link: '[{text}]({link})'. Internal links must be relative."
                    )
                    continue

                # Resolve the relative path
                target_path = os.path.abspath(os.path.join(file_dir, clean_link))

                if not os.path.exists(target_path):
                    self.report_error(
                        filepath,
                        f"Broken link: '[{text}]({link})' points to non-existent path: '{clean_link}'."
                    )

    def check_scorecards(self):
        print("2. Verifying Excavation Scorecard Compliance...")
        excavations_dir = os.path.join(self.root_dir, "excavations")
        if not os.path.exists(excavations_dir):
            log_warning("No 'excavations/' directory found, skipping scorecard checks.")
            return

        # Scan excavations files
        for file in os.listdir(excavations_dir):
            if not file.endswith(".md") or file in ("README.md", "excavation-template.md"):
                continue

            filepath = os.path.join(excavations_dir, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Find scorecard table
            # Looking for a table containing the categories
            lines = content.splitlines()
            categories_found = {}

            # Scorecard row pattern: | Category Name | StarRating | Comment |
            # Rating can be ★★★☆☆, etc.
            row_pattern = re.compile(r'^\s*\|\s*([^|]+)\s*\|\s*([★☆]{5})\s*\|.*$')

            for line in lines:
                m = row_pattern.match(line)
                if m:
                    category = m.group(1).strip()
                    rating = m.group(2).strip()
                    # Only map if it matches our standard categories
                    for req_cat in REQUIRED_SCORECARD_CATEGORIES:
                        if category.lower() == req_cat.lower():
                            categories_found[req_cat] = rating

            # Verify all required categories exist
            missing = REQUIRED_SCORECARD_CATEGORIES - set(categories_found.keys())
            if missing:
                self.report_error(
                    filepath,
                    f"Invalid or missing scorecard categories: {list(missing)}. Excavations must contain exactly the 6 standardized scorecard rows."
                )

            # Check individual rating stars format
            for cat, rating in categories_found.items():
                if len(rating) != 5 or not all(c in ('★', '☆') for c in rating):
                    self.report_error(
                        filepath,
                        f"Invalid scorecard rating format for '{cat}': '{rating}'. Must be exactly 5 characters of ★ and ☆."
                    )

    def check_comparative_index_mapping(self):
        print("4. Verifying Comparative Index Integration...")
        comp_path = os.path.join(self.root_dir, "COMPARATIVE_INDEX.md")
        if not os.path.exists(comp_path):
            self.report_error(self.root_dir, "COMPARATIVE_INDEX.md is missing from the repository root!")
            return

        with open(comp_path, 'r', encoding='utf-8') as f:
            comp_content = f.read()

        # Find all relative excavation links
        mapped_paths = set()
        link_pattern = re.compile(r'\[[^\]]+\]\((excavations/[^)]+\.md)\)')
        matches = link_pattern.findall(comp_content)
        for rel_link in matches:
            abs_path = os.path.abspath(os.path.join(self.root_dir, rel_link))
            mapped_paths.add(abs_path)

        # Get list of actual excavations
        excavations_dir = os.path.join(self.root_dir, "excavations")
        if not os.path.exists(excavations_dir):
            return

        for file in os.listdir(excavations_dir):
            if file.endswith(".md") and file not in ("README.md", "excavation-template.md"):
                abs_path = os.path.abspath(os.path.join(excavations_dir, file))
                if abs_path not in mapped_paths:
                    rel_exc = os.path.relpath(abs_path, self.root_dir)
                    self.report_error(
                        comp_path,
                        f"Excavation file '{rel_exc}' is not integrated or mapped anywhere in COMPARATIVE_INDEX.md! "
                        "Every excavation must be classified in our multi-dimensional comparative taxonomy to maintain high-density explanation."
                    )

    def check_glossary_referencing(self):
        print("3. Verifying GLOSSARY Referencing & Completeness...")
        glossary_path = os.path.join(self.root_dir, "GLOSSARY.md")
        if not os.path.exists(glossary_path):
            self.report_error(self.root_dir, "GLOSSARY.md is missing from the repository root!")
            return

        with open(glossary_path, 'r', encoding='utf-8') as f:
            glossary_content = f.read()

        # Parse all "See excavation" or "See modern relevance" links from GLOSSARY.md
        # Format: [Link Text](path)
        see_links = re.findall(r'\*\s*\*See (?:excavation|modern relevance)\*:\s*(.+)', glossary_content)
        referenced_paths = set()
        for link_line in see_links:
            matches = re.findall(r'\[[^\]]+\]\(([^)]+)\)', link_line)
            for path in matches:
                # Resolve relative path
                clean_path = path.split('#')[0].split('?')[0].strip()
                abs_path = os.path.abspath(os.path.join(os.path.dirname(glossary_path), clean_path))
                referenced_paths.add(abs_path)

        # Let's get the list of actual excavations
        excavations_dir = os.path.join(self.root_dir, "excavations")
        if not os.path.exists(excavations_dir):
            return

        all_excavations = []
        for file in os.listdir(excavations_dir):
            if file.endswith(".md") and file not in ("README.md", "excavation-template.md"):
                abs_path = os.path.abspath(os.path.join(excavations_dir, file))
                all_excavations.append(abs_path)

        # Verify that all excavations have corresponding references in GLOSSARY.md
        # This prevents "dangling" excavations that aren't integrated into the taxonomy!
        for exc_path in all_excavations:
            if exc_path not in referenced_paths:
                rel_exc = os.path.relpath(exc_path, self.root_dir)
                self.report_warning(
                    glossary_path,
                    f"Excavation file '{rel_exc}' is not referenced under any term in GLOSSARY.md. "
                    "Consider adding a glossary entry linking to this excavation."
                )


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    linter = RepoLinter(repo_root)
    success = linter.run_all_checks()
    sys.exit(0 if success else 1)
