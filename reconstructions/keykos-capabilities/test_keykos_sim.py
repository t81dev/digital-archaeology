import importlib.util
import os
import sys
import pytest

# Dynamic load
current_dir = os.path.dirname(os.path.abspath(__file__))
keykos_sim_path = os.path.join(current_dir, "keykos_sim.py")

spec = importlib.util.spec_from_file_location("keykos_sim", keykos_sim_path)
keykos_sim = importlib.util.module_from_spec(spec)
sys.modules["keykos_sim"] = keykos_sim
spec.loader.exec_module(keykos_sim)

Key = keykos_sim.Key
KeykosSystem = keykos_sim.KeykosSystem
FileNode = keykos_sim.FileNode
DirectoryNode = keykos_sim.DirectoryNode
KeyException = keykos_sim.KeyException

def test_capability_attenuation():
    master_key = Key("file_1", {'R', 'W', 'C'}, "Master")

    # Successful attenuation
    ro_key = master_key.attenuate({'R', 'C'})
    assert 'R' in ro_key.permissions
    assert 'C' in ro_key.permissions
    assert 'W' not in ro_key.permissions

    # Invalid attenuation (adding a permission)
    with pytest.raises(KeyException):
        master_key.attenuate({'R', 'W', 'C', 'X'}) # 'X' not in parent

def test_file_confinement_least_authority():
    sys = KeykosSystem()
    file_obj = FileNode("confined_file")
    sys.register_object(file_obj)

    master_key = Key("confined_file", {'R', 'W', 'C'}, "Master")
    ro_key = Key("confined_file", {'R', 'C'}, "Read Only")
    no_call_key = Key("confined_file", {'R', 'W'}, "No Call")

    # Verify write and read work with Master
    assert sys.invoke_key(master_key, "write", "Secret Token") is True
    assert sys.invoke_key(master_key, "read") == "Secret Token"

    # Verify read works with RO, write fails
    assert sys.invoke_key(ro_key, "read") == "Secret Token"
    with pytest.raises(KeyException):
        sys.invoke_key(ro_key, "write", "Overwrite Attempt")

    # Verify call fails if 'C' permission is missing from key
    with pytest.raises(KeyException):
        sys.invoke_key(no_call_key, "read")

def test_directory_key_slots():
    sys = KeykosSystem()
    dir_obj = DirectoryNode("dir_node")
    sys.register_object(dir_obj)

    dir_master = Key("dir_node", {'R', 'W', 'C'}, "Dir Master")
    target_key = Key("file_99", {'R', 'C'}, "Target Key")

    # Store key in directory slot
    sys.invoke_key(dir_master, "add_key", "slot_a", target_key)

    # Fetch key back
    fetched = sys.invoke_key(dir_master, "get_key", "slot_a")
    assert fetched.target_id == "file_99"
    assert fetched.permissions == {'R', 'C'}

def test_orthogonal_persistence():
    sys = KeykosSystem()
    file_obj = FileNode("f_0")
    sys.register_object(file_obj)

    master_key = Key("f_0", {'R', 'W', 'C'}, "Master")
    sys.invoke_key(master_key, "write", "Persistent State Record")

    # Capture checkpoint
    checkpoint = sys.checkpoint_state()

    # Restore onto a clean system
    sys2 = KeykosSystem()
    sys2.restore_state(checkpoint)

    assert sys2.invoke_key(master_key, "read") == "Persistent State Record"
