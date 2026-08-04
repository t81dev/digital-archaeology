#!/usr/bin/env python3
"""
Unit tests for the Linda Tuple Space Simulator.
Verifies associative matching, non-blocking operations, thread safety,
timeout semantics, and concurrent process execution via eval.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import pytest
import threading
from tuple_space_sim import TupleSpace, ANY


def test_basic_out_in():
    """Verify that we can output a tuple and retrieve it by exact value matching."""
    space = TupleSpace("TestSpace")
    space.out(("sensor", 42, "normal"))

    # Exact match
    matched = space.in_(("sensor", 42, "normal"))
    assert matched == ("sensor", 42, "normal")
    assert len(space.tuples) == 0


def test_type_formal_matching():
    """Verify that type formals (?type) correctly match and bind."""
    space = TupleSpace("TestSpace")
    space.out(("log", 101, "server_reboot", 3.14))

    # Match with formals
    matched = space.in_(("log", int, str, float))
    assert matched == ("log", 101, "server_reboot", 3.14)
    assert len(space.tuples) == 0


def test_type_mismatch():
    """Verify that matching fails and times out if there is a type mismatch."""
    space = TupleSpace("TestSpace")
    space.out(("log", "not_an_int", "msg"))

    # Try to read with a pattern expecting an int
    with pytest.raises(TimeoutError):
        space.rd(("log", int, str), timeout=0.1)


def test_wildcard_matching():
    """Verify that the ANY wildcard matches any value of any type."""
    space = TupleSpace("TestSpace")
    space.out(("metric", "cpu_usage", 94.5))
    space.out(("metric", "disk_usage", "low"))

    # ANY should match 94.5 and 'low'
    res1 = space.in_(("metric", "cpu_usage", ANY))
    res2 = space.in_(("metric", "disk_usage", ANY))

    assert res1 == ("metric", "cpu_usage", 94.5)
    assert res2 == ("metric", "disk_usage", "low")


def test_rd_leaves_tuple_in_space():
    """Verify that rd retrieves a copy of the tuple without removing it."""
    space = TupleSpace("TestSpace")
    space.out(("config", "port", 8080))

    matched1 = space.rd(("config", "port", int))
    matched2 = space.rd(("config", "port", int))

    assert matched1 == ("config", "port", 8080)
    assert matched2 == ("config", "port", 8080)
    assert len(space.tuples) == 1


def test_non_blocking_inp_rdp():
    """Verify non-blocking primitives return immediately with matched tuple or None."""
    space = TupleSpace("TestSpace")

    # Non-blocking read on empty space
    assert space.rdp(("status", str)) is None
    assert space.inp(("status", str)) is None

    # Deposit and test
    space.out(("status", "healthy"))
    assert space.rdp(("status", str)) == ("status", "healthy")
    assert space.inp(("status", str)) == ("status", "healthy")
    assert len(space.tuples) == 0


def test_multithreaded_blocking_and_notify():
    """Verify that a thread blocking on in_ is correctly notified and returns when tuple is deposited."""
    space = TupleSpace("TestSpace")
    shared_bag = []

    def consumer():
        # This will block until the producer outputs a matching tuple
        tup = space.in_(("job", int))
        shared_bag.append(tup)

    thread = threading.Thread(target=consumer)
    thread.start()

    # Allow consumer to enter blocking state
    time.sleep(0.1)
    assert len(shared_bag) == 0

    # Deposit non-matching tuple first
    space.out(("job", "not_an_int"))
    time.sleep(0.1)
    assert len(shared_bag) == 0

    # Deposit matching tuple
    space.out(("job", 12345))
    thread.join(timeout=1.0)

    assert len(shared_bag) == 1
    assert shared_bag[0] == ("job", 12345)


def test_eval_active_process():
    """Verify active evaluation of processes concurrently into passive tuples."""
    space = TupleSpace("TestSpace")

    def worker_computation(x, y):
        time.sleep(0.1)
        return x + y

    space.eval(worker_computation, 10, 20)

    # Should block and retrieve result when finished
    res = space.in_(("result", "worker_computation", int), timeout=1.0)
    assert res == ("result", "worker_computation", 30)
