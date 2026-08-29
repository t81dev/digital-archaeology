#!/usr/bin/env python3
"""
Unit tests for SteamOS Dual-Session, Gamescope, Proton & Immutable A/B Update Simulator.
"""

import pytest
from reconstructions.steamos_dual_session.steamos_sim import (
    SteamOSSessionManager,
    SessionMode,
    PartitionTarget,
    GamescopeCompositor,
    ProtonTranslationPipeline,
    ImmutableUpdateEngine,
)


def test_gamescope_compositor_scaling_and_pacing():
    compositor = GamescopeCompositor(display_res=(1280, 800), target_fps=60)
    config = compositor.set_display_config(40, "FSR")

    assert config["target_fps"] == 40
    assert config["scaling_filter"] == "FSR"
    assert config["frame_time_ms"] == 25.0

    frame = compositor.render_frame((1280, 720), "3D Frame")
    assert frame["frame_id"] == 1
    assert frame["scale_factor"] == (1.0, 1.11)
    assert "[FSR Scaled 1.0x] 3D Frame" in frame["composited_output"]

    # Toggle overlay
    compositor.toggle_overlay(True)
    frame_overlay = compositor.render_frame((1280, 720), "3D Frame")
    assert "Steam QuickAccess Overlay" in frame_overlay["composited_output"]


def test_gamescope_invalid_fps():
    compositor = GamescopeCompositor()
    with pytest.raises(ValueError):
        compositor.set_display_config(144, "FSR")


def test_proton_translation_pipeline():
    proton = ProtonTranslationPipeline()
    pfx = proton.create_prefix("cyberpunk_2077")
    assert "cyberpunk_2077" in pfx

    # Direct3D 11 translation
    d3d = proton.translate_call("Direct3D11", "D3D11_DrawIndexed(500, 0, 0)")
    assert d3d["translated_api"] == "Vulkan SPIR-V"
    assert "vkCmd_DrawIndexedIndirect" in d3d["translated_execution"]

    # Win32 Sync translation
    sync = proton.translate_call("Win32_Sync", "WaitForSingleObject(hMutex, 50)")
    assert sync["translated_api"] == "POSIX / Linux Syscall"
    assert "sys_futex_waitv" in sync["translated_execution"]


def test_immutable_update_engine_protection():
    engine = ImmutableUpdateEngine()

    # System write fail on read-only
    success, msg = engine.write_system_file("/usr/lib/libtest.so", "data")
    assert success is False
    assert "Read-only filesystem" in msg

    # Mutable write success
    success_user, msg_user = engine.write_system_file("/home/deck/file.txt", "hello")
    assert success_user is True
    assert "Mutable User Partition" in msg_user

    # Enable developer read-write mode
    engine.set_read_only(False)
    success_dev, msg_dev = engine.write_system_file("/usr/bin/tool", "data")
    assert success_dev is True
    assert "Developer Mode" in msg_dev


def test_immutable_update_atomic_ab_and_rollback():
    engine = ImmutableUpdateEngine()
    assert engine.active_partition == PartitionTarget.ROOTFS_A

    # Apply update onto ROOTFS_B
    result = engine.apply_update("3.6.0")
    assert result["status"] == "UPDATE_SUCCESS"
    assert engine.active_partition == PartitionTarget.ROOTFS_B
    assert result["installed_version"] == "3.6.0"

    # Simulate boot corruption and check automatic rollback
    boot = engine.boot_check(simulate_failure=True)
    assert boot["boot_status"] == "FAILED"
    assert boot["action"] == "AUTOMATIC_ROLLBACK"
    assert engine.active_partition == PartitionTarget.ROOTFS_A
    assert boot["restored_version"] == "3.5.7"


def test_steamos_session_manager_lifecycle():
    session = SteamOSSessionManager()
    assert session.current_mode == SessionMode.GAMING

    # Launch games
    p1 = session.launch_game("game1", "Game 1", is_win32=True)
    p2 = session.launch_game("game2", "Game 2", is_win32=False)
    assert len(session.running_processes) == 2

    # Switch session terminates games
    swap = session.switch_session(SessionMode.DESKTOP)
    assert swap["status"] == "SESSION_SWAPPED"
    assert swap["new_mode"] == "desktop_mode"
    assert swap["games_terminated"] == 2
    assert len(session.running_processes) == 0

    # No-op switch
    noop = session.switch_session(SessionMode.DESKTOP)
    assert noop["status"] == "NO_OP"
