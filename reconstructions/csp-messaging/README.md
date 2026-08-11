# CSP Synchronous Messaging Simulator

A zero-dependency Python simulator implementing an **[occam](../../excavations/occam.md)-style synchronous message-passing engine** based on Tony Hoare's Communicating Sequential Processes (CSP) formalism.

---

## Technical Concept

Unlike standard shared-memory concurrency (where parallel threads share address spaces and synchronize via locks or semaphores), CSP focuses on isolated processes that communicate exclusively over **synchronous channels**.

1. **Rendezvous Concurrency**: Channels are unbuffered. Senders and receivers must rendezvous. Whichever process arrives first blocks until the other process arrives at the matching channel endpoint.
2. **Deterministic Multi-Channel Selection (ALT)**: The `ALT` (Alternative) construct allows a process to listen to multiple incoming channels simultaneously. The process blocks until *any* of the channels has a sender ready, executes that communication, and resumes.
3. **Deadlock Analysis**: Because communication topology is formal and synchronous, incorrect sequencing creates cyclic dependencies. The scheduler automatically detects **structural deadlock** when no cooperative processes can make progress, producing a comprehensive diagnostic trace of which process is blocked on which channel.

---

## Key Features

- **Cooperative Scheduler**: Implements lightweight cooperative scheduling using Python Generators (`yield`) to yield communication actions to a central coordinator.
- **Synchronous Channels**: Supports unbuffered `Channel.send(val)` and `Channel.recv()` rendezvous.
- **Multiplexed waiting**: Fully models `ALT` (Alternative) channel select statements.
- **Deadlock Diagnostics**: Discovers and reports circular wait dependencies and channel blocking in real-time.

---

## Running the Simulator

To run the built-in test suite and interactive CSP scenarios, execute:

```bash
python3 reconstructions/csp-messaging/csp_sim.py
```

### Visual Output Example

```text
--- Starting CSP Execution Run (Limit: 100 steps) ---
  [Block] Process [Producer] is waiting to SEND value '10' on Channel 'DataStream'
  [Block] Process [Consumer] is waiting to RECEIVE on Channel 'DataStream'
  *RENDEZVOUS* Channel 'DataStream': [Producer] ---> [Consumer] with Value '10'
  [Block] Process [Producer] is waiting to SEND value '20' on Channel 'DataStream'
  [Block] Process [Consumer] is waiting to RECEIVE on Channel 'DataStream'
  *RENDEZVOUS* Channel 'DataStream': [Producer] ---> [Consumer] with Value '20'
  [Exit] Process [Producer] finished execution (TERMINATED).
  [Exit] Process [Consumer] finished execution (TERMINATED).

[Success] All processes terminated successfully.
```
