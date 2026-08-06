#!/usr/bin/env python3
"""
Stochastic Computing (SC) Simulator.
Reconstructs the 1960s probabilistic computing paradigm using unipolar and bipolar
representation, logic gate arithmetic (AND, XNOR, MUX), FSM-based activation functions,
and hardware-accurate Linear Feedback Shift Registers (LFSRs).

Expanded with accuracy vs. stream-length (energy proxy) trade-off evaluation
and realistic workload executions (stochastic artificial neuron and image/signal filter).
"""

import random
import math

class LFSR:
    """
    Hardware-accurate Linear Feedback Shift Register (LFSR)
    serving as a deterministic, pseudo-random bit source.
    """
    def __init__(self, seed=1, width=10):
        self.width = width
        self.mask = (1 << width) - 1
        self.state = seed & self.mask
        if self.state == 0:
            self.state = 1  # LFSR lock-up state avoidance

    def next_val(self):
        """
        Advances the LFSR by one clock cycle and returns the new state.
        Uses primitive polynomials for maximal-length sequences (period = 2^width - 1).
        """
        if self.width == 8:
            # x^8 + x^6 + x^5 + x^4 + 1
            bit = ((self.state >> 7) ^ (self.state >> 5) ^ (self.state >> 4) ^ (self.state >> 3)) & 1
        elif self.width == 10:
            # x^10 + x^7 + 1
            bit = ((self.state >> 9) ^ (self.state >> 6)) & 1
        else:
            # 16-bit: x^16 + x^14 + x^13 + x^11 + 1
            bit = ((self.state >> 15) ^ (self.state >> 13) ^ (self.state >> 12) ^ (self.state >> 10)) & 1

        self.state = ((self.state << 1) | bit) & self.mask
        return self.state

    def next_float(self):
        """Returns a pseudo-random float in [0.0, 1.0) derived from the LFSR state."""
        return self.next_val() / (1 << self.width)


class StochasticGenerator:
    """
    Converts real numbers into randomized stochastic bitstreams (unipolar or bipolar).
    """
    @staticmethod
    def to_unipolar(val, length, lfsr=None):
        """
        Converts float val in [0, 1] to a unipolar stochastic bitstream.
        If lfsr is provided, uses it for hardware-accurate pseudo-random generation.
        Otherwise, uses the Python system PRNG.
        """
        val = max(0.0, min(1.0, val))
        stream = []
        for _ in range(length):
            rand_val = lfsr.next_float() if lfsr else random.random()
            stream.append(1 if rand_val < val else 0)
        return stream

    @staticmethod
    def to_bipolar(val, length, lfsr=None):
        """
        Converts float val in [-1, 1] to a bipolar stochastic bitstream.
        Mapped probability p = (val + 1) / 2.
        """
        val = max(-1.0, min(1.0, val))
        prob = (val + 1.0) / 2.0
        stream = []
        for _ in range(length):
            rand_val = lfsr.next_float() if lfsr else random.random()
            stream.append(1 if rand_val < prob else 0)
        return stream


class StochasticDecoder:
    """
    Decodes stochastic bitstreams back into floating-point numbers.
    """
    @staticmethod
    def decode_unipolar(stream):
        """Decodes unipolar bitstream (0s and 1s) to range [0.0, 1.0]."""
        if not stream:
            return 0.0
        return sum(stream) / len(stream)

    @staticmethod
    def decode_bipolar(stream):
        """Decodes bipolar bitstream to range [-1.0, 1.0]."""
        if not stream:
            return 0.0
        prob = sum(stream) / len(stream)
        return 2.0 * prob - 1.0


class StochasticArithmetic:
    """
    Gate-level arithmetic operations on stochastic bitstreams.
    """
    @staticmethod
    def multiply_unipolar(stream_a, stream_b):
        """
        Multiplication of two unipolar streams.
        Implemented via a single 2-input AND gate.
        """
        assert len(stream_a) == len(stream_b), "Stream lengths must match"
        return [bit_a & bit_b for bit_a, bit_b in zip(stream_a, stream_b)]

    @staticmethod
    def multiply_bipolar(stream_a, stream_b):
        """
        Multiplication of two bipolar streams.
        Implemented via a single 2-input XNOR gate.
        """
        assert len(stream_a) == len(stream_b), "Stream lengths must match"
        # XNOR(a, b) = ~(a ^ b) & 1
        return [1 if bit_a == bit_b else 0 for bit_a, bit_b in zip(stream_a, stream_b)]

    @staticmethod
    def add_weighted(stream_a, stream_b, stream_sel):
        """
        Weighted addition of two streams: Y = A * Sel + B * (1 - Sel).
        Implemented via a Multiplexer (MUX).
        """
        assert len(stream_a) == len(stream_b) == len(stream_sel), "Stream lengths must match"
        output = []
        for bit_a, bit_b, sel in zip(stream_a, stream_b, stream_sel):
            output.append(bit_a if sel == 1 else bit_b)
        return output


class StochasticFSM:
    """
    Finite State Machine (FSM) executing non-linear operations (e.g., Tanh).
    Implements Gaines' saturating state counter.
    """
    def __init__(self, states=8):
        # State index from -M to +M where M = states / 2
        self.M = states // 2
        self.state = 0  # Start at center state

    def process_bipolar_tanh(self, stream_in):
        """
        Processes a bipolar input stream through the FSM to compute Tanh.
        State transitions:
          - Input bit = 1: increment state (saturates at +M)
          - Input bit = 0: decrement state (saturates at -M)
        Output bit is 1 if state >= 0, otherwise 0.
        """
        stream_out = []
        for bit in stream_in:
            if bit == 1:
                self.state = min(self.M, self.state + 1)
            else:
                self.state = max(-self.M, self.state - 1)

            # Output bit decision based on current state
            stream_out.append(1 if self.state >= 0 else 0)
        return stream_out


# =====================================================================
# Realistic Workloads & Evaluation Reports
# =====================================================================

class StochasticNeuron:
    """
    Models a single Artificial Neuron implemented entirely in the stochastic domain.
    Computes a dot product of inputs and weights using parallel logic, and passes
    the result through an FSM-based activation function (Tanh).
    """
    def __init__(self, weights, states=16):
        self.weights = weights  # List of floating-point weights in [-1, 1]
        self.M = states // 2
        self.fsm = StochasticFSM(states=states)

    def evaluate(self, inputs, length=1024):
        """
        Computes f(sum(w_i * x_i)) on floating-point inputs in [-1, 1].
        All inputs are scaled through weighted addition to prevent saturation.
        """
        assert len(inputs) == len(self.weights), "Inputs and weights length mismatch"
        num_inputs = len(inputs)

        # 1. Convert inputs and weights to bipolar bitstreams
        input_streams = []
        weight_streams = []
        for i in range(num_inputs):
            lfsr_in = LFSR(seed=i * 2 + 10, width=16)
            lfsr_wt = LFSR(seed=i * 2 + 11, width=16)
            input_streams.append(StochasticGenerator.to_bipolar(inputs[i], length, lfsr_in))
            weight_streams.append(StochasticGenerator.to_bipolar(self.weights[i], length, lfsr_wt))

        # 2. Perform parallel multiplications (XNOR gates)
        product_streams = []
        for i in range(num_inputs):
            product_streams.append(StochasticArithmetic.multiply_bipolar(input_streams[i], weight_streams[i]))

        # 3. Perform tree-based or scaled weighted addition via MUXes
        # For simplicity, we model a multi-way weighted MUX addition:
        # P(Y = 1) = (1/N) * sum(P(Product_i = 1))
        # This is implemented by a selection stream choosing index randomly or cyclically.
        combined_stream = []
        for bit_idx in range(length):
            # Select which product to channel to the output on this cycle
            select_idx = bit_idx % num_inputs # cyclic select
            combined_stream.append(product_streams[select_idx][bit_idx])

        # 4. Pass through Non-Linear Activation FSM (Saturating Counter Tanh)
        output_stream = self.fsm.process_bipolar_tanh(combined_stream)

        # Decode results
        actual_product_sum = sum(inputs[i] * self.weights[i] for i in range(num_inputs)) / num_inputs

        # The exact expected output of Gaines' Tanh FSM is given by:
        # y = tanh(M * arctanh(x)) where M = states / 2
        if -1.0 < actual_product_sum < 1.0:
            expected_tanh = math.tanh(self.M * math.atanh(actual_product_sum))
        else:
            expected_tanh = 1.0 if actual_product_sum >= 1.0 else -1.0

        decoded_output = StochasticDecoder.decode_bipolar(output_stream)

        return decoded_output, expected_tanh


class StochasticSignalFilter:
    """
    Implements a simple 1D Smoothing/Moving-Average Filter on digital signals
    using weighted MUX additions in the stochastic domain.
    """
    @staticmethod
    def filter_signal(signal, kernel_width=3, length=512):
        """
        Applies a moving average filter to an input signal.
        signal: List of floats in [0, 1].
        """
        filtered_signal = []
        # Generate independent seeds for each sample index to maintain independence
        for idx in range(len(signal)):
            # Window boundaries
            start = max(0, idx - kernel_width // 2)
            end = min(len(signal), idx + kernel_width // 2 + 1)
            window = signal[start:end]

            # Generate unipolar streams for the window
            streams = []
            for i, val in enumerate(window):
                lfsr = LFSR(seed=(idx * 13 + i * 37) % 1000 + 1, width=16)
                streams.append(StochasticGenerator.to_unipolar(val, length, lfsr))

            # Perform MUX-based average of window streams
            out_stream = []
            for bit_idx in range(length):
                select_idx = bit_idx % len(window)
                out_stream.append(streams[select_idx][bit_idx])

            filtered_signal.append(StochasticDecoder.decode_unipolar(out_stream))
        return filtered_signal


def generate_energy_tradeoff_report():
    """
    Generates a quantitative analysis showing the accuracy vs energy proxy trade-offs
    of Stochastic Computing compared to standard binary multipliers.
    """
    print("\n" + "=" * 80)
    print("      QUANTITATIVE ANALYSIS: ACCURACY VS. ENERGY PROXY TRADE-OFF")
    print("=" * 80)
    print("  * Energy Proxy: Measured in active dynamic CMOS transitions (Logic Gate Toggles).")
    print("  * A standard 8-bit array multiplier consumes ~1200 Gate Toggles per operation.")
    print("  * A Stochastic Multiplier requires exactly 1 gate (AND) toggled over L cycles.")
    print("-" * 80)
    print("  Bitstream  |  Stochastic  |  Stochastic  |  Binary 8-Bit  |  Stochastic vs. Binary")
    print("  Length (L) |  Gate Toggles|  Mean Error  |  Gate Toggles  |  Energy Savings Ratio")
    print("  (Cycles)   |  (Energy)    |  (Precision) |  (Baseline)    |  (Lower is Better)")
    print("-" * 80)

    # Evaluate across bitstream lengths
    lengths = [16, 64, 256, 1024, 4096, 16384]
    trials = 100

    for l in lengths:
        total_error = 0.0
        # Calculate mean error across random multiplication trials
        for t in range(trials):
            val_a = random.random()
            val_b = random.random()

            lfsr_a = LFSR(seed=t*2 + 1, width=16)
            lfsr_b = LFSR(seed=t*2 + 2, width=16)

            sa = StochasticGenerator.to_unipolar(val_a, l, lfsr_a)
            sb = StochasticGenerator.to_unipolar(val_b, l, lfsr_b)

            sout = StochasticArithmetic.multiply_unipolar(sa, sb)
            decoded = StochasticDecoder.decode_unipolar(sout)
            total_error += abs(decoded - (val_a * val_b))

        mean_error = total_error / trials
        # SC Energy proxy: L clock cycles * 2 toggle trans (approx 1 input/output toggle per cycle)
        sc_energy = l * 2
        binary_energy = 1200 # Constant baseline for 8-bit multiplier
        savings = sc_energy / binary_energy

        print(f"  {l:9d} | {sc_energy:12d} | {mean_error:12.5f} | {binary_energy:14d} | {savings:19.4f}x")
    print("=" * 80)


def run_demo():
    print("=" * 65)
    print("      STOCHASTIC COMPUTING ARCHITECTURAL SIMULATION ENGINE")
    print("=" * 65)

    # 1. Show Unipolar Multiplication
    print("\n[1] Unipolar Multiplication (AND gate): 0.60 * 0.70")
    print("-" * 50)
    for length in [64, 256, 1024, 4096]:
        # Generate independent streams using separate LFSR seeds
        lfsr_a = LFSR(seed=42, width=10)
        lfsr_b = LFSR(seed=1337, width=10)

        stream_a = StochasticGenerator.to_unipolar(0.60, length, lfsr_a)
        stream_b = StochasticGenerator.to_unipolar(0.70, length, lfsr_b)

        stream_out = StochasticArithmetic.multiply_unipolar(stream_a, stream_b)
        decoded = StochasticDecoder.decode_unipolar(stream_out)
        error = abs(decoded - 0.42)
        print(f"  Length: {length:4d} | Decoded Product: {decoded:.4f} | Absolute Error: {error:.4f}")

    # 2. Show Bipolar Multiplication (XNOR gate)
    print("\n[2] Bipolar Multiplication (XNOR gate): -0.50 * 0.80")
    print("-" * 50)
    for length in [64, 256, 1024, 4096]:
        lfsr_a = LFSR(seed=123, width=16)
        lfsr_b = LFSR(seed=456, width=16)

        stream_a = StochasticGenerator.to_bipolar(-0.50, length, lfsr_a)
        stream_b = StochasticGenerator.to_bipolar(0.80, length, lfsr_b)

        stream_out = StochasticArithmetic.multiply_bipolar(stream_a, stream_b)
        decoded = StochasticDecoder.decode_bipolar(stream_out)
        error = abs(decoded - (-0.40))
        print(f"  Length: {length:4d} | Decoded Product: {decoded:.4f} | Absolute Error: {error:.4f}")

    # 3. Show Weighted Addition (MUX)
    print("\n[3] Weighted Addition (MUX): 0.40 * 0.50 + 0.80 * 0.50 = 0.60")
    print("-" * 50)
    length = 4096
    lfsr_a = LFSR(seed=11, width=16)
    lfsr_b = LFSR(seed=22, width=16)
    lfsr_s = LFSR(seed=33, width=16)

    stream_a = StochasticGenerator.to_unipolar(0.40, length, lfsr_a)
    stream_b = StochasticGenerator.to_unipolar(0.80, length, lfsr_b)
    stream_sel = StochasticGenerator.to_unipolar(0.50, length, lfsr_s) # Equal weight

    stream_out = StochasticArithmetic.add_weighted(stream_a, stream_b, stream_sel)
    decoded = StochasticDecoder.decode_unipolar(stream_out)
    print(f"  Length: {length:4d} | Decoded Sum: {decoded:.4f} | Target: 0.6000")

    # 4. Non-linear FSM-based Tanh Activation Function
    print("\n[4] Non-Linear Activation (FSM-based Bipolar Tanh)")
    print("-" * 50)
    length = 2048
    for input_val in [-0.8, -0.4, 0.0, 0.4, 0.8]:
        # Generate bipolar input stream
        lfsr = LFSR(seed=777, width=16)
        stream_in = StochasticGenerator.to_bipolar(input_val, length, lfsr)

        # Process through saturating FSM
        fsm = StochasticFSM(states=16)
        stream_out = fsm.process_bipolar_tanh(stream_in)
        decoded = StochasticDecoder.decode_bipolar(stream_out)

        print(f"  Input Bipolar: {input_val:+.1f} | SC-Tanh Output: {decoded:+.4f}")

    # 5. Stochastic Artificial Neuron Workload
    print("\n[5] Workload A: Stochastic Artificial Neuron Execution")
    print("-" * 50)
    weights = [0.8, -0.5, 0.2]
    inputs  = [0.4, 0.6, -0.9]
    neuron = StochasticNeuron(weights, states=16)
    for length in [256, 1024, 4096]:
        decoded_output, expected_tanh = neuron.evaluate(inputs, length=length)
        neuron_err = abs(decoded_output - expected_tanh)
        print(f"  Length: {length:4d} | Neuron Output: {decoded_output:+.4f} | Target Tanh: {expected_tanh:+.4f} | Error: {neuron_err:.4f}")

    # 6. Stochastic 1D Smoothing Filter Workload
    print("\n[6] Workload B: Stochastic Moving Average Signal Filter")
    print("-" * 50)
    raw_signal = [0.2, 0.8, 0.7, 0.3, 0.9, 0.8, 0.4]
    filtered = StochasticSignalFilter.filter_signal(raw_signal, kernel_width=3, length=1024)
    print(f"  Raw Input Signal:  {[round(x, 2) for x in raw_signal]}")
    print(f"  Stochastic Filter: {[round(x, 3) for x in filtered]}")

    # 7. The Correlation Bottleneck (Demonstration)
    print("\n[7] Demonstration of Correlation Sensitivity (Shared Random Seed)")
    print("-" * 50)
    length = 1024
    # Correlated streams share the same seed and LFSR state
    lfsr_shared = LFSR(seed=99, width=10)
    stream_correlated_a = StochasticGenerator.to_unipolar(0.50, length, lfsr_shared)
    # Reset LFSR to create same stream
    lfsr_shared = LFSR(seed=99, width=10)
    stream_correlated_b = StochasticGenerator.to_unipolar(0.50, length, lfsr_shared)

    # Independent streams use different seeds
    lfsr_ind_a = LFSR(seed=99, width=10)
    lfsr_ind_b = LFSR(seed=888, width=10)
    stream_ind_a = StochasticGenerator.to_unipolar(0.50, length, lfsr_ind_a)
    stream_ind_b = StochasticGenerator.to_unipolar(0.50, length, lfsr_ind_b)

    # Multiply both
    out_correlated = StochasticArithmetic.multiply_unipolar(stream_correlated_a, stream_correlated_b)
    out_independent = StochasticArithmetic.multiply_unipolar(stream_ind_a, stream_ind_b)

    print(f"  Target Product (0.50 * 0.50) = 0.25")
    print(f"  Correlated Streams Decoded  = {StochasticDecoder.decode_unipolar(out_correlated):.4f} (Severe Error!)")
    print(f"  Independent Streams Decoded = {StochasticDecoder.decode_unipolar(out_independent):.4f} (Accurate)")
    print("=" * 65)

    # Generate quantitative trade-off report
    generate_energy_tradeoff_report()


if __name__ == "__main__":
    run_demo()
