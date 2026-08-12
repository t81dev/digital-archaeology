#!/usr/bin/env python3
"""
KeyKOS-style Capability Simulator
Demonstrates unforgeable capability keys, message invocation, least authority sandboxing,
attenuation/minting, and basic persistence checkpointing of a capability graph.
"""

import json

class KeyException(Exception):
    """Raised when an invalid key invocation occurs or authority is violated."""
    pass


class Key:
    """
    Represents an unforgeable Key designating a target object and a set of permission rights.
    """
    def __init__(self, target_id: str, permissions: set, label: str = ""):
        self.target_id = target_id
        # Permissions can be a subset of {'R', 'W', 'C'} (Read, Write, Call)
        self.permissions = permissions
        self.label = label

    def attenuate(self, restricted_permissions: set) -> 'Key':
        """Creates a restricted version of the key with a subset of permissions."""
        if not restricted_permissions.issubset(self.permissions):
            raise KeyException("Attenuated key cannot claim permissions not present in the original key.")
        return Key(self.target_id, restricted_permissions, f"Attenuated {self.label}")

    def __repr__(self):
        perms = "".join(sorted(list(self.permissions)))
        return f"Key(target={self.target_id}, perms={perms}, label='{self.label}')"


class KeykosObject:
    """
    Base class representing an invocable object in the KeyKOS capability network.
    Contains local slots for storing unforgeable keys and raw data.
    """
    def __init__(self, obj_id: str):
        self.obj_id = obj_id
        self.keys = {}  # slot_id -> Key
        self.data = {}  # key -> raw_val

    def invoke(self, key: Key, method: str, *args, **kwargs):
        """Invokes a method on the object, verifying the presenting key's permissions."""
        if 'C' not in key.permissions:
            raise KeyException(f"Presented key lacks Call ('C') permission.")

        handler_name = f"method_{method}"
        if not hasattr(self, handler_name):
            raise KeyException(f"Object {self.obj_id} has no method '{method}'.")

        handler = getattr(self, handler_name)
        return handler(key, *args, **kwargs)


class DirectoryNode(KeykosObject):
    """
    A directory node storing unforgeable keys.
    """
    def method_add_key(self, key: Key, slot: str, new_key: Key):
        if 'W' not in key.permissions:
            raise KeyException("Write permission required to add keys.")
        self.keys[slot] = new_key
        return True

    def method_get_key(self, key: Key, slot: str) -> Key:
        if 'R' not in key.permissions:
            raise KeyException("Read permission required to fetch keys.")
        if slot not in self.keys:
            raise KeyException(f"Key slot '{slot}' empty.")
        return self.keys[slot]


class FileNode(KeykosObject):
    """
    A flat storage node containing raw data records.
    """
    def method_write(self, key: Key, content: str):
        if 'W' not in key.permissions:
            raise KeyException("Write permission required to modify file content.")
        self.data["content"] = content
        return True

    def method_read(self, key: Key) -> str:
        if 'R' not in key.permissions:
            raise KeyException("Read permission required to read file content.")
        return self.data.get("content", "")


class KeykosSystem:
    """
    Coordinates the object registration, routing of invocations, and persistence
    checkpointing of the capability graph.
    """
    def __init__(self):
        self.objects = {}

    def register_object(self, obj: KeykosObject):
        self.objects[obj.obj_id] = obj

    def invoke_key(self, caller_key: Key, method: str, *args, **kwargs):
        """
        Global routing engine: Bypasses ambient authority. Invocations occur
        strictly through the target designated in the presented unforgeable key.
        """
        target_id = caller_key.target_id
        if target_id not in self.objects:
            raise KeyException(f"Key target '{target_id}' does not exist in the system.")
        target_obj = self.objects[target_id]
        return target_obj.invoke(caller_key, method, *args, **kwargs)

    def checkpoint_state(self) -> str:
        """
        Simulates KeyKOS continuous orthogonal persistence.
        Serializes the entire state (object definitions and key slots) to a clean JSON string.
        """
        serialized = {
            "objects": []
        }
        for obj_id, obj in self.objects.items():
            obj_data = {
                "id": obj_id,
                "type": type(obj).__name__,
                "data": obj.data,
                "keys": {
                    slot: {"target": k.target_id, "perms": list(k.permissions), "label": k.label}
                    for slot, k in obj.keys.items()
                }
            }
            serialized["objects"].append(obj_data)
        return json.dumps(serialized, indent=2)

    def restore_state(self, json_str: str):
        """
        Restores capability graph from a serialized checkpoint.
        """
        serialized = json.loads(json_str)
        self.objects.clear()

        for obj_data in serialized["objects"]:
            obj_id = obj_data["id"]
            obj_type = obj_data["type"]

            if obj_type == "FileNode":
                obj = FileNode(obj_id)
            elif obj_type == "DirectoryNode":
                obj = DirectoryNode(obj_id)
            else:
                obj = KeykosObject(obj_id)

            obj.data = obj_data["data"]
            for slot, k_data in obj_data["keys"].items():
                obj.keys[slot] = Key(
                    target_id=k_data["target"],
                    permissions=set(k_data["perms"]),
                    label=k_data["label"]
                )
            self.register_object(obj)


def run_demo():
    print("=== KeyKOS Capability System Simulator Demo ===")
    sys = KeykosSystem()

    # Create nodes
    file1 = FileNode("file_0")
    dir1 = DirectoryNode("dir_0")

    sys.register_object(file1)
    sys.register_object(dir1)

    # Mint a Master Key for file1 with Full R/W/C rights
    file_master = Key("file_0", {'R', 'W', 'C'}, "File Master")

    # Attenuate File Master to Read-Only
    file_ro = file_master.attenuate({'R', 'C'})

    print(f"Master Key: {file_master}")
    print(f"Attenuated (RO) Key: {file_ro}")

    # Try writing using Master Key
    print("\nAction: Writing content using File Master Key...")
    sys.invoke_key(file_master, "write", "Highly Secure Segment Content")

    # Read back using RO Key
    content = sys.invoke_key(file_ro, "read")
    print(f"Read using RO Key: '{content}'")

    # Attempting to write using RO Key
    print("\nAttacker Action: Attempting write using RO Key...")
    try:
        sys.invoke_key(file_ro, "write", "Malicious Injected Content")
    except KeyException as e:
        print(f"  [SUCCESS] System blocked write! Exception: {e}")
    else:
        print("  [FAIL] Security boundary bypassed!")

    # Checkpoint persistence demo
    print("\nAction: Executing Orthogonal Persistence Checkpoint...")
    checkpoint = sys.checkpoint_state()
    print("Checkpoint Saved. Restoring onto fresh instance...")

    sys2 = KeykosSystem()
    sys2.restore_state(checkpoint)
    restored_content = sys2.invoke_key(file_ro, "read")
    print(f"Restored RO read content: '{restored_content}'")


if __name__ == "__main__":
    run_demo()
