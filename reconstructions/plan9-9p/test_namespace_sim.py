#!/usr/bin/env python3
"""
Unit tests for the 9P Distributed Resource Namespace & Message Protocol Simulator.
"""

import pytest
from namespace_sim import (
    FileNode, Namespace, NinePSession,
    T_VERSION, R_VERSION, T_ATTACH, R_ATTACH, T_WALK, R_WALK,
    T_OPEN, R_OPEN, T_READ, R_READ, T_WRITE, R_WRITE,
    T_CREATE, R_CREATE, T_CLUNK, R_CLUNK, R_ERROR
)

def test_file_node_lookup():
    root = FileNode("/", is_dir=True)
    child = FileNode("test.txt", is_dir=False, content="hello")
    root.add_child(child)

    assert root.lookup("test.txt") == child
    assert root.lookup("missing.txt") is None

def test_union_mount_lookup():
    dir_a = FileNode("dir_a", is_dir=True)
    dir_b = FileNode("dir_b", is_dir=True)

    file_a = FileNode("shared.txt", content="content_a")
    file_b = FileNode("shared.txt", content="content_b")
    file_unique = FileNode("unique.txt", content="unique_val")

    dir_a.add_child(file_a)
    dir_b.add_child(file_b)
    dir_b.add_child(file_unique)

    # Union mount: dir_b bound to dir_a (dir_b is searched AFTER dir_a)
    dir_a.union_bindings.append(dir_b)

    # Looking up "shared.txt" should find dir_a's first (shadowing dir_b)
    assert dir_a.lookup("shared.txt") == file_a
    # Looking up "unique.txt" should fallback to dir_b and find it
    assert dir_a.lookup("unique.txt") == file_unique

def test_namespace_resolution_and_bind():
    ns = Namespace()
    # Add sample resource in /bin
    bin_node = ns._resolve_path("/bin")
    assert bin_node is not None
    assert bin_node.is_dir

    ls_tool = FileNode("ls", content="ls_binary_data")
    bin_node.add_child(ls_tool)

    # Verify resolution
    assert ns._resolve_path("/bin/ls") == ls_tool

    # Bind /bin/ls to /dev/ls_cmd
    success = ns.bind("/bin/ls", "/dev/ls_cmd")
    assert success
    resolved = ns._resolve_path("/dev/ls_cmd")
    assert resolved is not None
    assert resolved.content == "ls_binary_data"

def test_namespace_union_bind():
    ns = Namespace()

    # Setup dir1 with tool_a
    ns.root.add_child(FileNode("dir1", is_dir=True))
    dir1 = ns._resolve_path("/dir1")
    dir1.add_child(FileNode("tool_a", content="A"))

    # Setup dir2 with tool_b
    ns.root.add_child(FileNode("dir2", is_dir=True))
    dir2 = ns._resolve_path("/dir2")
    dir2.add_child(FileNode("tool_b", content="B"))

    # Union mount dir2 AFTER dir1 under /bin
    assert ns.bind("/dir1", "/bin", flags="replace")
    assert ns.bind("/dir2", "/bin", flags="union_after")

    # Look up bin children - should resolve both
    bin_dir = ns._resolve_path("/bin")
    assert bin_dir.lookup("tool_a") is not None
    assert bin_dir.lookup("tool_b") is not None

def test_9p_session_flow():
    ns = Namespace()
    session = NinePSession(ns)

    # 1. Negotiate Version (Must be first)
    msg = {"type": T_VERSION, "tag": 1, "version": "9P2000"}
    resp = session.handle_message(msg)
    assert resp["type"] == R_VERSION
    assert resp["version"] == "9P2000"

    # Any non-version call before version should fail (tested by resetting)
    fresh_session = NinePSession(ns)
    err_resp = fresh_session.handle_message({"type": T_ATTACH, "tag": 1, "fid": 1})
    assert err_resp["type"] == R_ERROR

    # 2. Attach to root
    resp = session.handle_message({"type": T_ATTACH, "tag": 2, "fid": 1})
    assert resp["type"] == R_ATTACH

    # 3. Create a file /newfile
    # First walk to root to get a new writable fid, then create
    resp = session.handle_message({"type": T_WALK, "tag": 3, "fid": 1, "newfid": 2, "wnames": []})
    assert resp["type"] == R_WALK

    resp = session.handle_message({"type": T_CREATE, "tag": 4, "fid": 2, "name": "newfile", "is_dir": False})
    assert resp["type"] == R_CREATE

    # Write to /newfile
    resp = session.handle_message({"type": T_WRITE, "tag": 5, "fid": 2, "offset": 0, "data": "hello 9P"})
    assert resp["type"] == R_WRITE
    assert resp["count"] == 8

    # Read from /newfile
    resp = session.handle_message({"type": T_READ, "tag": 6, "fid": 2, "offset": 0, "count": 1024})
    assert resp["type"] == R_READ
    assert resp["data"] == "hello 9P"

    # Clunk fid
    resp = session.handle_message({"type": T_CLUNK, "tag": 7, "fid": 2})
    assert resp["type"] == R_CLUNK
