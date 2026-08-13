"""
High-Fidelity MapReduce Distributed Execution and Fault-Tolerance Simulator.
Demonstrates functional data partitioning, shuffling, and fault-tolerant retry contracts.
"""

import hashlib
from typing import Any, Callable, Dict, List, Tuple


class Mapper:
    """Base Mapper class. User subclasses this and overrides `map`."""
    def map(self, key: Any, value: Any, emit_fn: Callable[[Any, Any], None]) -> None:
        raise NotImplementedError


class Reducer:
    """Base Reducer class. User subclasses this and overrides `reduce`."""
    def reduce(self, key: Any, values: List[Any], emit_fn: Callable[[Any, Any], None]) -> None:
        raise NotImplementedError


class SimpleWordCountMapper(Mapper):
    """A standard WordCount Mapper implementation."""
    def map(self, key: Any, value: str, emit_fn: Callable[[Any, Any], None]) -> None:
        # Simple word isolation
        for word in value.split():
            clean_word = "".join(c.lower() for c in word if c.isalnum())
            if clean_word:
                emit_fn(clean_word, 1)


class SimpleWordCountReducer(Reducer):
    """A standard WordCount Reducer implementation."""
    def reduce(self, key: str, values: List[int], emit_fn: Callable[[Any, Any], None]) -> None:
        emit_fn(key, sum(values))


class WorkerNode:
    """Simulates a commodity hardware worker node in a MapReduce cluster."""
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.is_healthy = True
        self.local_storage: Dict[int, List[Tuple[Any, Any]]] = {}  # partition -> list(key, value)

    def crash(self) -> None:
        """Crashes the worker, losing all local state."""
        self.is_healthy = False
        self.local_storage.clear()

    def recover(self) -> None:
        """Recovers the worker, making it healthy again."""
        self.is_healthy = True


class MapReduceEngine:
    """
    Coordinates MapReduce task scheduling, data partitioning,
    intermediate shuffling, and fault-tolerant recovery.
    """
    def __init__(self, num_reducers: int = 2):
        self.num_reducers = num_reducers
        self.workers: Dict[str, WorkerNode] = {}
        self.logs: List[str] = []

    def log(self, message: str) -> None:
        self.logs.append(message)
        print(f"[MapReduceEngine] {message}")

    def add_worker(self, worker_id: str) -> None:
        self.workers[worker_id] = WorkerNode(worker_id)
        self.log(f"Registered Worker Node: {worker_id}")

    def partition_key(self, key: Any) -> int:
        """Determines the target reducer partition based on key hash."""
        # Standard hash partitioner
        sha = hashlib.sha256(str(key).encode("utf-8")).hexdigest()
        return int(sha, 16) % self.num_reducers

    def execute(
        self,
        input_chunks: List[Tuple[Any, Any]],
        mapper: Mapper,
        reducer: Reducer,
        fail_during_map: List[Tuple[int, str]] = None,  # List of (chunk_index, worker_id) to trigger crash
    ) -> Dict[Any, Any]:
        """
        Executes a full MapReduce loop across simulated workers.
        Handles dynamic partitioning, shuffling, sorting, and fault recovery.
        """
        self.log(f"Starting execution loop. Inputs: {len(input_chunks)} chunks, Reducers: {self.num_reducers}")

        # Track active workers
        active_workers = [w_id for w_id, w in self.workers.items() if w.is_healthy]
        if not active_workers:
            raise ValueError("No healthy workers registered in cluster!")

        # ----------------------------------------------------
        # 1. Map Phase with Scheduler and Fault Tolerance
        # ----------------------------------------------------
        # Mapping input chunk index to status: "PENDING", "COMPLETED"
        chunk_status = {i: "PENDING" for i in range(len(input_chunks))}
        chunk_worker_mapping: Dict[int, str] = {}

        # Simulating scheduler dispatch queue
        round_robin_idx = 0

        while "PENDING" in chunk_status.values():
            for chunk_idx, status in list(chunk_status.items()):
                if status != "PENDING":
                    continue

                # Locate a healthy worker
                healthy_workers = [w_id for w_id, w in self.workers.items() if w.is_healthy]
                if not healthy_workers:
                    raise RuntimeError("System Panic: All cluster workers crashed during Map phase!")

                worker_id = healthy_workers[round_robin_idx % len(healthy_workers)]
                round_robin_idx += 1

                self.log(f"Assigning Chunk {chunk_idx} to Worker {worker_id}")
                chunk_worker_mapping[chunk_idx] = worker_id
                worker = self.workers[worker_id]

                # Check if a crash is injected for this chunk assignment
                if fail_during_map and (chunk_idx, worker_id) in fail_during_map:
                    self.log(f"!!! CRASH INJECTED: Worker {worker_id} crashed during processing of Chunk {chunk_idx} !!!")
                    worker.crash()
                    # Mark chunk as pending still so another worker will pick it up
                    continue

                # Execute Map task
                key, val = input_chunks[chunk_idx]
                intermediate_emitted: List[Tuple[Any, Any]] = []

                def emit(k: Any, v: Any) -> None:
                    intermediate_emitted.append((k, v))

                try:
                    mapper.map(key, val, emit)

                    # Partition and store intermediate data locally on the worker
                    for k, v in intermediate_emitted:
                        part = self.partition_key(k)
                        if part not in worker.local_storage:
                            worker.local_storage[part] = []
                        worker.local_storage[part].append((k, v))

                    chunk_status[chunk_idx] = "COMPLETED"
                    self.log(f"Worker {worker_id} successfully completed Chunk {chunk_idx}")
                except Exception as e:
                    self.log(f"Worker {worker_id} failed processing Chunk {chunk_idx}: {str(e)}")
                    worker.crash()

        # ----------------------------------------------------
        # 2. Shuffle & Partition Phase
        # ----------------------------------------------------
        self.log("Map phase complete. Initiating Shuffle and Partition phase.")
        # Shuffle pulls intermediate partitions from local worker disks to reducer buckets
        reducer_inputs: Dict[int, Dict[Any, List[Any]]] = {i: {} for i in range(self.num_reducers)}

        for worker_id, worker in self.workers.items():
            if not worker.is_healthy:
                continue
            for partition, pairs in worker.local_storage.items():
                for k, v in pairs:
                    if k not in reducer_inputs[partition]:
                        reducer_inputs[partition][k] = []
                    reducer_inputs[partition][k].append(v)

        # ----------------------------------------------------
        # 3. Reduce Phase
        # ----------------------------------------------------
        self.log("Shuffle complete. Initiating Reduce phase.")
        final_outputs: Dict[Any, Any] = {}

        for partition in range(self.num_reducers):
            self.log(f"Reducing Partition {partition}")
            partition_data = reducer_inputs[partition]

            # Sort intermediate keys in partition to mimic production sorting
            sorted_keys = sorted(partition_data.keys())

            for key in sorted_keys:
                values = partition_data[key]
                reduced_emitted: List[Any] = []

                def emit_reduce(k: Any, v: Any) -> None:
                    reduced_emitted.append(v)

                reducer.reduce(key, values, emit_reduce)

                # Assume one output per key for simplicity
                if reduced_emitted:
                    final_outputs[key] = reduced_emitted[0]

        self.log(f"Execution loop complete. Emitted {len(final_outputs)} unique keys.")
        return final_outputs
