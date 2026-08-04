#!/usr/bin/env python3
"""
Interactive Linda Tuple Space Simulator (Generative Communication).
Provides a thread-safe implementation of an associative Tuple Space with blocking
and non-blocking primitives, supporting coordinate-free concurrent programming.
"""

import time
import threading
import logging
from typing import Any, Tuple, List, Optional, Union, Callable

# Set up logging to display thread interactions clearly
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(threadName)s] %(message)s",
    datefmt="%H:%M:%S"
)


class WildcardType:
    """A placeholder for any value of any type in pattern matching."""
    def __repr__(self):
        return "?"


# Global wildcard instance
ANY = WildcardType()


class TupleSpace:
    """
    A thread-safe implementation of David Gelernter's Linda Tuple Space.
    Provides generative communication primitives: out, in, rd, inp, rdp, and eval.
    """
    def __init__(self, name: str = "GlobalSpace"):
        self.name = name
        self.tuples: List[Tuple[Any, ...]] = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        logging.info(f"Initialized Tuple Space: '{self.name}'")

    def out(self, tup: Tuple[Any, ...]) -> None:
        """
        Deposits a passive data tuple into the Tuple Space.
        Triggers notification to any blocked threads waiting on 'in' or 'rd'.
        """
        if not isinstance(tup, tuple):
            raise TypeError("Linda operations require a concrete 'tuple' as input.")

        with self._lock:
            self.tuples.append(tup)
            logging.info(f"OUT -> Deposited: {tup} | Total Tuples: {len(self.tuples)}")
            self._condition.notify_all()

    def _match(self, pattern: Tuple[Any, ...], tup: Tuple[Any, ...]) -> bool:
        """
        Helper to match a tuple against a template pattern.
        A match is successful if:
        1. Arity matches exactly.
        2. Corresponding fields match:
           - If pattern field is a 'type' (formal), the tuple field must be an instance of that type.
           - If pattern field is 'ANY', it matches anything.
           - Otherwise, fields must be exactly equal (actuals).
        """
        if len(pattern) != len(tup):
            return False

        for p_val, t_val in zip(pattern, tup):
            if p_val is ANY:
                continue
            elif isinstance(p_val, type):
                # Formal parameter: check type
                if not isinstance(t_val, p_val):
                    return False
            else:
                # Actual parameter: check exact value equivalence
                if p_val != t_val:
                    return False
        return True

    def _find_match(self, pattern: Tuple[Any, ...], remove: bool) -> Optional[Tuple[Any, ...]]:
        """
        Internal scan of the tuple pool for a matching pattern.
        If remove is True, the tuple is withdrawn from the pool (implements 'in' vs 'rd').
        Must be called with self._lock acquired.
        """
        for i, tup in enumerate(self.tuples):
            if self._match(pattern, tup):
                matched_tuple = self.tuples.pop(i) if remove else tup
                return matched_tuple
        return None

    def in_(self, pattern: Tuple[Any, ...], timeout: Optional[float] = None) -> Tuple[Any, ...]:
        """
        Associatively searches the Tuple Space for a tuple matching 'pattern',
        withdraws it from the space, and returns it.
        Blocks the calling thread if no match exists, waiting for future 'out' operations.

        Note: Method is named 'in_' to avoid conflict with Python's 'in' keyword.
        """
        if not isinstance(pattern, tuple):
            raise TypeError("Linda template pattern must be a tuple.")

        start_time = time.time()
        with self._lock:
            while True:
                matched = self._find_match(pattern, remove=True)
                if matched is not None:
                    logging.info(f"IN  <- Consumed:  {matched} (matched pattern: {pattern})")
                    return matched

                # Check if we timed out
                if timeout is not None:
                    elapsed = time.time() - start_time
                    remaining = timeout - elapsed
                    if remaining <= 0:
                        raise TimeoutError(f"Operation in({pattern}) timed out.")
                    self._condition.wait(remaining)
                else:
                    self._condition.wait()

    def rd(self, pattern: Tuple[Any, ...], timeout: Optional[float] = None) -> Tuple[Any, ...]:
        """
        Associatively searches the Tuple Space for a tuple matching 'pattern',
        and returns a copy of it, leaving the original in the space.
        Blocks the calling thread if no match exists.
        """
        if not isinstance(pattern, tuple):
            raise TypeError("Linda template pattern must be a tuple.")

        start_time = time.time()
        with self._lock:
            while True:
                matched = self._find_match(pattern, remove=False)
                if matched is not None:
                    logging.info(f"RD  <- Read Copy: {matched} (matched pattern: {pattern})")
                    return matched

                if timeout is not None:
                    elapsed = time.time() - start_time
                    remaining = timeout - elapsed
                    if remaining <= 0:
                        raise TimeoutError(f"Operation rd({pattern}) timed out.")
                    self._condition.wait(remaining)
                else:
                    self._condition.wait()

    def inp(self, pattern: Tuple[Any, ...]) -> Optional[Tuple[Any, ...]]:
        """
        Non-blocking version of 'in'.
        Immediately returns a matching tuple if present (withdrawing it),
        or returns None if no match is found.
        """
        if not isinstance(pattern, tuple):
            raise TypeError("Linda template pattern must be a tuple.")

        with self._lock:
            matched = self._find_match(pattern, remove=True)
            if matched is not None:
                logging.info(f"INP <- Consumed (Immediate): {matched} (pattern: {pattern})")
            else:
                logging.info(f"INP <- Match Failed (Immediate): {pattern}")
            return matched

    def rdp(self, pattern: Tuple[Any, ...]) -> Optional[Tuple[Any, ...]]:
        """
        Non-blocking version of 'rd'.
        Immediately returns a copy of a matching tuple if present,
        or returns None if no match is found.
        """
        if not isinstance(pattern, tuple):
            raise TypeError("Linda template pattern must be a tuple.")

        with self._lock:
            matched = self._find_match(pattern, remove=False)
            if matched is not None:
                logging.info(f"RDP <- Read Copy (Immediate): {matched} (pattern: {pattern})")
            else:
                logging.info(f"RDP <- Match Failed (Immediate): {pattern}")
            return matched

    def eval(self, func: Callable[..., Any], *args: Any) -> None:
        """
        Spawns an active process tuple.
        Executes 'func(*args)' concurrently inside a separate thread.
        Upon completion, the function's return value is automatically deposited
        as a passive data tuple ('result', function_name, output) in the Tuple Space.
        """
        def process_wrapper():
            thread_name = f"eval-{func.__name__}"
            threading.current_thread().name = thread_name
            logging.info(f"EVAL -> Active Process Started")
            try:
                result = func(*args)
                # Formulate return tuple.
                # If return value is a tuple, we serialize it directly, otherwise wrap it.
                if isinstance(result, tuple):
                    out_tuple = ("result", func.__name__) + result
                else:
                    out_tuple = ("result", func.__name__, result)
                self.out(out_tuple)
            except Exception as e:
                logging.error(f"EVAL -> Process Failed: {e}")
                self.out(("error", func.__name__, str(e)))

        thread = threading.Thread(target=process_wrapper)
        thread.start()


# --- CLI Demonstration ---

def worker_node(space: TupleSpace, worker_id: int):
    """
    A coordinate-free worker pool.
    Consumes task tuples, processes them, and outputs result tuples.
    Does not know where the tasks came from or which master created them.
    """
    threading.current_thread().name = f"Worker-{worker_id}"
    logging.info("Worker spawned, polling for tasks...")

    while True:
        try:
            # Block until a task is available: matching pattern ("task", int, list)
            task = space.in_(("task", int, list))
            task_id = task[1]
            numbers = task[2]

            logging.info(f"Processing task {task_id}: {numbers}")
            # Simulate some heavy compute (e.g., sum of squares)
            sum_of_squares = sum(x*x for x in numbers)
            time.sleep(0.5) # Simulate physical latency

            # Post result back anonymously
            space.out(("result", task_id, sum_of_squares, worker_id))
        except Exception as e:
            logging.error(f"Worker encountered error: {e}")
            break


def run_demo():
    print("\n" + "="*60)
    print("           LINDA TUPLE SPACE SIMULATOR SHOWCASE")
    print("         Coordinate-free Parallel Master-Worker Pool")
    print("="*60 + "\n")

    # Initialize our central associative medium
    space = TupleSpace("DemoSpace")

    # Spawn 3 concurrent worker nodes
    workers = []
    for i in range(1, 4):
        t = threading.Thread(target=worker_node, args=(space, i), daemon=True)
        t.start()
        workers.append(t)

    time.sleep(0.2) # Allow threads to boot

    print("\n--- MASTER Phase 1: Depositing Tasks Anonymously ---")
    # Master outputs 5 computational tasks
    tasks = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
        [13, 14, 15]
    ]

    for idx, num_list in enumerate(tasks):
        # Tuple schema: ("task", task_id, data_list)
        space.out(("task", idx, num_list))

    print("\n--- MASTER Phase 2: Processing Active Process via EVAL ---")
    # Demonstrate EVAL active process
    def async_factorial(n: int) -> int:
        val = 1
        for i in range(2, n + 1):
            val *= i
        time.sleep(0.8) # Simulate processing
        return val

    space.eval(async_factorial, 5)

    print("\n--- MASTER Phase 3: Block-waiting and Gathering Results ---")
    # Master reads all 5 task results
    results_gathered = 0
    while results_gathered < len(tasks):
        # Block until a result tuple matches: ("result", int, int, int)
        # where fields represent: ("result", task_id, calculation_result, worker_id)
        res = space.in_(("result", int, int, int))
        task_id = res[1]
        calc_val = res[2]
        worker_id = res[3]
        print(f"Master GATHER -> Task {task_id} completed by Worker-{worker_id}: Result = {calc_val}")
        results_gathered += 1

    # Read the eval active process result
    eval_res = space.in_(("result", "async_factorial", int))
    print(f"Master GATHER -> Async eval process 'async_factorial' completed: Result = {eval_res[2]}\n")

    print("="*60)
    print("   DEMONSTRATION SUCCESSFUL: SPATIAL & TEMPORAL DECOUPLING")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_demo()
