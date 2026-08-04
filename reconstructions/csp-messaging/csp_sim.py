#!/usr/bin/env python3
"""
CSP Messaging Engine Simulator
Visualizes occam-style synchronized channel execution, ALT multi-channel waiting,
and structural deadlock detection / avoidance.
"""

import sys

class Channel:
    """
    An unbuffered, synchronous communication channel.
    Both sender and receiver must rendezvous (block until both are ready).
    """
    def __init__(self, name: str):
        self.name = name

    def send(self, value):
        """Yield this action to the scheduler to send a value."""
        return ('send', self, value)

    def recv(self):
        """Yield this action to the scheduler to receive a value."""
        return ('recv', self, None)

    def __repr__(self):
        return f"Channel('{self.name}')"


def alt_wait(*channels):
    """
    Wait on multiple channels simultaneously (occam ALT construct).
    Yields to the scheduler and resumes with (selected_channel, value).
    """
    return ('alt', list(channels), None)


class Process:
    """
    Represents a concurrent process managed by the cooperative CSP scheduler.
    """
    def __init__(self, name: str, generator):
        self.name = name
        self.generator = generator
        self.state = "READY"  # READY, BLOCKED, TERMINATED
        self.block_action = None  # Current action process is blocked on
        self.last_val = None      # Value to send back into the generator on resume

    def __repr__(self):
        return f"Process(name={self.name}, state={self.state})"


class CSPScheduler:
    """
    A cooperative CSP scheduler that manages process state transitions,
    synchronous channel rendezvous, ALT multiplexing, and deadlock detection.
    """
    def __init__(self, verbose=True):
        self.processes = []
        self.step_count = 0
        self.verbose = verbose
        self.log_history = []

    def log(self, message: str):
        self.log_history.append(message)
        if self.verbose:
            print(message)

    def register(self, name: str, generator_func, *args, **kwargs):
        """Registers a process generator with the scheduler."""
        p = Process(name, generator_func(*args, **kwargs))
        self.processes.append(p)
        return p

    def _run_ready_processes(self) -> bool:
        """Runs all READY processes for one cooperative step until they block or finish."""
        progress = False
        for p in self.processes:
            if p.state == "READY":
                progress = True
                try:
                    # Pass the result of the previous channel event into the generator
                    action = p.generator.send(p.last_val)
                    p.last_val = None  # Clear consumed value

                    # Process yielded a CSP action
                    if isinstance(action, tuple) and len(action) == 3:
                        act_type, target, val = action
                        p.block_action = action
                        p.state = "BLOCKED"
                        if act_type == "send":
                            self.log(f"  [Block] Process [{p.name}] is waiting to SEND value '{val}' on Channel '{target.name}'")
                        elif act_type == "recv":
                            self.log(f"  [Block] Process [{p.name}] is waiting to RECEIVE on Channel '{target.name}'")
                        elif act_type == "alt":
                            ch_names = ", ".join([c.name for c in target])
                            self.log(f"  [Block] Process [{p.name}] is waiting on ALT for channels: [{ch_names}]")
                    else:
                        # Process yielded something unrecognized, terminate it
                        p.state = "TERMINATED"
                        self.log(f"  [Exit] Process [{p.name}] yielded invalid action, terminated.")
                except StopIteration:
                    p.state = "TERMINATED"
                    self.log(f"  [Exit] Process [{p.name}] finished execution (TERMINATED).")
        return progress

    def _match_communications(self) -> int:
        """Looks for matching senders and receivers to perform synchronous rendezvous."""
        rendezvous_count = 0

        while True:
            matched = False
            for p1 in self.processes:
                if p1.state != "BLOCKED":
                    continue
                act1_type, target1, val1 = p1.block_action

                if act1_type == "send":
                    # Look for a matching receiver or ALT
                    for p2 in self.processes:
                        if p2.state != "BLOCKED" or p2 == p1:
                            continue
                        act2_type, target2, val2 = p2.block_action

                        if act2_type == "recv" and target2 == target1:
                            # Direct match (Sender meets Receiver)
                            self._execute_rendezvous(p1, p2, target1, val1)
                            matched = True
                            rendezvous_count += 1
                            break
                        elif act2_type == "alt" and target1 in target2:
                            # ALT match (Sender meets ALT listener)
                            self._execute_rendezvous_alt(p1, p2, target1, val1)
                            matched = True
                            rendezvous_count += 1
                            break
                if matched:
                    break  # Restart scanning from beginning for scheduling fairness
            if not matched:
                break

        return rendezvous_count

    def _execute_rendezvous(self, p_send, p_recv, channel, val):
        self.log(f"  *RENDEZVOUS* Channel '{channel.name}': [{p_send.name}] ---> [{p_recv.name}] with Value '{val}'")
        p_send.state = "READY"
        p_send.block_action = None
        p_send.last_val = None

        p_recv.state = "READY"
        p_recv.block_action = None
        p_recv.last_val = val

    def _execute_rendezvous_alt(self, p_send, p_alt, channel, val):
        self.log(f"  *ALT-RENDEZVOUS* Channel '{channel.name}': [{p_send.name}] ---> [{p_alt.name}] with Value '{val}'")
        p_send.state = "READY"
        p_send.block_action = None
        p_send.last_val = None

        p_alt.state = "READY"
        p_alt.block_action = None
        p_alt.last_val = (channel, val)  # Passes both the channel and the value

    def run(self, limit=100) -> bool:
        """
        Executes the scheduler.
        Returns True if all processes finished successfully.
        Returns False if a structural deadlock is detected.
        """
        self.log(f"\n--- Starting CSP Execution Run (Limit: {limit} steps) ---")
        while self.step_count < limit:
            progress_made = self._run_ready_processes()

            rendezvous_made = self._match_communications()
            if rendezvous_made > 0:
                progress_made = True

            # Check if all processes are finished
            all_terminated = all(p.state == "TERMINATED" for p in self.processes)
            if all_terminated:
                self.log("\n[Success] All processes terminated successfully.")
                return True

            if not progress_made:
                self.log("\n[DEADLOCK] No progress could be made! All active processes are blocked.")
                self._report_deadlock()
                return False

            self.step_count += 1

        self.log(f"\n[Limit Exceeded] Exceeded step execution limit of {limit}.")
        return False

    def _report_deadlock(self):
        print("\n" + "=" * 50)
        print("           STRUCTURAL DEADLOCK REPORT")
        print("=" * 50)
        for p in self.processes:
            if p.state == "BLOCKED":
                act_type, target, val = p.block_action
                if act_type == "send":
                    print(f"  Process [{p.name}]: Blocked trying to SEND '{val}' on Channel '{target.name}'")
                elif act_type == "recv":
                    print(f"  Process [{p.name}]: Blocked trying to RECEIVE on Channel '{target.name}'")
                elif act_type == "alt":
                    ch_names = ", ".join([c.name for c in target])
                    print(f"  Process [{p.name}]: Blocked on ALT waiting for any of: [{ch_names}]")
            elif p.state == "TERMINATED":
                print(f"  Process [{p.name}]: Already completed (TERMINATED)")
            else:
                print(f"  Process [{p.name}]: State is {p.state} (Inconsistent state!)")
        print("=" * 50)


# =========================================================
# Demo Demos & CSP Scenarios
# =========================================================

# 1. Classical Producer-Consumer Rendezvous
def producer_proc(chan_out, items):
    for item in items:
        yield chan_out.send(item)
    # End of process

def consumer_proc(chan_in, expected_count):
    for _ in range(expected_count):
        val = yield chan_in.recv()
        # Processing received value...


# 2. ALT Multiplexer (Multiplexing two separate channels)
def alt_multiplexer_proc(chan_a, chan_b, chan_out, count):
    for _ in range(count):
        # Wait on either channel A or channel B
        selected_chan, val = yield alt_wait(chan_a, chan_b)
        # Forward result onto output channel with indicator
        yield chan_out.send(f"Mux({selected_chan.name}:{val})")


def forward_consumer_proc(chan_in, count):
    for _ in range(count):
        yield chan_in.recv()


# 3. Structural Deadlock Demonstration
def deadlocked_p1_proc(chan_x, chan_y):
    # Process 1 tries to send on X first, then receive on Y
    yield chan_x.send("P1_Msg")
    yield chan_y.recv()

def deadlocked_p2_proc(chan_x, chan_y):
    # Process 2 also tries to send on Y first, then receive on X
    # This forms a cyclic wait (deadlock) because both are blocked on sending!
    yield chan_y.send("P2_Msg")
    yield chan_x.recv()


# 4. Structural Deadlock Avoidance (Corrected version)
def avoided_p1_proc(chan_x, chan_y):
    yield chan_x.send("P1_Safe_Msg")
    val = yield chan_y.recv()

def avoided_p2_proc(chan_x, chan_y):
    # Process 2 receives first, matching Process 1's send, then sends. No deadlock!
    val = yield chan_x.recv()
    yield chan_y.send("P2_Safe_Msg")


def run_producer_consumer_demo():
    print("\n" + "=" * 60)
    print("Demo 1: Synchronous Producer-Consumer Rendezvous")
    print("=" * 60)
    scheduler = CSPScheduler(verbose=True)
    c = Channel("DataStream")
    scheduler.register("Producer", producer_proc, c, [10, 20, 30])
    scheduler.register("Consumer", consumer_proc, c, 3)
    success = scheduler.run()
    assert success, "Producer-Consumer rendezvous failed!"


def run_alt_multiplexer_demo():
    print("\n" + "=" * 60)
    print("Demo 2: occam-style ALT Multi-Channel Selection")
    print("=" * 60)
    scheduler = CSPScheduler(verbose=True)
    chan_a = Channel("ChanA")
    chan_b = Channel("ChanB")
    chan_out = Channel("ChanOut")

    scheduler.register("ProducerA", producer_proc, chan_a, ["Apple", "Apricot"])
    scheduler.register("ProducerB", producer_proc, chan_b, ["Banana", "Berry"])
    scheduler.register("Multiplexer", alt_multiplexer_proc, chan_a, chan_b, chan_out, 4)
    scheduler.register("OutConsumer", forward_consumer_proc, chan_out, 4)

    success = scheduler.run()
    assert success, "ALT multiplexer demo failed!"


def run_deadlock_demo():
    print("\n" + "=" * 60)
    print("Demo 3: Structural Deadlock Detection")
    print("=" * 60)
    scheduler = CSPScheduler(verbose=True)
    chan_x = Channel("ChanX")
    chan_y = Channel("ChanY")

    scheduler.register("DeadlockedP1", deadlocked_p1_proc, chan_x, chan_y)
    scheduler.register("DeadlockedP2", deadlocked_p2_proc, chan_x, chan_y)

    success = scheduler.run()
    assert not success, "Expected deadlock was not detected!"
    print("  [Verified] Scheduler successfully detected structural deadlock.")


def run_deadlock_avoidance_demo():
    print("\n" + "=" * 60)
    print("Demo 4: Structural Deadlock Avoidance")
    print("=" * 60)
    scheduler = CSPScheduler(verbose=True)
    chan_x = Channel("ChanX")
    chan_y = Channel("ChanY")

    scheduler.register("SafeP1", avoided_p1_proc, chan_x, chan_y)
    scheduler.register("SafeP2", avoided_p2_proc, chan_x, chan_y)

    success = scheduler.run()
    assert success, "Deadlock avoidance scheme failed!"
    print("  [Verified] Correct scheduling order completely avoided deadlock.")


def main():
    # Automatically execute all verification scenarios
    run_producer_consumer_demo()
    run_alt_multiplexer_demo()
    run_deadlock_demo()
    run_deadlock_avoidance_demo()

    # Only run interactive CLI if connected to an interactive tty
    if sys.stdin.isatty():
        print("\n" + "=" * 60)
        print("Welcome to the Interactive CSP Messaging Engine Simulator!")
        print("=" * 60)
        while True:
            print("\nInteractive Options:")
            print("1. Re-run Producer-Consumer Rendezvous")
            print("2. Re-run ALT Multiplexer")
            print("3. Re-run Deadlock Detection Demo")
            print("4. Re-run Deadlock Avoidance Demo")
            print("5. Exit")
            try:
                choice = input("Enter choice (1-5): ").strip()
                if choice == '1':
                    run_producer_consumer_demo()
                elif choice == '2':
                    run_alt_multiplexer_demo()
                elif choice == '3':
                    run_deadlock_demo()
                elif choice == '4':
                    run_deadlock_avoidance_demo()
                elif choice == '5':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice, select between 1 and 5.")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break
    else:
        print("\nNon-interactive mode: All CSP demos passed successfully.")

if __name__ == "__main__":
    main()
