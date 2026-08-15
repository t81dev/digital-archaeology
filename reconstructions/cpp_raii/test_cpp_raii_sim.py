"""
Unit tests for C++ RAII, Exception Unwinding, and Zero-Overhead Dispatch Simulator
"""

import pytest
from reconstructions.cpp_raii.cpp_raii_sim import (
    ScopeStack,
    Resource,
    DispatchProfiler,
    GenericIteratorContract,
    run_raii_demo,
)


def test_raii_normal_scope_exit():
    """Tests that normal scope exit destroys objects in exact reverse construction order."""
    stack = ScopeStack()
    stack.enter_scope("main")
    r1 = stack.allocate("buf1", "unique_ptr")
    r2 = stack.allocate("buf2", "unique_ptr")
    r3 = stack.allocate("buf3", "unique_ptr")

    assert not r1.released
    assert not r2.released
    assert not r3.released

    logs = stack.exit_scope()

    # Destructors must execute in reverse order: buf3, buf2, buf1
    assert "buf3" in logs[0]
    assert "buf2" in logs[1]
    assert "buf1" in logs[2]

    assert r1.released
    assert r2.released
    assert r3.released


def test_raii_exception_unwinding():
    """Tests stack unwinding through nested scopes until catch handler is met."""
    stack = ScopeStack()

    # Outer scope has catch handler
    stack.enter_scope("outer_frame", catch_types=["std::out_of_range"])
    r_outer = stack.allocate("outer_resource", "shared_ptr")

    # Middle scope without catch handler
    stack.enter_scope("middle_frame")
    r_mid = stack.allocate("mid_resource", "lock_guard")

    # Inner scope where exception originates
    stack.enter_scope("inner_frame")
    r_inner = stack.allocate("inner_resource", "ifstream")

    # Throw exception
    report = stack.throw_exception("std::out_of_range", "Index 10 out of vector bounds")

    assert report["caught"] is True
    assert report["handler_scope"] == "outer_frame"
    assert "inner_frame" in report["unwound_scopes"]
    assert "middle_frame" in report["unwound_scopes"]
    assert "outer_frame" in report["unwound_scopes"]

    # All resources created in inner, middle, and outer frames must be released during unwind
    assert r_inner.released is True
    assert r_mid.released is True
    assert r_outer.released is True


def test_dispatch_profiler_comparison():
    """Tests performance metric calculations for static vs dynamic dispatch."""
    static_perf = DispatchProfiler.profile_static_dispatch(1000)
    dynamic_perf = DispatchProfiler.profile_dynamic_vtable_dispatch(1000, btb_miss_rate=0.10)

    assert static_perf["vptr_lookups"] == 0
    assert static_perf["indirect_branches"] == 0
    assert static_perf["estimated_cycles"] == 1000

    assert dynamic_perf["vptr_lookups"] == 1000
    assert dynamic_perf["indirect_branches"] == 1000
    assert dynamic_perf["btb_misses"] == 100
    # 1000 * 4 base cycles + 100 * 12 miss penalty cycles = 5200 cycles
    assert dynamic_perf["estimated_cycles"] == 5200
    assert dynamic_perf["overhead_tax_percent"] > 0.0


def test_generic_iterator_contract():
    """Tests container-algorithm accumulation via iterator abstraction."""
    data = [10, 20, 30, 40, 50]
    contract = GenericIteratorContract(data)
    result, ops = contract.accumulate_via_iterator(init_value=0)

    assert result == 150
    assert ops == 5


def test_raii_demo_execution():
    """Tests that the full demo runs cleanly and produces correct logs."""
    demo = run_raii_demo()
    assert "unwind_report" in demo
    assert demo["unwind_report"]["caught"] is True
    assert len(demo["total_released_resources"]) == 4
    assert "temp_matrix" in demo["total_released_resources"]
    assert "mutex_lock" in demo["total_released_resources"]
    assert "file_handle" in demo["total_released_resources"]
    assert "heap_buffer" in demo["total_released_resources"]
