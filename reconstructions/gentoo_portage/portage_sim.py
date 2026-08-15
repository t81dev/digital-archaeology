#!/usr/bin/env python3
"""
Portage Engine, USE Flag & Profile Simulator
Reconstructs core Gentoo Portage abstractions:
- Cascading Profile Policy Hierarchy
- USE-Flag Dependency Graph Mutation
- Package Slotting and Virtual Package Resolution
- LD_PRELOAD-style Sandbox Staging and Lifecycle Execution
- Var Database (VDB) Installed Package Tracking
"""

import os
import sys
import re
from typing import Dict, List, Set, Optional, Tuple, Any

class ProfileCascade:
    """Simulates inherited profile directories and cascading configuration defaults."""
    def __init__(self):
        # Cascading layers: [Base, OS, Arch, Subprofile/Desktop]
        self.profile_layers: List[Dict[str, Any]] = [
            # Layer 0: Base profile defaults
            {
                "name": "base",
                "use_defaults": {"unicode", "ssl", "zlib"},
                "masked_packages": set(),
            },
            # Layer 1: OS / Linux defaults
            {
                "name": "default/linux",
                "use_defaults": {"ipc", "posix"},
                "masked_packages": set(),
            },
            # Layer 2: Architecture (amd64) defaults
            {
                "name": "default/linux/amd64",
                "use_defaults": {"amd64", "64bit", "sse2"},
                "masked_packages": set(),
            },
            # Layer 3: Profile target (23.0/desktop) defaults
            {
                "name": "default/linux/amd64/23.0/desktop",
                "use_defaults": {"gui", "alsa", "dbus", "-systemd"},
                "masked_packages": {"sys-apps/systemd-legacy"},
            }
        ]
        self.local_make_conf_use: Set[str] = set()
        self.local_package_use: Dict[str, Set[str]] = {}
        self.local_package_mask: Set[str] = set()

    def set_local_make_conf(self, use_flags: List[str]) -> None:
        """Sets global USE flags in /etc/portage/make.conf."""
        self.local_make_conf_use = set(use_flags)

    def set_local_package_use(self, package_atom: str, use_flags: List[str]) -> None:
        """Sets per-package USE flags in /etc/portage/package.use."""
        self.local_package_use[package_atom] = set(use_flags)

    def mask_package(self, package_atom: str) -> None:
        """Adds a package to /etc/portage/package.mask."""
        self.local_package_mask.add(package_atom)

    def get_effective_global_use(self) -> Set[str]:
        """Cascades through profile layers to evaluate global active USE flags."""
        active_use: Set[str] = set()
        for layer in self.profile_layers:
            for flag in layer["use_defaults"]:
                if flag.startswith("-"):
                    active_use.discard(flag[1:])
                else:
                    active_use.add(flag)

        # Apply local make.conf overrides
        for flag in self.local_make_conf_use:
            if flag.startswith("-"):
                active_use.discard(flag[1:])
            else:
                active_use.add(flag)

        return active_use

    def get_effective_package_use(self, package_atom: str) -> Set[str]:
        """Evaluates final USE flags for a specific package, combining global and package.use overrides."""
        effective = self.get_effective_global_use()
        if package_atom in self.local_package_use:
            for flag in self.local_package_use[package_atom]:
                if flag.startswith("-"):
                    effective.discard(flag[1:])
                else:
                    effective.add(flag)
        return effective

    def is_package_masked(self, package_atom: str) -> bool:
        """Checks if a package is masked by profile layers or local mask configuration."""
        if package_atom in self.local_package_mask:
            return True
        for layer in self.profile_layers:
            if package_atom in layer["masked_packages"]:
                return True
        return False


class USEEvaluator:
    """Evaluates conditional dependency strings against active USE flags."""
    @staticmethod
    def parse_conditional_deps(dep_string: str, active_use: Set[str]) -> List[str]:
        """
        Parses dependencies like:
        'sys-libs/ncurses ssl? ( dev-libs/openssl ) !gui? ( dev-libs/libcli )'
        """
        tokens = dep_string.split()
        resolved_deps: List[str] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if "?" in token:
                condition = token[:-1] # Remove trailing ?
                negated = condition.startswith("!")
                flag = condition[1:] if negated else condition

                # Look for group enclosed in parenthesis
                if i + 1 < len(tokens) and tokens[i+1] == "(":
                    group_deps: List[str] = []
                    i += 2
                    while i < len(tokens) and tokens[i] != ")":
                        group_deps.append(tokens[i])
                        i += 1

                    flag_active = flag in active_use
                    should_include = (not flag_active) if negated else flag_active
                    if should_include:
                        resolved_deps.extend(group_deps)
                else:
                    # Single item after ?
                    if i + 1 < len(tokens):
                        target_dep = tokens[i+1]
                        i += 1
                        flag_active = flag in active_use
                        should_include = (not flag_active) if negated else flag_active
                        if should_include:
                            resolved_deps.append(target_dep)
            else:
                if token not in ("(", ")"):
                    resolved_deps.append(token)
            i += 1
        return resolved_deps


class Ebuild:
    """Represents a Gentoo executable package recipe definition."""
    def __init__(
        self,
        atom: str,
        version: str,
        slot: str = "0",
        iuse: Optional[List[str]] = None,
        raw_depend: str = "",
        raw_rdepend: str = "",
        virtual_provider_for: Optional[str] = None
    ):
        self.atom = atom            # e.g., "app-editors/vim"
        self.version = version      # e.g., "9.0"
        self.slot = slot            # e.g., "0" or "3/3.20"
        self.iuse = set(iuse or []) # Available USE flags
        self.raw_depend = raw_depend
        self.raw_rdepend = raw_rdepend
        self.virtual_provider_for = virtual_provider_for

    @property
    def cpv(self) -> str:
        return f"{self.atom}-{self.version}"


class VarDB:
    """Simulates Portage's Var Database (/var/db/pkg/) installed state tracking."""
    def __init__(self):
        # Installed record map: cpv -> { "atom": str, "version": str, "slot": str, "use": set, "contents": list }
        self.installed: Dict[str, Dict[str, Any]] = {}

    def is_installed(self, atom: str, slot: Optional[str] = None) -> bool:
        """Checks if a package atom (and optional slot) is installed."""
        for cpv, data in self.installed.items():
            if data["atom"] == atom:
                if slot is None or data["slot"] == slot:
                    return True
        return False

    def register_installation(self, ebuild: Ebuild, active_use: Set[str], installed_files: List[str]) -> None:
        """Registers a newly built package into /var/db/pkg/."""
        self.installed[ebuild.cpv] = {
            "atom": ebuild.atom,
            "version": ebuild.version,
            "slot": ebuild.slot,
            "use": set(active_use.intersection(ebuild.iuse)),
            "contents": list(installed_files)
        }

    def get_installed_slots(self, atom: str) -> List[str]:
        """Returns all installed slots for a given package atom."""
        return [data["slot"] for data in self.installed.values() if data["atom"] == atom]


class PortageDependencySolver:
    """Dependency graph resolution engine handling USE flag mutations, slots, virtuals, and blocks."""
    def __init__(self, profile: ProfileCascade, vdb: VarDB):
        self.profile = profile
        self.vdb = vdb
        self.repository: Dict[str, List[Ebuild]] = {}
        self.virtuals: Dict[str, List[str]] = {} # virtual_atom -> list of provider_atoms

    def register_ebuild(self, ebuild: Ebuild) -> None:
        """Registers an ebuild in the package repository."""
        if ebuild.atom not in self.repository:
            self.repository[ebuild.atom] = []
        self.repository[ebuild.atom].append(ebuild)

        if ebuild.virtual_provider_for:
            virt = ebuild.virtual_provider_for
            if virt not in self.virtuals:
                self.virtuals[virt] = []
            if ebuild.atom not in self.virtuals[virt]:
                self.virtuals[virt].append(ebuild.atom)

    def resolve(self, target_atom: str) -> Tuple[List[Ebuild], List[str]]:
        """
        Resolves the full dependency graph for a target package atom.
        Returns (build_order, list_of_conflicts_or_errors)
        """
        if self.profile.is_package_masked(target_atom):
            return [], [f"Package '{target_atom}' is masked by profile or local policy."]

        # Map virtuals if target is a virtual package
        if target_atom.startswith("virtual/"):
            if target_atom in self.virtuals and self.virtuals[target_atom]:
                # Pick first available provider
                target_atom = self.virtuals[target_atom][0]
            else:
                return [], [f"No provider found for virtual package '{target_atom}'."]

        if target_atom not in self.repository or not self.repository[target_atom]:
            return [], [f"Package '{target_atom}' not found in repository."]

        # Select latest ebuild for target atom
        target_ebuild = self.repository[target_atom][-1]

        build_order: List[Ebuild] = []
        visited: Set[str] = set()
        errors: List[str] = []
        blocked_packages: Set[str] = set()

        def visit(ebuild: Ebuild):
            nonlocal errors
            if ebuild.cpv in visited:
                return
            visited.add(ebuild.cpv)

            # Evaluate package USE flags
            active_use = self.profile.get_effective_package_use(ebuild.atom)

            # Parse raw dependencies
            raw_deps = ebuild.raw_depend + " " + ebuild.raw_rdepend
            parsed_deps = USEEvaluator.parse_conditional_deps(raw_deps, active_use)

            for dep_token in parsed_deps:
                # Handle blocks (!package)
                if dep_token.startswith("!"):
                    block_atom = dep_token.lstrip("!")
                    blocked_packages.add(block_atom)
                    if self.vdb.is_installed(block_atom):
                        errors.append(f"Hard block collision: '{ebuild.cpv}' blocks installed package '{block_atom}'.")
                    continue

                # Parse slot constraint if present (e.g. sys-libs/ncurses:0)
                dep_slot = None
                dep_atom = dep_token
                if ":" in dep_token:
                    parts = dep_token.split(":")
                    dep_atom = parts[0]
                    dep_slot = parts[1].rstrip("=")

                # Handle virtual dependency resolution
                if dep_atom.startswith("virtual/"):
                    if dep_atom in self.virtuals and self.virtuals[dep_atom]:
                        dep_atom = self.virtuals[dep_atom][0]
                    else:
                        errors.append(f"Unresolved virtual dependency: '{dep_atom}' for '{ebuild.cpv}'.")
                        continue

                # Resolve sub-dependency
                if dep_atom in self.repository and self.repository[dep_atom]:
                    sub_ebuild = self.repository[dep_atom][-1]
                    if self.profile.is_package_masked(sub_ebuild.atom):
                        errors.append(f"Dependency package '{sub_ebuild.atom}' is masked.")
                        continue
                    visit(sub_ebuild)
                else:
                    errors.append(f"Missing dependency package '{dep_atom}' required by '{ebuild.cpv}'.")

            build_order.append(ebuild)

        visit(target_ebuild)

        # Check if any package in build order conflicts with blocks
        for eb in build_order:
            if eb.atom in blocked_packages:
                errors.append(f"Block conflict: Package '{eb.atom}' in build plan is blocked by another selected package.")

        return build_order, errors


class EbuildSandboxRunner:
    """Simulates ebuild lifecycle execution and LD_PRELOAD filesystem write sandboxing."""
    def __init__(self, sandbox_allowed_prefix: str = "/var/tmp/portage"):
        self.sandbox_allowed_prefix = sandbox_allowed_prefix

    def execute_lifecycle(
        self,
        ebuild: Ebuild,
        active_use: Set[str],
        attempted_writes: List[str]
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Executes ebuild lifecycle phases (src_unpack, src_configure, src_compile, src_install).
        Validates filesystem writes against sandbox boundaries.
        Returns (success, installed_files, log_messages)
        """
        logs: List[str] = []
        installed_files: List[str] = []

        logs.append(f">>> Executing build lifecycle for {ebuild.cpv}")
        logs.append(f"    Active USE flags: {sorted(list(active_use.intersection(ebuild.iuse)))}")

        # Phase 1: src_unpack
        logs.append(f"=== Phase [src_unpack]: Unpacking source archives for {ebuild.cpv}")

        # Phase 2: src_configure
        logs.append(f"=== Phase [src_configure]: Configuring build parameters")

        # Phase 3: src_compile
        logs.append(f"=== Phase [src_compile]: Compiling C/C++ source code")

        # Phase 4: src_install & Sandbox Verification
        logs.append(f"=== Phase [src_install]: Staging files into image directory ($D)")

        sandbox_violation = False
        for path in attempted_writes:
            if not path.startswith(self.sandbox_allowed_prefix):
                logs.append(f"!!! SANDBOX VIOLATION: Unauthorized write attempt to '{path}' outside '{self.sandbox_allowed_prefix}'")
                sandbox_violation = True
            else:
                logs.append(f"    Sandbox OK: Staged '{path}'")
                # Strip prefix to simulate final host path
                final_path = path.replace(f"{self.sandbox_allowed_prefix}/{ebuild.cpv}/image", "")
                installed_files.append(final_path or path)

        if sandbox_violation:
            logs.append(f"ERROR: Build failed for {ebuild.cpv} due to sandbox violations!")
            return False, [], logs

        logs.append(f">>> Successfully staged and installed {ebuild.cpv}")
        return True, installed_files, logs


def run_demo():
    print("=== Gentoo Portage Engine & USE-Flag Reconstruction Demo ===\n")

    # 1. Initialize Profile Cascade & VarDB
    profile = ProfileCascade()
    vdb = VarDB()

    print("1. Profile Defaults:")
    print("   Effective Global USE:", sorted(list(profile.get_effective_global_use())))

    # Customize Profile & local USE flags
    profile.set_local_make_conf(["gui", "ssl", "python", "-alsa"])
    profile.set_local_package_use("app-editors/vim", ["python", "lua"])

    print("\n2. Evaluated Active USE Flags After Local Overrides:")
    print("   Global USE:", sorted(list(profile.get_effective_global_use())))
    print("   Vim USE:", sorted(list(profile.get_effective_package_use("app-editors/vim"))))

    # 2. Populate Repository with Ebuilds
    solver = PortageDependencySolver(profile, vdb)

    # Core C Library
    solver.register_ebuild(Ebuild("sys-libs/glibc", "2.38", slot="2.2"))

    # NCurses TUI Library
    solver.register_ebuild(Ebuild("sys-libs/ncurses", "6.4", slot="0"))

    # Lua Language
    solver.register_ebuild(Ebuild("dev-lang/lua", "5.4.6", slot="5.4"))

    # Python Language
    solver.register_ebuild(Ebuild("dev-lang/python", "3.11.5", slot="3.11"))

    # X11 Window Library
    solver.register_ebuild(Ebuild("x11-libs/libX11", "1.8.7", slot="0"))

    # Vim Editor (with conditional dependencies based on USE flags)
    vim_ebuild = Ebuild(
        atom="app-editors/vim",
        version="9.0.2000",
        slot="0",
        iuse=["python", "lua", "X", "ssl"],
        raw_depend="sys-libs/glibc sys-libs/ncurses:0 python? ( dev-lang/python ) lua? ( dev-lang/lua ) X? ( x11-libs/libX11 )"
    )
    solver.register_ebuild(vim_ebuild)

    print("\n3. Resolving Dependency Graph for 'app-editors/vim':")
    build_plan, errors = solver.resolve("app-editors/vim")

    if errors:
        print("   Resolution Errors:", errors)
    else:
        print("   Resolved Build Sequence:")
        for idx, eb in enumerate(build_plan, 1):
            print(f"     [{idx}] {eb.cpv} (Slot: {eb.slot})")

    # 3. Simulate Lifecycle Execution & LD_PRELOAD Sandbox
    runner = EbuildSandboxRunner(sandbox_allowed_prefix="/var/tmp/portage")
    attempted_paths = [
        "/var/tmp/portage/app-editors/vim-9.0.2000/image/usr/bin/vim",
        "/var/tmp/portage/app-editors/vim-9.0.2000/image/usr/share/man/man1/vim.1"
    ]

    print("\n4. Executing Build Sandbox for 'app-editors/vim':")
    success, installed_files, logs = runner.execute_lifecycle(
        vim_ebuild,
        profile.get_effective_package_use("app-editors/vim"),
        attempted_paths
    )

    for line in logs:
        print("  ", line)

    if success:
        vdb.register_installation(vim_ebuild, profile.get_effective_package_use("app-editors/vim"), installed_files)
        print("\n5. Var Database (VDB) State (/var/db/pkg/):")
        print("   Is vim installed?", vdb.is_installed("app-editors/vim"))
        print("   Installed slots:", vdb.get_installed_slots("app-editors/vim"))

if __name__ == "__main__":
    run_demo()
