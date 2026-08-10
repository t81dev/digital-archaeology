#!/usr/bin/env python3
"""
Unit tests for the Constraint Migration Predictive Hypothesis Engine.
"""

import json
from predictive_engine import PredictiveHypothesisEngine, render_star_rating


def test_baseline_predictions():
    """
    Verifies that with all factors at 1.0, the predicted scores equal the baselines.
    """
    engine = PredictiveHypothesisEngine()
    result = engine.forecast()

    assert result["inputs"]["copper_resistance"] == 1.0
    assert result["inputs"]["gate_leakage"] == 1.0

    # Under baseline, scores should match exactly
    for lineage, baseline in engine.LINEAGE_BASELINES.items():
        assert result["forecasts"][lineage]["predicted"] == baseline
        assert result["forecasts"][lineage]["delta"] == 0.0

    # Ensure ranking follows baselines descending
    # Spatial (4.4) > Neuromorphic (4.2) > Capability (3.8) > Physical (3.6) == Distributed (3.6) > Superconducting (3.4)
    assert result["ranking"][0] == "Spatial & Data-Parallel"
    assert result["ranking"][-1] == "Superconducting & Cryogenic"


def test_score_boundaries():
    """
    Verifies that even under extreme inputs, predicted scores are clamped between 1.0 and 5.0.
    """
    engine = PredictiveHypothesisEngine()

    # Extreme high scaling
    result_high = engine.forecast(
        copper_resistance=10.0,
        memory_wall=10.0,
        gate_leakage=10.0,
        security_risk=10.0,
        tensor_density=10.0,
        cryo_penalty=10.0
    )

    for data in result_high["forecasts"].values():
        assert 1.0 <= data["predicted"] <= 5.0

    # Extreme low scaling
    result_low = engine.forecast(
        copper_resistance=0.1,
        memory_wall=0.1,
        gate_leakage=0.1,
        security_risk=0.1,
        tensor_density=0.1,
        cryo_penalty=0.1
    )

    for data in result_low["forecasts"].values():
        assert 1.0 <= data["predicted"] <= 5.0


def test_security_risk_sensitivity():
    """
    Verifies that scaling security risks increases the Capability lineage score and triggers its hypothesis.
    """
    engine = PredictiveHypothesisEngine()
    result = engine.forecast(security_risk=4.0)

    # Capability score should have increased from baseline 3.8
    capability_data = result["forecasts"]["Capability, Tagged & Descriptor"]
    assert capability_data["predicted"] > 3.8
    assert capability_data["delta"] > 0.0

    # Ensure the correct security-related hypothesis was generated
    assert len(result["hypotheses"]) >= 1
    triggered_security = False
    for hyp in result["hypotheses"]:
        if "Capability" in hyp["proposal"] or "CHERI" in hyp["proposal"]:
            triggered_security = True
    assert triggered_security


def test_cryo_penalty_sensitivity():
    """
    Verifies that lowering cryo_penalty raises the Superconducting score, and raising it lowers the score.
    """
    engine = PredictiveHypothesisEngine()

    # Highly efficient cryocooler / high-temperature superconductor advancement (cryo_penalty = 0.2)
    result_efficient = engine.forecast(cryo_penalty=0.2)
    sc_efficient = result_efficient["forecasts"]["Superconducting & Cryogenic"]
    assert sc_efficient["predicted"] > 3.4
    assert sc_efficient["delta"] > 0.0

    # Inefficient cooling / expensive refrigeration (cryo_penalty = 3.0)
    result_expensive = engine.forecast(cryo_penalty=3.0)
    sc_expensive = result_expensive["forecasts"]["Superconducting & Cryogenic"]
    assert sc_expensive["predicted"] < 3.4
    assert sc_expensive["delta"] < 0.0


def test_star_ratings():
    """
    Verifies star rating string generation functions as expected.
    """
    assert render_star_rating(4.6) == "★★★★★"
    assert render_star_rating(3.2) == "★★★☆☆"
    assert render_star_rating(1.0) == "★☆☆☆☆"


def test_json_structure():
    """
    Verifies that the forecast payload structure is complete and JSON serialization friendly.
    """
    engine = PredictiveHypothesisEngine()
    result = engine.forecast(copper_resistance=2.0)

    # Serialize and deserialize to verify compatibility
    serialized = json.dumps(result)
    parsed = json.loads(serialized)

    assert "inputs" in parsed
    assert "forecasts" in parsed
    assert "ranking" in parsed
    assert "hypotheses" in parsed
    assert len(parsed["ranking"]) == 6


def test_cmos_node_modifiers():
    """
    Verifies that selecting a CMOS node correctly applies scaling modifiers.
    """
    engine = PredictiveHypothesisEngine()

    # Under GAA 3nm baseline, copper resistance should be scaled to 3.0
    result_gaa = engine.forecast(cmos_node="gaa-3nm")
    assert result_gaa["inputs"]["copper_resistance"] == 3.0
    assert result_gaa["inputs"]["memory_wall"] == 2.5

    # Under FinFET 16nm, gate leakage is scaled to 1.2
    result_finfet = engine.forecast(cmos_node="finfet-16nm")
    assert result_finfet["inputs"]["gate_leakage"] == 1.2


def test_sensitivity_analysis():
    """
    Verifies that the sensitivity analysis swept values and correctly isolates catalysts.
    """
    engine = PredictiveHypothesisEngine()
    sensitivities = engine.analyze_sensitivity("planar-28nm")

    # Capability primary catalyst should be security_risk
    cap_sens = sensitivities["Capability, Tagged & Descriptor"]
    assert cap_sens["primary_catalyst"] == "security_risk"
    assert cap_sens["max_sensitivity_slope"] > 0.0

    # Spatial primary catalyst should be memory_wall
    spatial_sens = sensitivities["Spatial & Data-Parallel"]
    assert spatial_sens["primary_catalyst"] == "memory_wall"

    # Verify that we have all 6 lineages represented
    assert len(sensitivities) == 6
