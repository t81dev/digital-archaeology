"""
Unit tests for Netscape Browser Runtime & Network Client Simulator.
Verifies DOM Host, Same-Origin Policy (SOP), NPAPI Dispatcher, Cookie Engine, and SSL Trust Evaluator.
"""

import time
import pytest
from reconstructions.netscape_browser_runtime.netscape_sim import (
    CookieRecord,
    CookieEngine,
    X509Certificate,
    SSLTrustEvaluator,
    NPAPIPluginFuncs,
    NPAPIDispatcher,
    Origin,
    DOMElement,
    DOMDocument,
    NetscapeDOMHost
)


def test_cookie_engine_parsing_and_scoping():
    engine = CookieEngine()
    current_time = 100000.0

    # Parse cookie header
    set_cookie = "CUSTOMER=WILEY_9021; domain=.netscape.com; path=/cart; secure; expires=200000.0"
    rec = engine.parse_set_cookie(set_cookie, request_host="merchant.netscape.com", request_path="/cart")

    assert rec is not None
    assert rec.name == "CUSTOMER"
    assert rec.value == "WILEY_9021"
    assert rec.domain == "netscape.com"
    assert rec.path == "/cart"
    assert rec.secure is True

    # Matching test 1: Valid HTTPS request matching domain and path
    hdr_valid = engine.get_cookie_header_for_request("https://merchant.netscape.com/cart/checkout", current_time)
    assert hdr_valid == "Cookie: CUSTOMER=WILEY_9021"

    # Matching test 2: Insecure HTTP request (should be blocked because secure=True)
    hdr_insecure = engine.get_cookie_header_for_request("http://merchant.netscape.com/cart/checkout", current_time)
    assert hdr_insecure == ""

    # Matching test 3: Mismatched path (should be blocked)
    hdr_wrong_path = engine.get_cookie_header_for_request("https://merchant.netscape.com/account", current_time)
    assert hdr_wrong_path == ""

    # Matching test 4: Expired cookie
    hdr_expired = engine.get_cookie_header_for_request("https://merchant.netscape.com/cart/checkout", current_time=250000.0)
    assert hdr_expired == ""


def test_ssl_trust_evaluator():
    evaluator = SSLTrustEvaluator()
    current_time = 100000.0

    valid_cert = X509Certificate(
        domain_pattern="*.netscape.com",
        issuer="VeriSign Root CA",
        public_key_rsa="RSA_PUBLIC_KEY_3072",
        valid_until_timestamp=200000.0,
        signature_valid=True
    )

    # Test 1: Successful HTTPS handshake
    res1 = evaluator.perform_handshake("https://home.netscape.com/index.html", valid_cert, current_time)
    assert res1["status"] == "HANDSHAKE_SUCCESSFUL"
    assert res1["secure"] is True
    assert res1["lock_icon"] == "🔒"

    # Test 2: Untrusted issuer
    bad_issuer_cert = X509Certificate(
        domain_pattern="*.netscape.com",
        issuer="Unknown Rogue CA",
        public_key_rsa="RSA_PUBLIC_KEY_3072",
        valid_until_timestamp=200000.0
    )
    res2 = evaluator.perform_handshake("https://home.netscape.com/index.html", bad_issuer_cert, current_time)
    assert res2["status"] == "UNTRUSTED_ISSUER"
    assert res2["secure"] is False
    assert res2["lock_icon"] == "🔓"

    # Test 3: Hostname mismatch
    res3 = evaluator.perform_handshake("https://www.example.org/index.html", valid_cert, current_time)
    assert res3["status"] == "HOSTNAME_MISMATCH"
    assert res3["secure"] is False

    # Test 4: Expired cert
    res4 = evaluator.perform_handshake("https://home.netscape.com/index.html", valid_cert, current_time=300000.0)
    assert res4["status"] == "EXPIRED_CERTIFICATE"
    assert res4["secure"] is False


def test_npapi_plugin_dispatcher():
    dispatcher = NPAPIDispatcher()

    flash_plugin = NPAPIPluginFuncs(mime_type="application/x-shockwave-flash", plugin_name="Macromedia Flash")
    dispatcher.register_plugin(flash_plugin)

    # Embed flash element
    plug_ref = dispatcher.embed_element(
        mime_type="application/x-shockwave-flash",
        instance_id="flash_inst_1",
        window_handle="HWND_0x99238",
        width=400,
        height=300
    )

    assert plug_ref is not None
    assert "flash_inst_1" in flash_plugin.active_instances
    assert flash_plugin.active_instances["flash_inst_1"]["window_handle"] == "HWND_0x99238"

    # Stream data into plugin
    written = flash_plugin.NPP_Write("flash_inst_1", b"FLASH_HEADER_SWF_DATA")
    assert written == 21
    assert len(flash_plugin.active_instances["flash_inst_1"]["data_stream"]) == 1

    # Call NPN_ host functions
    fetched = dispatcher.npn_funcs.NPN_GetURL("flash_inst_1", "https://site.com/movie.swf")
    assert "HOST_FETCHING" in fetched

    mem_addr = dispatcher.npn_funcs.NPN_MemAlloc(1024)
    assert mem_addr > 0

    # Destroy instance
    destroyed = flash_plugin.NPP_Destroy("flash_inst_1")
    assert destroyed is True
    assert "flash_inst_1" not in flash_plugin.active_instances


def test_netscape_dom_host_and_same_origin_policy():
    host = NetscapeDOMHost()

    # Create top document and iframe documents
    doc_top = host.create_document("top_win", "https://bank.com:443/account")
    doc_sub1 = host.create_document("frame_same", "https://bank.com:443/statement")
    doc_sub2 = host.create_document("frame_cross", "https://attacker.org:443/phish")

    # Add form to same-origin frame
    form = doc_sub1.add_form("loginForm")
    form.value = "UserSessionActive"

    # Add event listener
    event_triggered = []
    def on_submit_handler():
        event_triggered.append("SUBMITTED")
        return True

    form.attach_event_listener("onsubmit", on_submit_handler)
    res_submit = form.dispatch_event("onsubmit")
    assert res_submit is True
    assert event_triggered == ["SUBMITTED"]

    # Test Same-Origin Policy Access
    # Same origin: bank.com -> bank.com
    success_same, val_same = host.execute_script_cross_frame_access("top_win", "frame_same", "loginForm")
    assert success_same is True
    assert val_same == "UserSessionActive"

    # Cross origin: bank.com -> attacker.org (Blocked by SOP)
    success_cross, val_cross = host.execute_script_cross_frame_access("top_win", "frame_cross", "forms")
    assert success_cross is False
    assert "SecurityException" in val_cross
