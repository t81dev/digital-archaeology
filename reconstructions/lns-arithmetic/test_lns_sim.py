import importlib.util
import os
import sys
import pytest

# Dynamic load
current_dir = os.path.dirname(os.path.abspath(__file__))
lns_sim_path = os.path.join(current_dir, "lns_sim.py")

spec = importlib.util.spec_from_file_location("lns_sim", lns_sim_path)
lns_sim = importlib.util.module_from_spec(spec)
sys.modules["lns_sim"] = lns_sim
spec.loader.exec_module(lns_sim)

LNS = lns_sim.LNS

def test_lns_encode_decode():
    lns = LNS(base=2.0)

    # Simple values
    for val in [1.0, 2.0, 4.0, 0.5, 0.25]:
        lns_val = lns.encode(val)
        assert lns_val[0] == 1
        assert lns.decode(lns_val) == pytest.approx(val)

    for val in [-1.0, -4.0, -0.5]:
        lns_val = lns.encode(val)
        assert lns_val[0] == -1
        assert lns.decode(lns_val) == pytest.approx(val)

    # Zero
    assert lns.decode(lns.encode(0.0)) == 0.0

def test_lns_multiply_divide():
    lns = LNS(base=2.0)

    x = lns.encode(5.5)
    y = lns.encode(2.0)

    prod = lns.multiply(x, y)
    assert lns.decode(prod) == pytest.approx(11.0)

    div = lns.divide(x, y)
    assert lns.decode(div) == pytest.approx(2.75)

def test_lns_addition_subtraction():
    lns = LNS(base=2.0, table_size=200) # larger table = more precise

    # Addition
    x = lns.encode(14.0)
    y = lns.encode(6.0)

    l_sum = lns.add(x, y)
    assert lns.decode(l_sum) == pytest.approx(20.0, rel=0.01) # allow minor interpolation error

    # Subtraction
    l_diff = lns.subtract(x, y)
    assert lns.decode(l_diff) == pytest.approx(8.0, rel=0.01)

    # Signs mixed
    ny = lns.encode(-6.0)
    l_sum_mixed = lns.add(x, ny)
    assert lns.decode(l_sum_mixed) == pytest.approx(8.0, rel=0.01)
