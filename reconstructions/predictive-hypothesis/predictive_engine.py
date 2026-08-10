#!/usr/bin/env python3
"""
Constraint Migration Predictive Hypothesis Engine.
A Python-based forecasting tool that maps historically sidelined architectural failures
to emerging post-CMOS physics, predicting which forgotten abstractions will gain the
highest-value revival potential within the next 10 years (2026-2036).
"""

import sys
import argparse
from typing import Dict, List, Any


class PredictiveHypothesisEngine:
    """
    Evaluates alternative computing lineages under custom post-CMOS scaling scenarios.
    Computes dynamic, quantitative scores representing "revival readiness" based on
    shifting physical and architectural constraints.
    """

    # Baseline scores from the Modern Revival Readiness Scorecard
    # These represent the starting average scores of each lineage under standard CMOS constraints.
    LINEAGE_BASELINES = {
        "Spatial & Data-Parallel": 4.4,
        "Neuromorphic & Stochastic": 4.2,
        "Capability, Tagged & Descriptor": 3.8,
        "Physical, Thermodynamic & Optical": 3.6,
        "Distributed & Single-Level-Store OS": 3.6,
        "Superconducting & Cryogenic": 3.4
    }

    # Custom CMOS technology node presets modeling physical scaling barriers
    CMOS_NODES = {
        "planar-28nm": {
            "copper_resistance": 1.0,
            "memory_wall": 1.0,
            "gate_leakage": 1.0,
            "security_risk": 1.0,
            "tensor_density": 1.0,
            "cryo_penalty": 1.0
        },
        "finfet-16nm": {
            "copper_resistance": 1.5,
            "memory_wall": 1.3,
            "gate_leakage": 1.2,
            "security_risk": 1.2,
            "tensor_density": 1.5,
            "cryo_penalty": 1.0
        },
        "gaa-3nm": {
            "copper_resistance": 3.0,
            "memory_wall": 2.5,
            "gate_leakage": 2.2,
            "security_risk": 1.8,
            "tensor_density": 2.5,
            "cryo_penalty": 1.0
        },
        "gaa-bspdn-2nm": {
            "copper_resistance": 4.5,
            "memory_wall": 3.5,
            "gate_leakage": 3.0,
            "security_risk": 2.5,
            "tensor_density": 3.5,
            "cryo_penalty": 1.1
        }
    }

    # Sensitivity weights (W_ij) for each lineage under each constraint.
    # Positives indicate that higher constraints increase the lineage's relative utility.
    # Negatives indicate that higher constraints degrade the lineage's relative utility.
    CONSTRAINT_WEIGHTS = {
        "Spatial & Data-Parallel": {
            "copper_resistance": 0.15,
            "memory_wall": 0.25,
            "gate_leakage": 0.10,
            "security_risk": 0.00,
            "tensor_density": 0.20,
            "cryo_penalty": 0.00
        },
        "Neuromorphic & Stochastic": {
            "copper_resistance": 0.15,
            "memory_wall": 0.10,
            "gate_leakage": 0.30,
            "security_risk": 0.00,
            "tensor_density": 0.20,
            "cryo_penalty": 0.00
        },
        "Capability, Tagged & Descriptor": {
            "copper_resistance": 0.00,
            "memory_wall": 0.05,
            "gate_leakage": 0.00,
            "security_risk": 0.40,
            "tensor_density": 0.10,
            "cryo_penalty": 0.00
        },
        "Physical, Thermodynamic & Optical": {
            "copper_resistance": 0.30,
            "memory_wall": 0.10,
            "gate_leakage": 0.25,
            "security_risk": 0.00,
            "tensor_density": 0.25,
            "cryo_penalty": 0.00
        },
        "Distributed & Single-Level-Store OS": {
            "copper_resistance": 0.00,
            "memory_wall": 0.15,
            "gate_leakage": 0.05,
            "security_risk": 0.25,
            "tensor_density": 0.10,
            "cryo_penalty": 0.00
        },
        "Superconducting & Cryogenic": {
            "copper_resistance": 0.15,
            "memory_wall": 0.05,
            "gate_leakage": 0.35,
            "security_risk": 0.00,
            "tensor_density": 0.15,
            "cryo_penalty": -0.35  # Higher penalty lowers the score, lower penalty (HTS/efficient cryo) raises it.
        }
    }

    def __init__(self):
        pass

    def forecast(
        self,
        copper_resistance: float = 1.0,
        memory_wall: float = 1.0,
        gate_leakage: float = 1.0,
        security_risk: float = 1.0,
        tensor_density: float = 1.0,
        cryo_penalty: float = 1.0,
        cmos_node: str = "planar-28nm"
    ) -> Dict[str, Any]:
        """
        Calculates dynamic scores and produces analytical hypotheses based on the inputs.

        Args:
            copper_resistance: Scale factor/multiplier for nanoscale interconnect RC delays (0.1 to 10.0)
            memory_wall: Scale factor/multiplier for off-chip DRAM latency & bandwidth limits (0.1 to 10.0)
            gate_leakage: Scale factor/multiplier for sub-threshold static power leakage (0.1 to 10.0)
            security_risk: Scale factor/multiplier for software-level exploit frequency (0.1 to 10.0)
            tensor_density: Scale factor/multiplier for AI workloads in compute mix (0.1 to 10.0)
            cryo_penalty: Scale factor/multiplier for cryogenic cooling thermodynamic overhead (0.1 to 10.0)
            cmos_node: The baseline CMOS technology node configuration preset.

        Returns:
            A structured dictionary containing inputs, forecasted scores, rankings, and hypotheses.
        """
        node_profile = self.CMOS_NODES.get(cmos_node, self.CMOS_NODES["planar-28nm"])

        inputs = {
            "copper_resistance": max(0.1, min(10.0, node_profile["copper_resistance"] * copper_resistance)),
            "memory_wall": max(0.1, min(10.0, node_profile["memory_wall"] * memory_wall)),
            "gate_leakage": max(0.1, min(10.0, node_profile["gate_leakage"] * gate_leakage)),
            "security_risk": max(0.1, min(10.0, node_profile["security_risk"] * security_risk)),
            "tensor_density": max(0.1, min(10.0, node_profile["tensor_density"] * tensor_density)),
            "cryo_penalty": max(0.1, min(10.0, node_profile["cryo_penalty"] * cryo_penalty))
        }

        forecasts = {}
        for lineage, baseline in self.LINEAGE_BASELINES.items():
            delta = 0.0
            weights = self.CONSTRAINT_WEIGHTS[lineage]

            # Apply linear delta scoring relative to baseline (where constraint factor 1.0 has delta 0.0)
            delta += weights["copper_resistance"] * (inputs["copper_resistance"] - 1.0)
            delta += weights["memory_wall"] * (inputs["memory_wall"] - 1.0)
            delta += weights["gate_leakage"] * (inputs["gate_leakage"] - 1.0)
            delta += weights["security_risk"] * (inputs["security_risk"] - 1.0)
            delta += weights["tensor_density"] * (inputs["tensor_density"] - 1.0)
            delta += weights["cryo_penalty"] * (inputs["cryo_penalty"] - 1.0)

            # Restrict final score within valid five-star boundaries [1.0, 5.0]
            predicted_score = round(max(1.0, min(5.0, baseline + delta)), 2)
            forecasts[lineage] = {
                "baseline": baseline,
                "predicted": predicted_score,
                "delta": round(predicted_score - baseline, 2)
            }

        # Rank lineages by predicted score
        ranked_lineages = sorted(
            forecasts.items(),
            key=lambda x: x[1]["predicted"],
            reverse=True
        )

        # Generate custom high-density research hypotheses based on bottlenecks
        hypotheses = self._generate_hypotheses(inputs)

        return {
            "inputs": inputs,
            "forecasts": forecasts,
            "ranking": [item[0] for item in ranked_lineages],
            "hypotheses": hypotheses
        }

    def _generate_hypotheses(self, inputs: Dict[str, float]) -> List[Dict[str, str]]:
        """
        Generates automated, highly-dense, primary-source-aligned research hypotheses.
        """
        hypotheses = []

        if inputs["copper_resistance"] >= 1.5:
            hypotheses.append({
                "trigger": f"Nanoscale interconnect copper resistance scaled to {inputs['copper_resistance']}x.",
                "claim": "Bypassing the wiring RC delay bottlenecks requires migrating away from global clock trees and multi-bit wide parallel buses.",
                "proposal": "Resurrect 2D spatial systolic arrays or asynchronous self-timed micropipelines with localized handshake protocols to eliminate clock distribution nets, or deploy Silicon Photonic Clements/Reck MZI wave meshes for zero-resistance optical matrix multiplication."
            })

        if inputs["gate_leakage"] >= 1.5:
            hypotheses.append({
                "trigger": f"Sub-threshold static leakage power scaled to {inputs['gate_leakage']}x (extreme Power Wall).",
                "claim": "Traditional room-temperature CMOS logic gates waste a critical share of energy during idle cycles through continuous sub-threshold leakage currents.",
                "proposal": "Resurrect event-driven neuromorphic Spiking Neural Networks (SNNs) with Address-Event Representation (AER) to keep circuits completely clockless and leakage-free during silence, or transition to cryogenic Josephson junction (SFQ/ERSFQ) logic to completely eliminate static power."
            })

        if inputs["memory_wall"] >= 1.5:
            hypotheses.append({
                "trigger": f"Off-chip memory latency and bandwidth limits scaled to {inputs['memory_wall']}x (severe Memory Wall).",
                "claim": "The energy and timing cost of shifting data from DRAM to CPU registers dominates compute overhead by up to two orders of magnitude.",
                "proposal": "Resurrect dynamic dataflow hardware with tagged-token matching architectures (such as the MIT J-Machine or TRIPS) to hide DRAM latency, or implement Burroughs-style segmented memory descriptors in hardware paired with Single-Level Store (SLS) persistent operating systems."
            })

        if inputs["security_risk"] >= 1.5:
            hypotheses.append({
                "trigger": f"Security exploit frequency and severity scaled to {inputs['security_risk']}x (Security Wall).",
                "claim": "Mainstream software-level virtual machine and OS rings fail to block spatial or temporal memory-corruption pointer exploits cleanly without massive performance degradation.",
                "proposal": "Resurrect unforgeable hardware-enforced Capability bounds checking registers (such as CHERI or Intel iAPX 432 object-descriptors) to secure multitenant boundaries at the hardware layer with less than 2% performance overhead."
            })

        if inputs["tensor_density"] >= 1.5:
            hypotheses.append({
                "trigger": f"AI and deep learning compute density scaled to {inputs['tensor_density']}x.",
                "claim": "Sequential von Neumann instruction fetching and multi-bit floating-point ALUs represent an unnecessarily complex execution model for highly-parallel and noise-tolerant linear algebra workloads.",
                "proposal": "Resurrect unipolar Stochastic Computing streams mapping multi-thousand-transistor arithmetic units to single 2-input AND logic gates, paired with continuous analog in-memory crossbar arrays (AIMC) calculating weights in-situ."
            })

        if inputs["cryo_penalty"] <= 0.7:
            hypotheses.append({
                "trigger": f"Cryogenic refrigeration penalty reduced to {inputs['cryo_penalty']}x (improved Carnot COP / High-Temperature Superconductors).",
                "claim": "The traditional thermodynamic cooling penalty that throttled the viability of superconducting logic is no longer the dominant cost barrier.",
                "proposal": "Resurrect multi-hundred-GHz classical control co-processors using picosecond-accurate Rapid Single Flux Quantum (RSFQ) pulse cells running natively inside quantum dilution refrigerators."
            })

        # Fallback default hypothesis if no extreme conditions are met
        if not hypotheses:
            hypotheses.append({
                "trigger": "Balanced physical constraints profile (all factors near 1.0).",
                "claim": "Under moderate CMOS scaling, heterogeneous revival remains a localized optimization problem.",
                "proposal": "Implement hybrid co-simulation fabrics bridging neural-probabilistic accelerators with unforgeable capability-bounds checkers to optimize the security-efficiency Pareto frontier."
            })

        return hypotheses

    def analyze_sensitivity(self, cmos_node: str = "planar-28nm") -> Dict[str, Any]:
        """
        Performs a systematic sensitivity analysis by sweeping each physical parameter individually
        from 0.1 to 10.0 (holding others at the node's baseline) for each lineage.
        Identifies the primary catalyst and the positive sensitivity slope for each lineage.
        """
        base_profile = self.CMOS_NODES.get(cmos_node, self.CMOS_NODES["planar-28nm"])
        parameters = ["copper_resistance", "memory_wall", "gate_leakage", "security_risk", "tensor_density", "cryo_penalty"]

        results = {}
        for lineage in self.LINEAGE_BASELINES.keys():
            results[lineage] = {
                "param_sensitivities": {},
                "primary_catalyst": None,
                "max_sensitivity_slope": -999.0
            }

            # Sweep each parameter holding others constant at base_profile
            for param in parameters:
                # Sweep from 0.1 to 10.0 in several steps to compute linear impact slope
                steps = [0.1, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
                scores = []
                for val in steps:
                    kwargs = {p: 1.0 for p in parameters} # We sweep multiplier factors on top of base_profile
                    kwargs[param] = val
                    f_res = self.forecast(cmos_node=cmos_node, **kwargs)
                    scores.append(f_res["forecasts"][lineage]["predicted"])

                # Slope = ΔScore / ΔFactor (dy/dx)
                slope = (scores[-1] - scores[0]) / 9.9
                results[lineage]["param_sensitivities"][param] = round(slope, 4)

                # Identify primary positive catalyst
                if slope > results[lineage]["max_sensitivity_slope"]:
                    results[lineage]["max_sensitivity_slope"] = round(slope, 4)
                    results[lineage]["primary_catalyst"] = param

        return results


def render_star_rating(score: float) -> str:
    """Converts a numerical score into a standard 5-character star string."""
    rounded = int(round(score))
    return "★" * rounded + "☆" * (5 - rounded)


def main():
    parser = argparse.ArgumentParser(
        description="Lightweight Predictive Hypothesis Engine: Maps emerging post-CMOS constraints to the revival readiness of forgotten architectural lineages."
    )
    parser.add_argument(
        "--copper-resistance",
        type=float,
        default=1.0,
        help="Interconnect copper resistance scale factor (default: 1.0, range: 0.1 - 10.0)"
    )
    parser.add_argument(
        "--memory-wall",
        type=float,
        default=1.0,
        help="Off-chip memory latency/bandwidth limit factor (default: 1.0, range: 0.1 - 10.0)"
    )
    parser.add_argument(
        "--gate-leakage",
        type=float,
        default=1.0,
        help="Sub-threshold static leakage power scale factor (default: 1.0, range: 0.1 - 10.0)"
    )
    parser.add_argument(
        "--security-risk",
        type=float,
        default=1.0,
        help="Software-level security exploit vulnerability frequency (default: 1.0, range: 0.1 - 10.0)"
    )
    parser.add_argument(
        "--tensor-density",
        type=float,
        default=1.0,
        help="AI tensor/matrix compute density in target workloads (default: 1.0, range: 0.1 - 10.0)"
    )
    parser.add_argument(
        "--cryo-penalty",
        type=float,
        default=1.0,
        help="Cryogenic refrigeration cooling penalty scale factor (default: 1.0, range: 0.1 - 10.0)"
    )
    parser.add_argument(
        "--cmos-node",
        type=str,
        default="planar-28nm",
        choices=["planar-28nm", "finfet-16nm", "gaa-3nm", "gaa-bspdn-2nm"],
        help="Baseline CMOS technology node configuration preset (default: planar-28nm)"
    )
    parser.add_argument(
        "--sensitivity",
        action="store_true",
        help="Run systematic sensitivity analysis sweep across all physical constraints and exit."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON results for automated AI ingestion instead of the text report."
    )

    args = parser.parse_args()

    engine = PredictiveHypothesisEngine()

    if args.sensitivity:
        results = engine.analyze_sensitivity(cmos_node=args.cmos_node)
        if args.json:
            import json
            print(json.dumps(results, indent=2))
            return

        print("\n" + "="*80)
        print(f"      PREDICTIVE HYPOTHESIS ENGINE: SENSITIVITY SWEEP ANALYSIS ({args.cmos_node.upper()})")
        print("="*80)
        print("  Systematically sweeping all physical modifiers [0.1 to 10.0] to isolate")
        print("  the primary catalyst (greatest positive slope dy/dx) for each lineage.")
        print("-" * 80)
        for lineage, info in results.items():
            print(f"  Lineage: {lineage}")
            print(f"    - Primary Catalyst:      {info['primary_catalyst']} (Slope: +{info['max_sensitivity_slope']:.4f})")
            print("    - Parameter Sensitivity Slopes (dy/dx):")
            for p, slope in info["param_sensitivities"].items():
                print(f"        * {p:<20}: {slope:+.4f}")
            print("-" * 80)
        return

    result = engine.forecast(
        copper_resistance=args.copper_resistance,
        memory_wall=args.memory_wall,
        gate_leakage=args.gate_leakage,
        security_risk=args.security_risk,
        tensor_density=args.tensor_density,
        cryo_penalty=args.cryo_penalty,
        cmos_node=args.cmos_node
    )

    if args.json:
        import json
        print(json.dumps(result, indent=2))
        return

    # Render a beautiful terminal dashboard
    print("\n" + "="*80)
    print("      DIGITAL ARCHAEOLOGY: CONSTRAINT MIGRATION PREDICTIVE HYPOTHESIS ENGINE")
    print("="*80)
    print("  Modeling future architectural transitions (2026-2036) by mapping emerging")
    print("  post-CMOS physical and economic limits to alternative hardware lineages.")
    print("-" * 80)
    print(f"  CMOS BASELINE NODE: {args.cmos_node.upper()}")
    print("  INPUTS PROFILE:")
    print(f"    - Nanoscale Copper Interconnect Resistance:   {result['inputs']['copper_resistance']:.2f}x")
    print(f"    - Memory Wall Limit (Off-chip Latency):      {result['inputs']['memory_wall']:.2f}x")
    print(f"    - Sub-threshold Static Gate Leakage:         {result['inputs']['gate_leakage']:.2f}x")
    print(f"    - Security Exploit Vulnerability Frequency:  {result['inputs']['security_risk']:.2f}x")
    print(f"    - AI Workload Compute / Tensor Density:      {result['inputs']['tensor_density']:.2f}x")
    print(f"    - Cryogenic Refrigeration Cooling Penalty:   {result['inputs']['cryo_penalty']:.2f}x")
    print("-" * 80)

    # Render score table
    print(f"  {'ARCHITECTURAL LINEAGE':<38} | {'BASELINE':<8} | {'FORECASTED':<10} | {'DELTA':<6}")
    print("-" * 80)
    for lineage in result["ranking"]:
        f_data = result["forecasts"][lineage]
        stars = render_star_rating(f_data["predicted"])
        delta_str = f"+{f_data['delta']:.2f}" if f_data["delta"] > 0 else f"{f_data['delta']:.2f}"
        print(f"  {lineage:<38} | {f_data['baseline']:.2f}     | {f_data['predicted']:.2f} {stars} | {delta_str}")
    print("-" * 80)

    # Print the top-ranked lineage
    print(f"  ✓ TOP-RANKED REVIVAL CANDIDATE: {result['ranking'][0]} ({result['forecasts'][result['ranking'][0]]['predicted']:.2f} / 5.0)")
    print("-" * 80)

    # Render hypotheses
    print("  GENERATED ARCHITECTURAL HYPOTHESES:")
    for idx, hyp in enumerate(result["hypotheses"], 1):
        print(f"\n    [{idx}] TRIGGER: {hyp['trigger']}")
        print(f"        CLAIM:   {hyp['claim']}")
        print(f"        PROPOSAL: {hyp['proposal']}")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
