"""
C++ RAII, Exception Unwinding, and Zero-Overhead Dispatch Simulator
====================================================================

This zero-dependency simulator models the core computational abstractions of C++:
1. Deterministic Scope-Bound Resource Acquisition Is Initialization (RAII).
2. Stack unwinding and guaranteed reverse-order destructor execution during exception paths.
3. Static monomorphized template dispatch vs. dynamic vtable indirect dispatch performance metrics.
4. Container-algorithm decoupling via generic iterator contracts.
"""

from typing import List, Dict, Any, Optional, Tuple, Callable


class Resource:
    """Represents a system resource managed via RAII (memory, file handle, mutex lock)."""

    def __init__(self, name: str, resource_type: str, details: Optional[Dict[str, Any]] = None):
        self.name = name
        self.resource_type = resource_type
        self.details = details or {}
        self.acquired = True
        self.released = False
        self.release_log: List[str] = []

    def release(self) -> str:
        """Invoked by the RAII object's destructor to release the underlying resource."""
        if not self.acquired or self.released:
            return f"Resource {self.name} already released"
        self.released = True
        self.acquired = False
        msg = f"Destructor executed for [{self.resource_type}:{self.name}] - Resource released"
        self.release_log.append(msg)
        return msg


class ScopeFrame:
    """Represents a single block or function scope frame containing RAII objects."""

    def __init__(self, scope_name: str, catch_types: Optional[List[str]] = None):
        self.scope_name = scope_name
        self.resources: List[Resource] = []
        self.catch_types = catch_types or []

    def register_resource(self, resource: Resource) -> None:
        """Registers an RAII resource in construction order."""
        self.resources.append(resource)

    def unwind(self) -> List[str]:
        """Destroys resources in exact reverse order of construction."""
        logs = []
        for res in reversed(self.resources):
            logs.append(res.release())
        return logs


class ScopeStack:
    """Simulates the C++ call stack and RAII lifetime unwinding engine."""

    def __init__(self):
        self.frames: List[ScopeFrame] = []
        self.execution_log: List[str] = []
        self.released_resources: List[Resource] = []

    def enter_scope(self, scope_name: str, catch_types: Optional[List[str]] = None) -> ScopeFrame:
        """Pushes a new scope frame onto the execution stack."""
        frame = ScopeFrame(scope_name, catch_types)
        self.frames.append(frame)
        self.execution_log.append(f"Entered scope: {scope_name}")
        return frame

    def allocate(self, name: str, resource_type: str, details: Optional[Dict[str, Any]] = None) -> Resource:
        """Constructs an RAII object bound to the current innermost scope frame."""
        if not self.frames:
            raise RuntimeError("Cannot allocate RAII resource outside of an active scope")
        res = Resource(name, resource_type, details)
        self.frames[-1].register_resource(res)
        self.execution_log.append(f"Constructed [{resource_type}:{name}] in scope '{self.frames[-1].scope_name}'")
        return res

    def exit_scope(self) -> List[str]:
        """Exits the innermost scope, executing destructors in reverse construction order."""
        if not self.frames:
            raise RuntimeError("Stack underflow: No scope to exit")
        frame = self.frames.pop()
        logs = frame.unwind()
        for res in reversed(frame.resources):
            self.released_resources.append(res)
        self.execution_log.append(f"Exited scope: {frame.scope_name}")
        self.execution_log.extend(logs)
        return logs

    def throw_exception(self, exception_type: str, message: str) -> Dict[str, Any]:
        """
        Simulates throwing an exception and unwinding stack frames
        until a frame catching exception_type is encountered.
        """
        self.execution_log.append(f"EXCEPTION THROWN [{exception_type}]: {message}")
        unwound_frames = []
        released_during_unwind = []
        caught = False
        handler_scope = None

        while self.frames:
            current_frame = self.frames.pop()
            unwound_frames.append(current_frame.scope_name)
            logs = current_frame.unwind()
            self.execution_log.extend(logs)
            for res in reversed(current_frame.resources):
                released_during_unwind.append(res)
                self.released_resources.append(res)

            if exception_type in current_frame.catch_types:
                caught = True
                handler_scope = current_frame.scope_name
                self.execution_log.append(f"Exception [{exception_type}] CAUGHT by handler in scope '{handler_scope}'")
                break

        return {
            "exception_type": exception_type,
            "message": message,
            "caught": caught,
            "handler_scope": handler_scope,
            "unwound_scopes": unwound_frames,
            "released_count": len(released_during_unwind),
        }


class DispatchProfiler:
    """Models compile-time template monomorphization vs runtime vtable dynamic dispatch overheads."""

    def __init__(self):
        pass

    @staticmethod
    def profile_static_dispatch(iterations: int) -> Dict[str, Any]:
        """
        Simulates static template / inline monomorphization dispatch.
        Cost model: Direct inline call = 1 CPU cycle per call, 0 pointer dereferences, 0 branch misses.
        """
        cycles_per_call = 1
        total_cycles = iterations * cycles_per_call
        return {
            "mode": "Static Template Monomorphization",
            "iterations": iterations,
            "vptr_lookups": 0,
            "indirect_branches": 0,
            "btb_misses": 0,
            "estimated_cycles": total_cycles,
            "cycles_per_call": cycles_per_call,
            "overhead_tax_percent": 0.0,
        }

    @staticmethod
    def profile_dynamic_vtable_dispatch(iterations: int, btb_miss_rate: float = 0.05) -> Dict[str, Any]:
        """
        Simulates virtual function table (vtable) dynamic dispatch.
        Cost model:
          - Load vptr from instance: 1 cycle
          - Load function pointer from vtable: 1 cycle
          - Indirect branch execution: 2 cycles
          - BTB branch misprediction penalty (if miss): +12 cycles
        """
        base_cycles_per_call = 4
        misses = int(iterations * btb_miss_rate)
        mispredict_penalty = 12
        total_cycles = (iterations * base_cycles_per_call) + (misses * mispredict_penalty)
        avg_cycles = total_cycles / iterations if iterations > 0 else 0

        static_cycles = iterations * 1
        tax = ((total_cycles - static_cycles) / static_cycles) * 100.0 if static_cycles > 0 else 0.0

        return {
            "mode": "Dynamic vtable Indirect Dispatch",
            "iterations": iterations,
            "vptr_lookups": iterations,
            "indirect_branches": iterations,
            "btb_misses": misses,
            "estimated_cycles": total_cycles,
            "cycles_per_call": avg_cycles,
            "overhead_tax_percent": round(tax, 2),
        }


class GenericIteratorContract:
    """Demonstrates STL container-algorithm decoupling via generic iterator interfaces."""

    def __init__(self, data: List[int]):
        self.data = list(data)

    def accumulate_via_iterator(self, init_value: int = 0) -> Tuple[int, int]:
        """
        Executes a generic std::accumulate algorithm over container iterators.
        Returns (result, operation_count).
        """
        ops = 0
        current = init_value
        for val in self.data:
            current += val
            ops += 1  # 1 addition, 1 iterator advance
        return current, ops

    def sort_via_random_access() -> Tuple[List[int], int]:
        """Simulates std::sort over random access iterators."""
        pass


def run_raii_demo() -> Dict[str, Any]:
    """Runs a complete demonstration of C++ RAII lifetime and stack unwinding."""
    stack = ScopeStack()

    # Scope 1: main() function scope with exception handler
    stack.enter_scope("main_scope", catch_types=["std::runtime_error"])
    stack.allocate("heap_buffer", "unique_ptr<char[]>", {"size": 1024})

    # Scope 2: process_data() inner block
    stack.enter_scope("process_data_block")
    stack.allocate("file_handle", "ifstream", {"file": "dataset.csv"})
    stack.allocate("mutex_lock", "lock_guard<mutex>", {"mutex": "data_mtx"})

    # Scope 3: nested calculation block
    stack.enter_scope("calculation_block")
    stack.allocate("temp_matrix", "vector<double>", {"elements": 100000})

    # Throw exception inside calculation block
    unwind_report = stack.throw_exception("std::runtime_error", "Matrix singular error during inversion")

    return {
        "execution_log": stack.execution_log,
        "unwind_report": unwind_report,
        "total_released_resources": [r.name for r in stack.released_resources],
    }


if __name__ == "__main__":
    demo = run_raii_demo()
    print("=== C++ RAII & Exception Unwinding Demo ===")
    for entry in demo["execution_log"]:
        print(f"  {entry}")
    print("\nUnwind Report:", demo["unwind_report"])
