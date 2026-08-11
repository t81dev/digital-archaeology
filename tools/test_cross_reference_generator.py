import os
import pytest
from tools.cross_reference_generator import (
    tokenize,
    compute_relative_path,
    process_content,
    build_vocabulary
)

def test_tokenize():
    content = (
        "Hello, this is a term. Read [Plan 9](excavations/plan-9.md) and see code: `foo`. "
        "Also here is an untouchable fenced block:\n"
        "```python\n"
        "print('Keep Balanced Ternary unmodified')\n"
        "```\n"
        "Have a nice day."
    )
    tokens = tokenize(content)

    # Verify we got the expected tokens
    assert len(tokens) > 0

    # Fenced code block should be marked as untouchable
    fenced_blocks = [val for t_type, val in tokens if t_type == "untouchable" and "```python" in val]
    assert len(fenced_blocks) == 1

    # Existing md link should be marked as untouchable
    link_blocks = [val for t_type, val in tokens if t_type == "untouchable" and "[Plan 9]" in val]
    assert len(link_blocks) == 1

    # Inline code block should be marked as untouchable
    inline_blocks = [val for t_type, val in tokens if t_type == "untouchable" and "`foo`" in val]
    assert len(inline_blocks) == 1


def test_compute_relative_path():
    # Source is at root, targeting excavations/plan-9.md
    assert compute_relative_path("", "excavations/plan-9.md") == "excavations/plan-9.md"

    # Source is at root, targeting GLOSSARY.md
    assert compute_relative_path(".", "GLOSSARY.md") == "GLOSSARY.md"

    # Source is in excavations/ directory, targeting synthesis/compiler-hardware-co-design.md
    assert compute_relative_path("excavations", "synthesis/compiler-hardware-co-design.md") == "../synthesis/compiler-hardware-co-design.md"

    # Source is in excavations/ directory, targeting GLOSSARY.md
    assert compute_relative_path("excavations", "GLOSSARY.md") == "../GLOSSARY.md"

    # Source is in excavations/ directory, targeting excavations/plan-9.md
    assert compute_relative_path("excavations", "excavations/plan-9.md") == "plan-9.md"


def test_process_content():
    vocabulary = {
        "Balanced Ternary": "excavations/balanced-ternary.md",
        "Analog Computing": "excavations/analog-computing.md",
        "Plan 9": "excavations/plan-9.md"
    }

    content = (
        "Here we discuss Balanced Ternary and Analog Computing. "
        "But we do NOT modify existing `Balanced Ternary` code, nor [Plan 9](excavations/plan-9.md)."
    )

    # File is excavations/test-file.md (located in excavations/)
    source_file = os.path.join("excavations", "test-file.md")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    new_content, changes = process_content(content, vocabulary, source_file, root_dir)

    # Expected: "Balanced Ternary" in plain text gets replaced by "[Balanced Ternary](balanced-ternary.md)"
    # Expected: "Analog Computing" gets replaced by "[Analog Computing](analog-computing.md)"
    # Expected: `Balanced Ternary` inside code block and [Plan 9] inside existing link remain unchanged!
    assert "[Balanced Ternary](balanced-ternary.md)" in new_content
    assert "[Analog Computing](analog-computing.md)" in new_content
    assert "`Balanced Ternary`" in new_content
    assert "[Plan 9](excavations/plan-9.md)" in new_content
    assert changes == 2


def test_prevent_self_referencing():
    vocabulary = {
        "Balanced Ternary": "excavations/balanced-ternary.md",
        "Analog Computing": "excavations/analog-computing.md"
    }

    content = "Welcome to Balanced Ternary and Analog Computing."

    # Source file is the excavations/balanced-ternary.md file itself
    source_file = os.path.join("excavations", "balanced-ternary.md")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    new_content, changes = process_content(content, vocabulary, source_file, root_dir)

    # "Balanced Ternary" should NOT be linked (as it's self-referencing), but "Analog Computing" should be linked!
    assert "Balanced Ternary" in new_content
    assert "[Balanced Ternary]" not in new_content
    assert "[Analog Computing](analog-computing.md)" in new_content
    assert changes == 1


def test_vocabulary_building():
    # Verify we can build the vocabulary successfully without throwing exceptions
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    vocab = build_vocabulary(root_dir)
    assert len(vocab) > 0
    assert "Balanced Ternary" in vocab
    assert "Analog Computing" in vocab
