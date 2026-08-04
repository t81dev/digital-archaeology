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
