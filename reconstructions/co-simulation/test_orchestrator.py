# test_orchestrator.py
# Pytest suite for checking Multi-Architecture Co-Simulation and Interoperability

import os
import sys
import pytest

# Ensure parents and sister folders can be loaded
COSIM_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, COSIM_DIR)

from orchestrator import CoSimulationOrchestrator


def test_co_simulation_pipeline_active_threat():
    """Verify that an active threat is correctly handled and computes a non-zero risk score."""
    orchestrator = CoSimulationOrchestrator(verbose=False)

    raw_data = {
        'package_detected': 0.10,
        'person_present': 0.95,
        'authorized_resident': 0.05,
        'unknown_person': 0.95,
        'threat_detected': 0.90 # High threat
    }

    # Execute orchestrator pipeline
    risk_score = orchestrator.execute_pipeline(raw_data)

    # Expected calculation:
    # base_threat = int(0.90 * 10) = 9
    # prox_factor = 4
    # (9^2 + 4^2) * 0.90 = (81 + 16) * 0.90 = 97 * 0.90 = 87.3
    assert risk_score == pytest.approx(87.3), f"Calculated risk score {risk_score} was not correct!"


def test_co_simulation_pipeline_nominal_standby():
    """Verify that no action is taken when there is no threat present."""
    orchestrator = CoSimulationOrchestrator(verbose=False)

    raw_data = {
        'package_detected': 0.05,
        'person_present': 0.05,
        'authorized_resident': 0.01,
        'unknown_person': 0.02,
        'threat_detected': 0.01 # Minimal threat
    }

    risk_score = orchestrator.execute_pipeline(raw_data)
    assert risk_score == 0.0, "Risk score should be 0.0 for nominal standby!"


def test_co_simulation_profiling_and_rebalancing():
    """Verify that co-simulation execution cycle profiling and dynamic rebalancing are performed."""
    orchestrator = CoSimulationOrchestrator(verbose=False)

    raw_data = {
        'package_detected': 0.10,
        'person_present': 0.95,
        'authorized_resident': 0.05,
        'unknown_person': 0.95,
        'threat_detected': 0.90 # High threat
    }

    risk_score = orchestrator.execute_pipeline(raw_data)
    assert risk_score > 0.0

    # Ensure profiled cycles were populated
    assert "Neuro-Symbolic" in orchestrator.profiled_cycles
    assert "CSP" in orchestrator.profiled_cycles
    assert "Dataflow" in orchestrator.profiled_cycles
    assert "EDGE" in orchestrator.profiled_cycles

    # Ensure rebalancer logged a configuration
    assert len(orchestrator.rebalance_logs) == 1
    rebalance_log = orchestrator.rebalance_logs[0]
    assert "bottleneck" in rebalance_log
    assert "recommendation" in rebalance_log
    assert len(rebalance_log["action_plan"]) > 0
