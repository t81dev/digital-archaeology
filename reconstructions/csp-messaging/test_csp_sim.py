import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from csp_sim import Channel, CSPScheduler, producer_proc, consumer_proc, deadlocked_p1_proc, deadlocked_p2_proc

def test_producer_consumer():
    scheduler = CSPScheduler(verbose=False)
    c = Channel("DataStream")
    scheduler.register("Producer", producer_proc, c, [10, 20])
    scheduler.register("Consumer", consumer_proc, c, 2)
    success = scheduler.run()
    assert success is True

def test_deadlock_detection():
    scheduler = CSPScheduler(verbose=False)
    c1 = Channel("Chan1")
    c2 = Channel("Chan2")
    scheduler.register("P1", deadlocked_p1_proc, c1, c2)
    scheduler.register("P2", deadlocked_p2_proc, c1, c2)
    success = scheduler.run()
    assert success is False

def test_deadlock_recovery_preemption():
    """Verify that deadlock recovery with 'preemption' policy unblocks the scheduler."""
    scheduler = CSPScheduler(verbose=False, deadlock_policy="preemption")
    c1 = Channel("Chan1")
    c2 = Channel("Chan2")
    scheduler.register("P1", deadlocked_p1_proc, c1, c2)
    scheduler.register("P2", deadlocked_p2_proc, c1, c2)
    success = scheduler.run()
    # Preemption unblocks them, they continue and stop naturally or terminated
    assert success is True

def test_deadlock_recovery_rollback():
    """Verify that deadlock recovery with 'rollback' policy unblocks the scheduler."""
    scheduler = CSPScheduler(verbose=False, deadlock_policy="rollback")
    c1 = Channel("Chan1")
    c2 = Channel("Chan2")
    scheduler.register("P1", deadlocked_p1_proc, c1, c2)
    scheduler.register("P2", deadlocked_p2_proc, c1, c2)
    success = scheduler.run()
    assert success is True
