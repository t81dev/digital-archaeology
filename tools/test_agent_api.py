# test_agent_api.py
# Unit tests for the Agentic Co-Design Tooling API

import os
import sys
import json
import pytest

# Add tools directory to path
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from agent_api import AgentAPI

def test_agent_api_initialization():
    """Verify AgentAPI compiles schemas and loads components correctly."""
    repo_root = os.path.abspath(os.path.join(current_dir, ".."))

    api = AgentAPI(repo_root=repo_root)
    schema = api.get_unified_agent_schema()

    assert schema["schema_version"] == "1.0"
    assert "co_design_endpoints" in schema
    assert "hardware_soft_cores" in schema

    # Assert capability checker RTL parsing works
    checker_rtl = schema["hardware_soft_cores"]["capability_bounds_checker"]
    assert "module" in checker_rtl
    assert checker_rtl["module"] == "capability_bounds_checker"
    assert len(checker_rtl["ports"]) > 0
    assert checker_rtl["assertions_count"] == 3  # assert_unforgeable, assert_boundary_safety, assert_page_fault

    # Assert predictive scores run successfully
    assert "predictive_horizon" in schema
    assert schema["predictive_horizon"]["status"] in ["success", "fallback"]
