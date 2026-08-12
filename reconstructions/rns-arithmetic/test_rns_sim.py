import importlib.util
import os
import sys
import pytest

# Since directory name 'rns-arithmetic' has a hyphen, we can load it dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
rns_sim_path = os.path.join(current_dir, "rns_sim.py")

spec = importlib.util.spec_from_file_location("rns_sim", rns_sim_path)
rns_sim = importlib.util.module_from_spec(spec)
sys.modules["rns_sim"] = rns_sim
spec.loader.exec_module(rns_sim)

RNS = rns_sim.RNS

def test_rns_encoding_decoding():
    rns = RNS([3, 5, 7])
    assert rns.M == 105

    # Test positive values (unsigned)
    for x in [0, 1, 10, 52, 104]:
        encoded = rns.encode(x)
        assert len(encoded) == 3
        decoded = rns.decode(encoded, signed=False)
        assert decoded == x

    # Test negative values inside symmetric range (signed)
    for y in [-1, -5, -52]:
        encoded = rns.encode(y)
        decoded = rns.decode(encoded, signed=True)
        assert decoded == y

def test_rns_out_of_bounds():
    rns = RNS([3, 5, 7])
    with pytest.raises(ValueError):
        rns.encode(105) # Exceeds range

def test_rns_arithmetic():
    rns = RNS([3, 5, 7])

    # 12 + 8 = 20
    r12 = rns.encode(12)
    r8 = rns.encode(8)

    r_sum = rns.add(r12, r8)
    assert rns.decode(r_sum, signed=False) == 20

    # 12 - 8 = 4
    r_diff = rns.subtract(r12, r8)
    assert rns.decode(r_diff, signed=False) == 4

    # 12 * 8 = 96
    r_prod = rns.multiply(r12, r8)
    assert rns.decode(r_prod, signed=False) == 96

def test_rns_coprime_check():
    # 3 and 6 are not coprime
    with pytest.raises(ValueError):
        RNS([3, 6])
