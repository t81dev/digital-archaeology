#!/usr/bin/env python3
"""
Setup Docs Source Script
-----------------------
Prepares the 'docs_source/' directory with relative symbolic links to the root-level
Markdown files and subdirectories. This allows MkDocs to build the site seamlessly
without duplicating files or violating its single-directory requirement.
"""

import os
import shutil
import sys

def main():
    # Resolve paths relative to repo root
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_source_dir = os.path.join(repo_root, "docs_source")

    print(f"Setting up MkDocs source directory in: {docs_source_dir}")

    # 1. Clean existing directory if it exists
    if os.path.exists(docs_source_dir):
        print("Cleaning existing docs_source/ directory...")
        try:
            if os.path.islink(docs_source_dir):
                os.unlink(docs_source_dir)
            else:
                shutil.rmtree(docs_source_dir)
        except Exception as e:
            print(f"Warning: Failed to clean docs_source/ directory: {e}")

    # Recreate docs_source
    os.makedirs(docs_source_dir, exist_ok=True)

    # 2. Define files and directories to symlink
    # Maps: target_name_in_docs_source -> relative_source_path_from_docs_source
    mappings = {
        "index.md": "../README.md",
        "INDEX.md": "../INDEX.md",
        "MANIFESTO.md": "../MANIFESTO.md",
        "ROADMAP.md": "../ROADMAP.md",
        "GLOSSARY.md": "../GLOSSARY.md",
        "COMPARATIVE_INDEX.md": "../COMPARATIVE_INDEX.md",
        "CONTRIBUTING.md": "../CONTRIBUTING.md",
        "excavations": "../excavations",
        "patterns": "../patterns",
        "synthesis": "../synthesis",
        "modern-relevance": "../modern-relevance",
        "reconstructions": "../reconstructions",
        "timelines": "../timelines",
        "bibliography": "../bibliography"
    }

    success = True
    for dest, src in mappings.items():
        dest_path = os.path.join(docs_source_dir, dest)
        try:
            # Create symbolic link using relative paths for portability
            if hasattr(os, "symlink"):
                try:
                    os.symlink(src, dest_path)
                    print(f"Created symlink: docs_source/{dest} -> {src}")
                    continue
                except OSError as symlink_err:
                    print(f"Symlink failed for {dest} ({symlink_err}). Falling back to copy...")

            # Fallback (for platforms without symlink support or missing privileges, e.g. Windows)
            real_src_path = os.path.abspath(os.path.join(docs_source_dir, src))
            if os.path.isdir(real_src_path):
                shutil.copytree(real_src_path, dest_path)
                print(f"Copied directory fallback: {dest} <- {src}")
            else:
                shutil.copy2(real_src_path, dest_path)
                print(f"Copied file fallback: {dest} <- {src}")
        except Exception as e:
            print(f"Error linking/copying {dest}: {e}")
            success = False

    if success:
        print("\n✓ MkDocs source setup completed successfully!")
    else:
        print("\n✗ Setup completed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
