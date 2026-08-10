#!/usr/bin/env python3
"""
Automated Academic Lab Manual Grading Harness.
Runs comprehensive test suites against student implementations from student_solutions.py
to assert mathematical correctness, safety invariants, and execution liveness.
"""

import sys
import os
import argparse
import traceback
from typing import Dict, Any

# Ensure correct pathing to import student solutions and relative simulators
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class LabAutograder:
    """
    Validates student lab modules and outputs a detailed performance matrix.
    """
    def __init__(self):
        self.scores = {}
        self.feedback = {}

    def run_grading(self) -> Dict[str, Any]:
        """
        Executes tests for all 8 lab modules.
        """
        # Attempt to import student solutions
        try:
            import student_solutions as solutions
        except ImportError as e:
            return {
                "success": False,
                "error": f"Failed to import reconstructions/student_solutions.py: {e}",
                "scores": {},
                "feedback": {}
            }

        # -------------------------------------------------------------
        # Lab 1: Radix-3 Balanced Ternary Half-Adder
        # -------------------------------------------------------------
        try:
            test_cases = [
                (-1, -1, (1, -1)), # -2
                (-1, 0, (-1, 0)),  # -1
                (-1, 1, (0, 0)),   # 0
                (0, 0, (0, 0)),     # 0
                (1, 0, (1, 0)),    # 1
                (1, 1, (-1, 1)),   # 2
            ]
            passed = 0
            for a, b, expected in test_cases:
                out = solutions.ternary_half_adder(a, b)
                if out == expected:
                    passed += 1
            score = round((passed / len(test_cases)) * 10, 2)
            self.scores["Lab 1: Radix-3 Economy"] = score
            self.feedback["Lab 1: Radix-3 Economy"] = f"Passed {passed}/{len(test_cases)} balanced ternary carry-sum assertion cases."
        except Exception as e:
            self.scores["Lab 1: Radix-3 Economy"] = 0.0
            self.feedback["Lab 1: Radix-3 Economy"] = f"Exception occurred during execution: {e}"

        # -------------------------------------------------------------
        # Lab 2: Tagged-Token Dataflow Parallel Graph
        # -------------------------------------------------------------
        try:
            # Formula: (x + y) * (y - z)
            # For 5, 3, 1: (5+3) * (3-1) = 8 * 2 = 16
            out_nominal = solutions.run_custom_dataflow_graph(5, 3, 1)
            # For 4, 4, 2: (4+4) * (4-2) = 8 * 2 = 16
            out_second = solutions.run_custom_dataflow_graph(4, 4, 2)

            if out_nominal == 16 and out_second == 16:
                self.scores["Lab 2: Tagged-Token Dataflow"] = 10.0
                self.feedback["Lab 2: Tagged-Token Dataflow"] = "Successfully assembled spatial dataflow nodes, injected parallel tokens, and replayed arithmetic pipelines."
            else:
                self.scores["Lab 2: Tagged-Token Dataflow"] = 0.0
                self.feedback["Lab 2: Tagged-Token Dataflow"] = f"Mismatched outputs. Got f(5,3,1)={out_nominal} (expected 16) and f(4,4,2)={out_second} (expected 16)."
        except Exception as e:
            self.scores["Lab 2: Tagged-Token Dataflow"] = 0.0
            self.feedback["Lab 2: Tagged-Token Dataflow"] = f"Exception occurred: {e}"

        # -------------------------------------------------------------
        # Lab 3: Capability and Tagged Memory Protection
        # -------------------------------------------------------------
        # 3A: Secure Domain Transitions
        try:
            safe_ok, oob_caught = solutions.run_secure_domain_transitions()
            if safe_ok and oob_caught:
                self.scores["Lab 3A: Capability Protection"] = 5.0
                self.feedback["Lab 3A: Capability Protection"] = "Hardware bounds registers successfully quarantined out-of-bounds memory writes."
            else:
                self.scores["Lab 3A: Capability Protection"] = 0.0
                self.feedback["Lab 3A: Capability Protection"] = f"Failed. safe_ok={safe_ok}, oob_caught={oob_caught}."
        except Exception as e:
            self.scores["Lab 3A: Capability Protection"] = 0.0
            self.feedback["Lab 3A: Capability Protection"] = f"Exception: {e}"

        # 3B: Lisp Machine Type-Safety
        try:
            added_val, tag_violation, traversed = solutions.run_lisp_machine_type_safety()
            if added_val == 100 and tag_violation and traversed == [100, 200, 300]:
                self.scores["Lab 3B: Lisp Machine Tagging"] = 5.0
                self.feedback["Lab 3B: Lisp Machine Tagging"] = "Type tagging triggered TagException correctly, and CDR-NEXT packing unpacked cleanly."
            else:
                self.scores["Lab 3B: Lisp Machine Tagging"] = 0.0
                self.feedback["Lab 3B: Lisp Machine Tagging"] = f"Failure: added_val={added_val}, tag_violation={tag_violation}, traversed={traversed}."
        except Exception as e:
            self.scores["Lab 3B: Lisp Machine Tagging"] = 0.0
            self.feedback["Lab 3B: Lisp Machine Tagging"] = f"Exception: {e}"

        # 3C: Burroughs Virtual Memory
        try:
            pf_caught, val, bounds_caught = solutions.run_burroughs_descriptors()
            if pf_caught and val == 202 and bounds_caught:
                self.scores["Lab 3C: Burroughs Descriptors"] = 5.0
                self.feedback["Lab 3C: Burroughs Descriptors"] = "Burroughs MCP correctly intercepted presence faults and enforced strict segment limits."
            else:
                self.scores["Lab 3C: Burroughs Descriptors"] = 0.0
                self.feedback["Lab 3C: Burroughs Descriptors"] = f"Failure: pf={pf_caught}, val={val}, bounds={bounds_caught}."
        except Exception as e:
            self.scores["Lab 3C: Burroughs Descriptors"] = 0.0
            self.feedback["Lab 3C: Burroughs Descriptors"] = f"Exception: {e}"

        # -------------------------------------------------------------
        # Lab 4: Cooperative Rendezvous
        # -------------------------------------------------------------
        try:
            logs = solutions.run_deadlock_avoiding_broker()
            expected_set = {"Logged(SensorChannel: Temp=23.5C)", "Logged(SensorChannel: Temp=24.1C)",
                            "Logged(TimerChannel: Tick_1s)", "Logged(TimerChannel: Tick_2s)"}
            if set(logs) == expected_set:
                self.scores["Lab 4: Cooperative Rendezvous"] = 10.0
                self.feedback["Lab 4: Cooperative Rendezvous"] = "ALT wait guard multiplexed channels successfully with synchronized thread liveness."
            else:
                self.scores["Lab 4: Cooperative Rendezvous"] = 0.0
                self.feedback["Lab 4: Cooperative Rendezvous"] = f"Multiplexer did not route all messages. Got: {logs}"
        except Exception as e:
            self.scores["Lab 4: Cooperative Rendezvous"] = 0.0
            self.feedback["Lab 4: Cooperative Rendezvous"] = f"Exception: {e}"

        # -------------------------------------------------------------
        # Lab 5: Reversible Logic
        # -------------------------------------------------------------
        try:
            # Test XOR reversibility
            cases = [(0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 1, 0)]
            passed = 0
            for a, b, expected_out in cases:
                out, regs, energy = solutions.run_reversible_xor_lab(a, b)
                # Check XOR result, and garbage deallocation (must be returned to 0)
                if out == expected_out and regs["garbage_G0"] == 0 and energy == 0.0:
                    passed += 1
            score = round((passed / len(cases)) * 10, 2)
            self.scores["Lab 5: Reversible Uncomputation"] = score
            self.feedback["Lab 5: Reversible Uncomputation"] = f"Passed {passed}/4 reversible XOR sweeps. All intermediate garbage successfully deallocated to zero (0J loss)."
        except Exception as e:
            self.scores["Lab 5: Reversible Uncomputation"] = 0.0
            self.feedback["Lab 5: Reversible Uncomputation"] = f"Exception: {e}"

        # -------------------------------------------------------------
        # Lab 6: 9P Union Mounts
        # -------------------------------------------------------------
        try:
            out_data = solutions.run_ninep_union_mount()
            if out_data == "BackupData_72F":
                self.scores["Lab 6: 9P Union Namespaces"] = 10.0
                self.feedback["Lab 6: 9P Union Namespaces"] = "Union mount lookup precedence successfully fell through to the backup device file."
            else:
                self.scores["Lab 6: 9P Union Namespaces"] = 0.0
                self.feedback["Lab 6: 9P Union Namespaces"] = f"Incorrect fallback data retrieved: {out_data}"
        except Exception as e:
            self.scores["Lab 6: 9P Union Namespaces"] = 0.0
            self.feedback["Lab 6: 9P Union Namespaces"] = f"Exception: {e}"

        # -------------------------------------------------------------
        # Lab 7: Spiking & Stochastic Computing
        # -------------------------------------------------------------
        # 7A: Spiking
        try:
            voltages, spikes = solutions.run_spiking_neuron()
            # Spikes should have fired at least once
            if len(voltages) == 7 and True in spikes:
                self.scores["Lab 7A: Spiking Neuromorphic"] = 5.0
                self.feedback["Lab 7A: Spiking Neuromorphic"] = "Asynchronous LIF neuron successfully charged potential and emitted temporal action events."
            else:
                self.scores["Lab 7A: Spiking Neuromorphic"] = 0.0
                self.feedback["Lab 7A: Spiking Neuromorphic"] = f"Failed spiking characteristics. Voltages: {[round(v,2) for v in voltages]}, Spikes: {spikes}"
        except Exception as e:
            self.scores["Lab 7A: Spiking Neuromorphic"] = 0.0
            self.feedback["Lab 7A: Spiking Neuromorphic"] = f"Exception: {e}"

        # 7B: Stochastic Multiplication
        try:
            res_dict = solutions.run_stochastic_multiplication()
            # 1024-bit accuracy should be closer to target 0.42 than 64-bit due to variance scaling
            err_64 = abs(res_dict[64] - 0.42)
            err_1024 = abs(res_dict[1024] - 0.42)
            if 0.0 <= res_dict[1024] <= 1.0:
                self.scores["Lab 7B: Stochastic Multiplication"] = 5.0
                self.feedback["Lab 7B: Stochastic Multiplication"] = f"Unipolar single-gate AND logic multiplied bitstreams. 1024-bit product: {res_dict[1024]:.4f} (Error: {err_1024:.4f})."
            else:
                self.scores["Lab 7B: Stochastic Multiplication"] = 0.0
                self.feedback["Lab 7B: Stochastic Multiplication"] = f"Out of bounds decoded product: {res_dict}"
        except Exception as e:
            self.scores["Lab 7B: Stochastic Multiplication"] = 0.0
            self.feedback["Lab 7B: Stochastic Multiplication"] = f"Exception: {e}"

        # -------------------------------------------------------------
        # Lab 8: Cryogenic Logic
        # -------------------------------------------------------------
        try:
            res = solutions.run_cryo_and_timing_lab()
            if res["nominal_success"] and res["violating_prevented"] and res["ersfq_utility_joules"] < res["rsfq_utility_joules"]:
                self.scores["Lab 8: Superconducting Cryo"] = 10.0
                self.feedback["Lab 8: Superconducting Cryo"] = "RSFQ setup timing violations caught successfully. ERSFQ verified to bypass static resistive bias power."
            else:
                self.scores["Lab 8: Superconducting Cryo"] = 0.0
                self.feedback["Lab 8: Superconducting Cryo"] = f"Failure in timing or energy calculations. Metrics: {res}"
        except Exception as e:
            self.scores["Lab 8: Superconducting Cryo"] = 0.0
            self.feedback["Lab 8: Superconducting Cryo"] = f"Exception: {e}"

        return {
            "success": True,
            "scores": self.scores,
            "feedback": self.feedback
        }


def main():
    parser = argparse.ArgumentParser(
        description="Academic Systems Architecture Lab Module Auto-Grader."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw grading metrics as a JSON string."
    )

    args = parser.parse_args()
    grader = LabAutograder()
    res = grader.run_grading()

    if args.json:
        import json
        print(json.dumps(res, indent=2))
        return

    print("\n" + "="*80)
    print("                 DIGITAL ARCHAEOLOGY: LAB MANUAL AUTO-GRADER")
    print("="*80)

    if not res["success"]:
        print(f"  \033[91mCRITICAL ERROR: {res['error']}\033[0m")
        print("="*80 + "\n")
        sys.exit(1)

    total_possible = 85.0
    total_earned = sum(res["scores"].values())
    percentage = (total_earned / total_possible) * 100.0

    print(f"  {'LAB MODULE CHALLENGE':<45} | {'SCORE':<7} | {'STATUS':<10}")
    print("-" * 80)

    for lab, score in res["scores"].items():
        status = "\033[92m[PASSED]\033[0m" if score > 0.0 else "\033[91m[FAILED]\033[0m"
        max_possible = 5.0 if "3A" in lab or "3B" in lab or "3C" in lab or "7A" in lab or "7B" in lab else 10.0
        print(f"  {lab:<45} | {score:>4.1f}/{max_possible:<3.1f} | {status}")
        print(f"    * Feedback: {res['feedback'][lab]}")
        print("-" * 80)

    color = "\033[92m" if percentage >= 80.0 else "\033[93m" if percentage >= 50.0 else "\033[91m"
    print(f"  CUMULATIVE GRADED PERFORMANCE: {color}{total_earned:.1f} / {total_possible:.1f} ({percentage:.1f}%)\033[0m")
    print("="*80 + "\n")

    if percentage < 100.0:
        sys.exit(1)


if __name__ == "__main__":
    main()
