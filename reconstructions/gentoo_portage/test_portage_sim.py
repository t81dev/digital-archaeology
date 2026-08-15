#!/usr/bin/env python3
"""
Unit tests for Portage Engine, USE Flag & Profile Simulator.
Tests profile cascades, USE flag dependency mutation, slotting, sandbox violations, and VDB tracking.
"""

import pytest
from reconstructions.gentoo_portage.portage_sim import (
    ProfileCascade,
    USEEvaluator,
    Ebuild,
    VarDB,
    PortageDependencySolver,
    EbuildSandboxRunner
)

def test_profile_cascade_defaults():
    profile = ProfileCascade()
    global_use = profile.get_effective_global_use()

    # Check default active flags
    assert "unicode" in global_use
    assert "ssl" in global_use
    assert "gui" in global_use
    assert "systemd" not in global_use # Negated in desktop layer

def test_profile_cascade_overrides():
    profile = ProfileCascade()
    profile.set_local_make_conf(["-gui", "wayland", "systemd"])
    profile.set_local_package_use("media-video/ffmpeg", ["vpx", "nvenc", "-ssl"])

    global_use = profile.get_effective_global_use()
    assert "gui" not in global_use
    assert "wayland" in global_use
    assert "systemd" in global_use

    ffmpeg_use = profile.get_effective_package_use("media-video/ffmpeg")
    assert "vpx" in ffmpeg_use
    assert "nvenc" in ffmpeg_use
    assert "ssl" not in ffmpeg_use

def test_package_masking():
    profile = ProfileCascade()
    assert profile.is_package_masked("sys-apps/systemd-legacy") is True
    assert profile.is_package_masked("app-editors/vim") is False

    profile.mask_package("app-editors/vim")
    assert profile.is_package_masked("app-editors/vim") is True

def test_use_evaluator_conditional_deps():
    active_use = {"ssl", "python", "X"}
    raw_deps = "sys-libs/ncurses ssl? ( dev-libs/openssl ) !gui? ( dev-libs/libcli ) x11? ( x11-libs/libX11 )"

    parsed = USEEvaluator.parse_conditional_deps(raw_deps, active_use)
    assert "sys-libs/ncurses" in parsed
    assert "dev-libs/openssl" in parsed # Active ssl
    assert "dev-libs/libcli" in parsed  # Active !gui (gui not in active_use)
    assert "x11-libs/libX11" not in parsed # x11 not in active_use

def test_dependency_solver_use_mutation():
    profile = ProfileCascade()
    vdb = VarDB()
    solver = PortageDependencySolver(profile, vdb)

    glibc = Ebuild("sys-libs/glibc", "2.38")
    openssl = Ebuild("dev-libs/openssl", "3.0")
    vim_no_ssl = Ebuild("app-editors/vim", "9.0", iuse=["ssl"], raw_depend="sys-libs/glibc ssl? ( dev-libs/openssl )")

    solver.register_ebuild(glibc)
    solver.register_ebuild(openssl)
    solver.register_ebuild(vim_no_ssl)

    # Disable ssl
    profile.set_local_make_conf(["-ssl"])
    plan, errors = solver.resolve("app-editors/vim")
    assert not errors
    atoms = [e.atom for e in plan]
    assert "sys-libs/glibc" in atoms
    assert "dev-libs/openssl" not in atoms

    # Enable ssl
    profile.set_local_make_conf(["ssl"])
    plan_ssl, errors_ssl = solver.resolve("app-editors/vim")
    assert not errors_ssl
    atoms_ssl = [e.atom for e in plan_ssl]
    assert "dev-libs/openssl" in atoms_ssl

def test_virtual_and_slot_resolution():
    profile = ProfileCascade()
    vdb = VarDB()
    solver = PortageDependencySolver(profile, vdb)

    glibc = Ebuild("sys-libs/glibc", "2.38")
    turbojpeg = Ebuild("media-libs/libjpeg-turbo", "2.1", slot="0", virtual_provider_for="virtual/jpeg")
    app = Ebuild("media-gfx/imagemagick", "7.1", raw_depend="sys-libs/glibc virtual/jpeg")

    solver.register_ebuild(glibc)
    solver.register_ebuild(turbojpeg)
    solver.register_ebuild(app)

    plan, errors = solver.resolve("media-gfx/imagemagick")
    assert not errors
    atoms = [e.atom for e in plan]
    assert "media-libs/libjpeg-turbo" in atoms

def test_hard_block_detection():
    profile = ProfileCascade()
    vdb = VarDB()
    solver = PortageDependencySolver(profile, vdb)

    pkg_a = Ebuild("app-misc/foo", "1.0", raw_depend="!app-misc/bar")
    pkg_b = Ebuild("app-misc/bar", "1.0")

    solver.register_ebuild(pkg_a)
    solver.register_ebuild(pkg_b)

    # Register bar in VDB
    vdb.register_installation(pkg_b, set(), ["/usr/bin/bar"])

    plan, errors = solver.resolve("app-misc/foo")
    assert len(errors) > 0
    assert "Hard block collision" in errors[0]

def test_sandbox_violation_and_vdb():
    runner = EbuildSandboxRunner(sandbox_allowed_prefix="/var/tmp/portage")
    ebuild = Ebuild("app-editors/vim", "9.0")

    # Unauthorized path write
    illegal_paths = ["/usr/bin/vim"]
    success, files, logs = runner.execute_lifecycle(ebuild, set(), illegal_paths)
    assert success is False
    assert any("SANDBOX VIOLATION" in line for line in logs)

    # Authorized path write
    valid_paths = ["/var/tmp/portage/app-editors/vim-9.0/image/usr/bin/vim"]
    success_ok, files_ok, logs_ok = runner.execute_lifecycle(ebuild, set(), valid_paths)
    assert success_ok is True
    assert files_ok == ["/usr/bin/vim"]

    vdb = VarDB()
    vdb.register_installation(ebuild, {"ssl"}, files_ok)
    assert vdb.is_installed("app-editors/vim") is True
    assert vdb.get_installed_slots("app-editors/vim") == ["0"]
