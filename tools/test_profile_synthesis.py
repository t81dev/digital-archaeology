"""Tests for provenance and estimate labeling in hardware synthesis reports."""

import json
import os
import subprocess
import sys


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def test_json_report_includes_provenance_and_measurement_kind(tmp_path):
    output = tmp_path / "profile.json"
    command = [
        sys.executable,
        "tools/profile_synthesis.py",
        "--module",
        "capability_bounds_checker",
        "--output",
        str(output),
    ]
    result = subprocess.run(command, cwd=ROOT_DIR, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr

    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["provenance"]["python_version"]
    assert "yosys" in report["provenance"]["toolchains"]
    metrics = report["results"]["capability_bounds_checker"]
    assert metrics["measurement_kind"] in {"analytical_estimate", "toolchain_estimate"}
