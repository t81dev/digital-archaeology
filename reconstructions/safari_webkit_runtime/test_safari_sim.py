"""
Unit Tests for WebKit & Safari Web Runtime Architecture Simulator
===================================================================

Tests:
1. WebKit2 Multi-Process Isolation & Crash Resilience
2. IPC Message Routing & Navigation Policy Enforcement
3. Intelligent Tracking Prevention (ITP) Double-Keyed Storage Partitioning
4. ITP Storage Access API Grant Lifecycle
"""

import pytest
from reconstructions.safari_webkit_runtime.safari_sim import (
    WebKit2ProcessCoordinator,
    WKWebViewHost,
    SecurityOrigin,
    IPCMessage
)


def test_webkit2_process_isolation_and_crash_resilience():
    coordinator = WebKit2ProcessCoordinator()
    host_app = WKWebViewHost(coordinator)

    # Load web page inside embedded WKWebView
    host_app.load_url("https://example.com")
    assert host_app.page_loaded_url == "https://example.com"
    assert host_app.active_process is not None
    active_proc_id = host_app.active_process.process_id

    # Trigger crash inside Web Content Process
    host_app.trigger_web_content_crash()

    # Verify Web Content Process crashed and was removed from coordinator
    assert active_proc_id in coordinator.crashed_process_ids
    assert active_proc_id not in coordinator.web_content_processes

    # Verify Host App Process remains alive and un-crashed (Process Isolation)
    assert host_app.is_host_alive() is True


def test_webkit2_navigation_policy_ipc():
    coordinator = WebKit2ProcessCoordinator()
    host_app = WKWebViewHost(coordinator)

    origin = SecurityOrigin("https", "bank.com")
    proc = coordinator.spawn_web_content_process(origin)

    # Test valid navigation
    res = proc.request_navigation("https://bank.com/dashboard")
    assert res["allow"] is True

    # Test unsafe javascript: scheme navigation blocked by UI Process delegate
    res_unsafe = proc.request_navigation("javascript:alert(1)")
    assert res_unsafe["allow"] is False


def test_itp_double_keyed_storage_partitioning():
    coordinator = WebKit2ProcessCoordinator()

    top_origin_a = SecurityOrigin("https", "site-a.com")
    top_origin_b = SecurityOrigin("https", "site-b.com")
    tracker_origin = SecurityOrigin("https", "tracker.com")

    proc_a = coordinator.spawn_web_content_process(tracker_origin)
    proc_b = coordinator.spawn_web_content_process(tracker_origin)

    # Tracker sets cookie when embedded on Site A
    proc_a.write_storage(key="user_id", value="TRACKER_ID_12345", top_level_origin=top_origin_a)

    # Tracker reads storage when embedded on Site A
    val_a = proc_a.read_storage(key="user_id", top_level_origin=top_origin_a)
    assert val_a == "TRACKER_ID_12345"

    # Tracker reads storage when embedded on Site B
    val_b = proc_b.read_storage(key="user_id", top_level_origin=top_origin_b)
    # Storage must be partitioned - tracker on Site B receives None (isolated bucket)
    assert val_b is None


def test_itp_storage_access_api_grant():
    coordinator = WebKit2ProcessCoordinator()

    top_origin = SecurityOrigin("https", "news.com")
    embed_origin = SecurityOrigin("https", "comments.com")

    proc = coordinator.spawn_web_content_process(embed_origin)

    # Without Storage Access API grant, storage is partitioned
    proc.write_storage(key="session", value="SESS_99", top_level_origin=top_origin)
    assert proc.read_storage(key="session", top_level_origin=top_origin) == "SESS_99"

    # Request Storage Access API without user interaction -> Denied
    msg_denied = IPCMessage(
        msg_type="RequestStorageAccess",
        sender_process=f"WebContentProcess-{proc.process_id}",
        target_process="NetworkProcess",
        payload={
            "top_origin": top_origin.to_string(),
            "sub_origin": embed_origin.to_string(),
            "user_interacted": False
        },
        message_id=coordinator.get_next_msg_id()
    )
    res = coordinator.send_message(msg_denied)
    assert res["granted"] is False

    # Request Storage Access API with user interaction -> Granted
    msg_granted = IPCMessage(
        msg_type="RequestStorageAccess",
        sender_process=f"WebContentProcess-{proc.process_id}",
        target_process="NetworkProcess",
        payload={
            "top_origin": top_origin.to_string(),
            "sub_origin": embed_origin.to_string(),
            "user_interacted": True
        },
        message_id=coordinator.get_next_msg_id()
    )
    res_granted = coordinator.send_message(msg_granted)
    assert res_granted["granted"] is True

    # After Storage Access grant, unpartitioned storage is accessible across origins
    proc.write_storage(key="global_cookie", value="GLOBAL_USER_KEY", top_level_origin=top_origin)
    assert proc.read_storage(key="global_cookie", top_level_origin=top_origin) == "GLOBAL_USER_KEY"
