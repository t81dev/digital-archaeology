# Linda Tuple Space Simulator

> **An interactive software reconstruction of David Gelernter's Linda coordination model implementing Generative Communication.**

---

## Overview

In traditional parallel and distributed computing, processes coordinate using **shared memory** (spatially coupled via physical address boundaries and managed by locks/semaphores) or **message passing** (temporally coupled sender-recipient channels).

**Linda** (introduced by David Gelernter at Yale University in 1982) pioneered a radically different paradigm called **Generative Communication**. Instead of direct communication, processes interact asynchronously and anonymously via a central, associative memory medium called a **Tuple Space**.

By replacing explicit channel addresses with associative, structural pattern-matching, Linda achieves complete **spatial decoupling** (processes communicate without knowing each other's identities) and **temporal decoupling** (tuples can persist in the space indefinitely, independent of their creators' lifespans).

---

## Conceptual Architecture

```
                            THE TUPLE SPACE ARCHITECTURE

      Process A                                                       Process B
 ┌─────────────────┐                                             ┌─────────────────┐
 │   out(tuple)    │ ───────── (deposits passive tuple) ───────> │                 │
 └─────────────────┘                                             │   in(pattern)   │
                                                                 │                 │
                                                                 │ (blocks/extracts│
                                                                 │  associatively) │
                                                                 └────────┬────────┘
                                                                          │
                                                                          ▼
 ┌────────────────────────────────────────────────────────────────────────┴────────┐
 │                                   TUPLE SPACE                                   │
 │                                                                                 │
 │   ("task", 101, [1, 2, 3])        ("sensor_data", "temp_sensor", 23.5)          │
 │                                                                                 │
 │   ("result", 101, 14, 3)          ("config", "port", 8080)                      │
 │                                                                                 │
 └─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Operations

Our zero-dependency, thread-safe Python simulator implements Linda's complete coordination operator suite:

1. **`out(tup)`**: Evaluates parameters and deposits a passive data tuple into the Tuple Space. Triggers notifications to any blocked threads waiting on matches.
2. **`in_(pattern)`**: Searches the Tuple Space for a tuple matching `pattern`, withdraws it from the space, and returns it. Blocks the calling thread if no match exists.
3. **`rd(pattern)`**: Same search as `in_`, but returns a copy of the matching tuple, leaving the original in the Tuple Space. Blocks if no match exists.
4. **`inp(pattern)`**: Non-blocking version of `in_`. Returns the matched tuple immediately if present (withdrawing it), otherwise returns `None`.
5. **`rdp(pattern)`**: Non-blocking version of `rd`. Returns a copy of the matched tuple immediately if present, otherwise returns `None`.
6. **`eval(func, *args)`**: Spawns an *active process tuple*. Evaluates `func(*args)` concurrently in a separate thread. Upon termination, it automatically deposits the result as a passive data tuple of the schema `("result", function_name, output)` back into the space.

---

## Pattern-Matching Semantics

A tuple $T$ in the space matches a pattern template $P$ if:
1. **Arity Match**: $T$ and $P$ have the exact same number of fields.
2. **Field-by-Field Match**:
   - **Formals**: If a field in $P$ is a Python class type (e.g., `int`, `str`, `float`), the corresponding field in $T$ must be an instance of that type.
   - **Wildcards**: If a field in $P$ is the global `ANY` placeholder, it matches any value.
   - **Actuals**: If a field in $P$ is a concrete value (e.g., `"sensor"`, `42`), the corresponding field in $T$ must equal that value exactly.

### Example Matches:

| Pattern (Template) | Tuple in Space | Match? | Explanation |
| :--- | :--- | :--- | :--- |
| `("sensor", int, float)` | `("sensor", 101, 23.5)` | **YES** | Arity is 3, types match in order, actual `"sensor"` matches. |
| `("sensor", int, float)` | `("sensor", "zone_a", 23.5)` | **NO** | Type mismatch (`str` instead of `int`). |
| `("sensor", ANY, float)` | `("sensor", "zone_a", 23.5)` | **YES** | Wildcard `ANY` matches `"zone_a"` successfully. |
| `("config", "port")` | `("config", "port", 8080)` | **NO** | Arity mismatch (2 fields vs 3 fields). |

---

## Master-Worker Showcase

The built-in demonstration implements a classic **coordinate-free worker pool**:
- **Master** anonymously drops computational tasks (`out(("task", task_id, num_list))`) and an active factorial computation (`eval(async_factorial, 5)`) into the Tuple Space.
- Three concurrent **Worker Nodes** poll the space for tasks (`in_(("task", int, list))`), perform the processing, and anonymously deposit result tuples back.
- **Master** block-waits on results (`in_(("result", int, int, int))`) and outputs the compiled results.

Neither the Master nor the Workers know each other's IDs or physical/thread boundaries. If more Worker threads are added, the task load automatically balances across them without a single line of orchestration code changing!

---

## How to Run

### Run the Interactive Simulator Demonstration:
You can execute the simulator demo directly from the root of the repository:
```bash
python3 reconstructions/tuple-space/tuple_space_sim.py
```

### Run the Unit Tests:
Validate the associative matching engine and concurrent safety primitives using `pytest`:
```bash
pytest reconstructions/tuple-space/
```
