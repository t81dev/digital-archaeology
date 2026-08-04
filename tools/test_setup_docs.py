import os
import sys
import pytest

# Add tools directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from setup_docs import main

def test_setup_docs():
    """Verify that setup_docs correctly generates the docs_source directory with expected links."""
    # Execute the main function to set up the docs_source directory
    main()

    # Resolve expected paths
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    docs_source_dir = os.path.join(repo_root, "docs_source")

    # Verify the directory was created
    assert os.path.exists(docs_source_dir)
    assert os.path.isdir(docs_source_dir)

    # Verify that crucial symlinks / files exist inside docs_source
    expected_links = [
        "index.md",
        "INDEX.md",
        "GLOSSARY.md",
        "ROADMAP.md",
        "excavations",
        "patterns",
        "reconstructions"
    ]
    for link in expected_links:
        link_path = os.path.join(docs_source_dir, link)
        assert os.path.exists(link_path), f"Expected link/file '{link}' is missing in docs_source!"
