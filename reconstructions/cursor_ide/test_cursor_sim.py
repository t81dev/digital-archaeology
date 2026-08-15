"""
Unit tests for Cursor IDE Substrate & Agentic Workspace Simulator.
"""

import pytest
from reconstructions.cursor_ide.cursor_sim import (
    VectorKeywordIndexer,
    ContextAssembler,
    DiffApplyEngine,
    CursorWorkspaceAgent,
    Diagnostic,
)


def test_vector_keyword_indexer():
    indexer = VectorKeywordIndexer()
    indexer.add_file(
        "auth.py",
        "def login_user(username, password):\n    # authenticate user\n    return True\n"
    )
    indexer.add_file(
        "database.py",
        "class Database:\n    def connect(self):\n        pass\n"
    )

    results = indexer.search("login user", top_k=2)
    assert len(results) > 0
    assert results[0].file_path == "auth.py"
    assert "login_user" in results[0].content


def test_context_assembler_budgeting():
    indexer = VectorKeywordIndexer()
    indexer.add_file("main.py", "def main():\n    print('Hello World')\n")
    assembler = ContextAssembler(indexer)

    workspace = {"main.py": "def main():\n    print('Hello World')\n"}
    diagnostics = [Diagnostic("main.py", 2, "error", "Missing type hint")]
    rules = ["Use strict typing", "Prefer functional style"]

    packet = assembler.build_packet(
        user_query="Fix type hint in main",
        workspace_files=workspace,
        active_file="main.py",
        diagnostics=diagnostics,
        project_rules=rules,
        token_budget=500
    )

    assert "System: You are an AI-native coding assistant" in packet.assembled_prompt
    assert "Project Rules (.cursorrules):" in packet.assembled_prompt
    assert "Use strict typing" in packet.assembled_prompt
    assert "Active File (main.py):" in packet.assembled_prompt
    assert "[ERROR] main.py:2 - Missing type hint" in packet.assembled_prompt
    assert "Fix type hint in main" in packet.assembled_prompt


def test_diff_apply_engine_patch_approval():
    workspace = {"app.py": "val = UNDEFINED_VARIABLE\n"}
    patch = DiffApplyEngine.create_patch("app.py", workspace["app.py"], "val = 42\n")

    assert "-val = UNDEFINED_VARIABLE" in patch.diff_unified
    assert "+val = 42" in patch.diff_unified

    # Reject patch
    applied = DiffApplyEngine.apply_patch(patch, workspace, user_accepts=False)
    assert not applied
    assert workspace["app.py"] == "val = UNDEFINED_VARIABLE\n"

    # Accept patch
    applied = DiffApplyEngine.apply_patch(patch, workspace, user_accepts=True)
    assert applied
    assert workspace["app.py"] == "val = 42\n"


def test_cursor_workspace_agent_self_healing_loop():
    workspace = {
        "src/calculator.py": "def add(a, b):\n    result = SYNTAX_ERROR\n    return result\n"
    }
    rules = ["Ensure clean syntax"]
    agent = CursorWorkspaceAgent(workspace, project_rules=rules)

    # Verify initial error detected
    errors = agent.get_linter_errors()
    assert len(errors) == 1
    assert errors[0].file_path == "src/calculator.py"

    # Run agent loop
    final_workspace = agent.execute_agent_goal("Fix syntax error and run tests")

    # Verify self-healing fix applied
    assert "SYNTAX_ERROR" not in final_workspace["src/calculator.py"]
    assert "FIXED_CODE" in final_workspace["src/calculator.py"]
    assert len(agent.get_linter_errors()) == 0


def test_agent_terminal_command_approval_safety():
    workspace = {"file.py": "print('hello')\n"}
    agent = CursorWorkspaceAgent(workspace)

    # Command rejected by user
    output_rejected = agent.run_terminal_command("rm -rf /", require_approval=True, approved=False)
    assert "Execution Rejected" in output_rejected

    # Command approved
    output_approved = agent.run_terminal_command("echo hello", require_approval=True, approved=True)
    assert "Exit Code 0" in output_approved
