"""Static smoke tests for browser features that cannot run in Python CI.

These assertions test the public page contract: configured simulator sources
exist, WebRTC local signaling remains available, and exported traces are
standard VCD-shaped text.
"""

import os
import re


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def read_playground():
    with open(os.path.join(ROOT_DIR, "playground.html"), encoding="utf-8") as page:
        return page.read()


def test_configured_playground_simulators_exist():
    page = read_playground()
    paths = re.findall(r"path:\s*'([^']+\.py)'", page)
    assert len(paths) >= 7
    for path in paths:
        assert os.path.isfile(os.path.join(ROOT_DIR, path)), path


def test_playground_keeps_local_p2p_signaling_contract():
    page = read_playground()
    assert "new BroadcastChannel('digital_archaeology_cluster')" in page
    assert "new RTCPeerConnection(configuration)" in page
    assert "createDataChannel('co-sim-grid'" in page


def test_vcd_export_has_standard_headers_and_download_path():
    page = read_playground()
    export_fn = re.search(
        r"function exportWaveformToVCD\(\)\s*\{(?P<body>.*?)\n        \}",
        page,
        re.DOTALL,
    )
    assert export_fn
    body = export_fn.group("body")
    for marker in ("$timescale", "$scope module top $end", "$enddefinitions", "$dumpvars"):
        assert marker in body
    assert "new Blob([vcd]" in body
    assert "_waveform.vcd" in body


def test_playground_has_webserial_webusb_hil_hooks():
    page = read_playground()
    assert "toggleWebSerialHIL" in page
    assert "parseHILTelemetryLine" in page
    assert "navigator.serial.requestPort" in page
