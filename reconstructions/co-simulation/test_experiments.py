# test_experiments.py
# Pytest suite for testing the multi-paradigm experiments.

import os
import sys
import pytest

# Ensure sister directory is in path
COSIM_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, COSIM_DIR)

from experiments import run_experiment_1, run_experiment_2, run_experiment_3


def test_experiment_1_cryo_systolic():
    """Verify cryogenic systolic coprocessor metrics are properly simulated."""
    metrics = run_experiment_1(verbose=False)
    assert metrics["cycles"] > 0
    assert metrics["mac_operations"] > 0
    assert metrics["interconnect_hops"] > 0
    assert metrics["total_switching_events"] > 0
    assert metrics["efficiency_gain"] > 1.0, "ERSFQ should be more efficient than standard CMOS!"


def test_experiment_2_reversible_uncomputation():
    """Verify Landauer heat minimization and refrigeration avoidance."""
    metrics = run_experiment_2(verbose=False)
    assert metrics["landauer_limit_4K_Joules"] > 0.0
    assert metrics["cooling_penalty_factor"] > 1.0
    assert metrics["irreversible_room_temp_Joules"] > 0.0
    assert metrics["reversible_room_temp_Joules"] == 0.0
    assert metrics["energy_saved_room_temp_fJ"] > 0.0


def test_experiment_3_plan9_and_capabilities():
    """Verify bounds and presence-bit security validation inside the sandbox."""
    metrics = run_experiment_3(verbose=False)
    assert metrics["nominal_read_success"] is True
    assert metrics["oob_attack_blocked"] is True
    assert metrics["page_fault_triggered"] is True
    assert metrics["page_fault_counter"] == 1


def test_cli_execution():
    """Verify that the CLI execution runs successfully via standard Python module execution."""
    import subprocess
    # Run CLI command with --all flag
    res = subprocess.run(
        [sys.executable, "-m", "reconstructions.co-simulation.experiments", "--all"],
        capture_output=True,
        text=True
    )
    assert res.returncode == 0
    assert "EXPERIMENT 1" in res.stdout
    assert "EXPERIMENT 2" in res.stdout
    assert "EXPERIMENT 3" in res.stdout
    assert "PASS / observed behavior" in res.stdout
