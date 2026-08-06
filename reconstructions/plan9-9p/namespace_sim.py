#!/usr/bin/env python3
"""
9P-style Distributed Resource Namespace & Message Protocol Simulator.
Implements Plan 9 / Styx-style message parsing, custom file-like resource binding,
dynamic mount / bind namespace operations, and union directory mounts.
"""

from typing import Dict, List, Tuple, Optional, Any, Union

# 9P Message Type constants
T_VERSION = "Tversion"
R_VERSION = "Rversion"
T_ATTACH  = "Tattach"
R_ATTACH  = "Rattach"
T_WALK    = "Twalk"
R_WALK    = "Rwalk"
T_OPEN    = "Topen"
R_OPEN    = "Ropen"
T_READ    = "Tread"
R_READ    = "Rread"
T_WRITE   = "Twrite"
R_WRITE   = "Rwrite"
T_CREATE  = "Tcreate"
R_CREATE  = "Rcreate"
T_CLUNK   = "Tclunk"
R_CLUNK   = "Rclunk"
R_ERROR   = "Rerror"


class FileNode:
    """
    A representation of a node in a resource tree (file or directory).
    """
    def __init__(self, name: str, is_dir: bool = False, content: str = ""):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children: Dict[str, 'FileNode'] = {}
        # Union mount structures: list of other directories mapped to this directory
        self.union_bindings: List['FileNode'] = []

    def add_child(self, node: 'FileNode'):
        self.children[node.name] = node

    def lookup(self, name: str) -> Optional['FileNode']:
        """
        Looks up a node in this directory, supporting Union mounts.
        Union mounts search this node's children first, then search the union bindings sequentially.
        """
        if name in self.children:
            return self.children[name]
        for union_node in self.union_bindings:
            found = union_node.lookup(name)
            if found:
                return found
        return None

    def clone(self) -> 'FileNode':
        """Deep copy of node and children for isolation."""
        new_node = FileNode(self.name, self.is_dir, self.content)
        for child_name, child_node in self.children.items():
            new_node.add_child(child_node.clone())
        return new_node


class Namespace:
    """
    Manages process-private views of the resource tree.
    Supports bind and union-mount operations.
    """
    def __init__(self):
        # Establish clean-slate root filesystem
        self.root = FileNode("/", is_dir=True)
        # Create standard directory structures
        self.root.add_child(FileNode("dev", is_dir=True))
        self.root.add_child(FileNode("net", is_dir=True))
        self.root.add_child(FileNode("bin", is_dir=True))

    def _resolve_path(self, path: str) -> Optional[FileNode]:
        """Traverses from root to resolve a specific path."""
        parts = [p for p in path.split("/") if p]
        curr = self.root
        for part in parts:
            if not curr.is_dir:
                return None
            next_node = curr.lookup(part)
            if not next_node:
                return None
            curr = next_node
        return curr

    def bind(self, src_path: str, dest_path: str, flags: str = "replace") -> bool:
        """
        Binds source resource path to target resource path.
        Flags:
          - 'replace': Target path is completely replaced by source path.
          - 'union_after': Source directory is appended to target directory search order.
          - 'union_before': Source directory is prepended to target directory search order.
        """
        src_node = self._resolve_path(src_path)
        dest_node = self._resolve_path(dest_path)

        if not src_node:
            return False

        # If dest path doesn't exist, we can only create it if its parent exists
        if not dest_node:
            parent_path = "/" + "/".join([p for p in dest_path.split("/") if p][:-1])
            dest_name = [p for p in dest_path.split("/") if p][-1]
            parent_node = self._resolve_path(parent_path)
            if parent_node and parent_node.is_dir:
                # Create a placeholder and proceed
                dest_node = FileNode(dest_name, is_dir=src_node.is_dir)
                parent_node.add_child(dest_node)
            else:
                return False

        # If it's a simple replace
        if flags == "replace":
            parent_path = "/" + "/".join([p for p in dest_path.split("/") if p][:-1])
            dest_name = [p for p in dest_path.split("/") if p][-1]
            parent_node = self._resolve_path(parent_path)
            if parent_node:
                cloned = src_node.clone()
                cloned.name = dest_name
                parent_node.children[dest_name] = cloned
                return True
            return False

        # If it's a Union Mount, both must be directories
        if not src_node.is_dir or not dest_node.is_dir:
            return False

        if flags == "union_after":
            dest_node.union_bindings.append(src_node)
        elif flags == "union_before":
            dest_node.union_bindings.insert(0, src_node)
        else:
            return False

        return True


class NinePSession:
    """
    A 9P Protocol Server state machine.
    Translates raw structured T-messages into R-messages.
    Maintains user Fids (File Identifiers) mapped to namespace nodes.
    """
    def __init__(self, namespace: Namespace):
        self.namespace = namespace
        self.fids: Dict[int, FileNode] = {}
        self.negotiated_version: Optional[str] = None

    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a single T-message and returns an R-message (or Rerror).
        """
        msg_type = message.get("type")
        tag = message.get("tag", 0)

        # Version negotiation check
        if msg_type != T_VERSION and not self.negotiated_version:
            return {"type": R_ERROR, "tag": tag, "ename": "Protocol version not negotiated"}

        try:
            if msg_type == T_VERSION:
                version = message.get("version", "9P2000")
                self.negotiated_version = version
                return {"type": R_VERSION, "tag": tag, "version": version, "msize": 8192}

            elif msg_type == T_ATTACH:
                fid = message["fid"]
                # For simplicity, attach always mounts the root of namespace
                self.fids[fid] = self.namespace.root
                return {"type": R_ATTACH, "tag": tag, "qid": {"type": "directory", "version": 0, "path": 0}}

            elif msg_type == T_WALK:
                fid = message["fid"]
                newfid = message["newfid"]
                wnames = message.get("wnames", [])

                if fid not in self.fids:
                    return {"type": R_ERROR, "tag": tag, "ename": f"Unknown fid {fid}"}

                curr_node = self.fids[fid]
                qids = []

                for wname in wnames:
                    if not curr_node.is_dir:
                        return {"type": R_ERROR, "tag": tag, "ename": f"Not a directory during walk of {wname}"}
                    next_node = curr_node.lookup(wname)
                    if not next_node:
                        return {"type": R_ERROR, "tag": tag, "ename": f"File not found: {wname}"}
                    curr_node = next_node
                    qid_type = "directory" if curr_node.is_dir else "file"
                    qids.append({"type": qid_type, "version": 0, "path": hash(curr_node.name)})

                # Assign walk endpoint node to newfid
                self.fids[newfid] = curr_node
                return {"type": R_WALK, "tag": tag, "qids": qids}

            elif msg_type == T_OPEN:
                fid = message["fid"]
                mode = message.get("mode", "R") # R, W, RW

                if fid not in self.fids:
                    return {"type": R_ERROR, "tag": tag, "ename": f"Unknown fid {fid}"}

                node = self.fids[fid]
                qid_type = "directory" if node.is_dir else "file"
                return {"type": R_OPEN, "tag": tag, "qid": {"type": qid_type, "version": 0, "path": hash(node.name)}, "iounit": 4096}

            elif msg_type == T_READ:
                fid = message["fid"]
                offset = message.get("offset", 0)
                count = message.get("count", 1024)

                if fid not in self.fids:
                    return {"type": R_ERROR, "tag": tag, "ename": f"Unknown fid {fid}"}

                node = self.fids[fid]
                if node.is_dir:
                    # Return list of filenames inside directory formatted as text
                    # Include standard children and all union bindings
                    all_names = list(node.children.keys())
                    for union in node.union_bindings:
                        all_names.extend(list(union.children.keys()))
                    # Remove duplicates while keeping order
                    unique_names = []
                    for n in all_names:
                        if n not in unique_names:
                            unique_names.append(n)
                    dir_list = "\n".join(unique_names)
                    chunk = dir_list[offset:offset+count]
                    return {"type": R_READ, "tag": tag, "data": chunk, "count": len(chunk)}
                else:
                    chunk = node.content[offset:offset+count]
                    return {"type": R_READ, "tag": tag, "data": chunk, "count": len(chunk)}

            elif msg_type == T_WRITE:
                fid = message["fid"]
                offset = message.get("offset", 0)
                data = message.get("data", "")

                if fid not in self.fids:
                    return {"type": R_ERROR, "tag": tag, "ename": f"Unknown fid {fid}"}

                node = self.fids[fid]
                if node.is_dir:
                    return {"type": R_ERROR, "tag": tag, "ename": "Cannot write to directory"}

                # Exceeding or inserting into content
                content_len = len(node.content)
                if offset > content_len:
                    node.content += " " * (offset - content_len)

                node.content = node.content[:offset] + data + node.content[offset+len(data):]
                return {"type": R_WRITE, "tag": tag, "count": len(data)}

            elif msg_type == T_CREATE:
                fid = message["fid"]
                name = message["name"]
                is_dir = message.get("is_dir", False)

                if fid not in self.fids:
                    return {"type": R_ERROR, "tag": tag, "ename": f"Unknown fid {fid}"}

                dir_node = self.fids[fid]
                if not dir_node.is_dir:
                    return {"type": R_ERROR, "tag": tag, "ename": "Cannot create child under non-directory"}

                # Create the node in the active directory node
                new_node = FileNode(name, is_dir=is_dir)
                dir_node.add_child(new_node)
                # fid now points to the new child
                self.fids[fid] = new_node
                qid_type = "directory" if is_dir else "file"
                return {"type": R_CREATE, "tag": tag, "qid": {"type": qid_type, "version": 0, "path": hash(name)}, "iounit": 4096}

            elif msg_type == T_CLUNK:
                fid = message["fid"]
                if fid in self.fids:
                    del self.fids[fid]
                return {"type": R_CLUNK, "tag": tag}

            else:
                return {"type": R_ERROR, "tag": tag, "ename": f"Unsupported message type: {msg_type}"}

        except Exception as e:
            return {"type": R_ERROR, "tag": tag, "ename": f"Internal Server Error: {str(e)}"}
