"""
Unit tests for the high-fidelity MapReduce Simulator.
"""

from reconstructions.mapreduce.mapreduce_sim import (
    MapReduceEngine,
    SimpleWordCountMapper,
    SimpleWordCountReducer,
)


def test_standard_mapreduce_word_count():
    """Tests basic MapReduce execution without failures."""
    engine = MapReduceEngine(num_reducers=2)
    engine.add_worker("Worker_A")
    engine.add_worker("Worker_B")

    inputs = [
        (0, "the quick brown fox"),
        (1, "jumps over the lazy dog"),
        (2, "the quick lazy dog"),
    ]

    outputs = engine.execute(
        inputs,
        SimpleWordCountMapper(),
        SimpleWordCountReducer(),
    )

    assert outputs["the"] == 3
    assert outputs["quick"] == 2
    assert outputs["lazy"] == 2
    assert outputs["fox"] == 1
    assert outputs["dog"] == 2


def test_partitioner_behavior():
    """Asserts that keys are partitioned deterministically."""
    engine = MapReduceEngine(num_reducers=4)
    p0 = engine.partition_key("hello")
    p1 = engine.partition_key("world")
    p2 = engine.partition_key("hello")

    assert p0 == p2  # Same key must map to the same partition
    assert 0 <= p0 < 4
    assert 0 <= p1 < 4


def test_fault_recovery_during_map():
    """
    Tests fault tolerance: injecting a worker crash during the Map phase
    and verifying the scheduler successfully recovers and finishes deterministically.
    """
    engine = MapReduceEngine(num_reducers=2)
    engine.add_worker("Worker_X")
    engine.add_worker("Worker_Y")

    inputs = [
        (0, "alpha beta gamma"),
        (1, "delta epsilon"),
        (2, "alpha delta"),
    ]

    # Inject crash: when chunk 0 is allocated to Worker_X, Worker_X crashes
    # Worker_Y should pick up chunk 0 and finish the work
    outputs = engine.execute(
        inputs,
        SimpleWordCountMapper(),
        SimpleWordCountReducer(),
        fail_during_map=[(0, "Worker_X")],
    )

    # Worker_X should be crashed/unhealthy
    assert not engine.workers["Worker_X"].is_healthy
    assert engine.workers["Worker_Y"].is_healthy

    # The final outputs must be correct and complete
    assert outputs["alpha"] == 2
    assert outputs["beta"] == 1
    assert outputs["gamma"] == 1
    assert outputs["delta"] == 2
    assert outputs["epsilon"] == 1
