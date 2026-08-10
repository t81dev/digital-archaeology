import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lab_autograder import LabAutograder


def test_autograder_perfect_score():
    """
    Asserts that the model solutions in student_solutions.py achieve a perfect 85/85 score.
    """
    grader = LabAutograder()
    results = grader.run_grading()

    assert results["success"] is True
    assert len(results["scores"]) == 11

    total_earned = sum(results["scores"].values())
    assert total_earned == 85.0
