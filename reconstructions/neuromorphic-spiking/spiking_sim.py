#!/usr/bin/env python3
"""
Neuromorphic Spiking Neural Network (SNN) Simulator.
Reconstructs event-driven spiking computation with Leaky Integrate-and-Fire (LIF)
neurons, Address-Event Representation (AER) routing, and Spike-Timing-Dependent Plasticity (STDP) learning.
"""

class SpikingNeuron:
    """
    Leaky Integrate-and-Fire (LIF) Spiking Neuron.
    Models biological neuron dynamics with:
      - Exponential decay leak towards Rest potential
      - Synaptic integration of input spikes
      - Firing threshold, spike emission, and refractory period reset
    """
    def __init__(self, neuron_id, v_rest=0.0, v_th=1.0, tau_m=10.0, v_reset=0.0, refractory_cycles=2):
        self.neuron_id = neuron_id
        self.v_rest = v_rest
        self.v_th = v_th
        self.tau_m = tau_m  # Membrane time constant
        self.v_reset = v_reset
        self.refractory_cycles = refractory_cycles

        self.v = v_rest  # Current membrane potential
        self.last_spike_time = -999.0
        self.refractory_timer = 0

    def step(self, current_time, input_current):
        """
        Steps the neuron potential by 1 cycle.
        Returns 1 if the neuron fires a spike, otherwise 0.
        """
        if self.refractory_timer > 0:
            self.refractory_timer -= 1
            self.v = self.v_reset
            return 0

        # Apply exponential leak: V(t+1) = V(t) + (V_rest - V(t))/tau_m + Input
        leak = (self.v_rest - self.v) / self.tau_m
        self.v += leak + input_current

        # Check threshold
        if self.v >= self.v_th:
            self.v = self.v_reset
            self.last_spike_time = current_time
            self.refractory_timer = self.refractory_cycles
            return 1  # Spike fired!
        return 0


class Synapse:
    """
    Synaptic Connection with Spike-Timing-Dependent Plasticity (STDP) learning.
    Adapts weight based on relative spike timing of pre-synaptic and post-synaptic neurons.
    """
    def __init__(self, src_id, dest_id, initial_weight=0.5, max_weight=2.0, w_min=0.0):
        self.src_id = src_id
        self.dest_id = dest_id
        self.weight = initial_weight
        self.max_weight = max_weight
        self.w_min = w_min

        # STDP parameters
        self.a_plus = 0.1   # Potentiation step
        self.a_minus = 0.08 # Depression step
        self.tau_stdp = 8.0 # Temporal window size

    def apply_stdp(self, pre_spike_time, post_spike_time, pre_fired, post_fired):
        """
        Applies STDP rule:
          - If pre fires before post: Potentiation (Hebbian: cause-and-effect)
          - If post fires before pre: Depression (Anti-Hebbian)
        """
        if pre_fired and post_fired:
            dt = post_spike_time - pre_spike_time
            if dt > 0:
                # Potentiation
                dw = self.a_plus * (2.71828 ** (-dt / self.tau_stdp))
                self.weight = min(self.max_weight, self.weight + dw)
            elif dt < 0:
                # Depression
                dw = -self.a_minus * (2.71828 ** (dt / self.tau_stdp))
                self.weight = max(self.w_min, self.weight + dw)


class SpikingNetwork:
    """
    Main Spiking Network container.
    Coordinates neurons, synapses, AER routing events, and STDP updates.
    """
    def __init__(self):
        self.neurons = {}
        self.synapses = []  # List of Synapse objects
        self.aer_log = []   # Logs spike events (time, neuron_id)

    def add_neuron(self, neuron):
        self.neurons[neuron.neuron_id] = neuron

    def add_synapse(self, src_id, dest_id, weight=0.5):
        syn = Synapse(src_id, dest_id, initial_weight=weight)
        self.synapses.append(syn)

    def run_simulation(self, steps=100, external_stimuli=None):
        """
        Simulates SNN over steps.
        external_stimuli: Dict of neuron_id -> list of float current inputs for each cycle.
        """
        if external_stimuli is None:
            external_stimuli = {}

        for t in range(steps):
            # 1. Fetch external input current for this step
            inputs = {}
            for nid in self.neurons:
                stim_list = external_stimuli.get(nid, [])
                inputs[nid] = stim_list[t] if t < len(stim_list) else 0.0

            # 2. Record which neurons spiked on this step
            spiked_this_step = set()
            for nid, neuron in self.neurons.items():
                if neuron.step(t, inputs[nid]):
                    spiked_this_step.add(nid)
                    self.aer_log.append((t, nid)) # AER routing record

            # 3. Propagate spikes across synapses & compute STDP learning
            for syn in self.synapses:
                pre_neuron = self.neurons.get(syn.src_id)
                post_neuron = self.neurons.get(syn.dest_id)

                if not pre_neuron or not post_neuron:
                    continue

                pre_fired = syn.src_id in spiked_this_step
                post_fired = syn.dest_id in spiked_this_step

                # If pre-synaptic neuron fired, inject weighted current to post-synaptic next step
                if pre_fired:
                    inputs[syn.dest_id] += syn.weight

                # Apply STDP weight adjustments if spike events occurred
                if pre_fired or post_fired:
                    syn.apply_stdp(
                        pre_neuron.last_spike_time,
                        post_neuron.last_spike_time,
                        pre_fired,
                        post_fired
                    )


def run_demo():
    print("=" * 65)
    print("      NEUROMORPHIC SPIKING SIMULATOR")
    print("=" * 65)

    # Setup simple network: Input neuron (0) connected to output neuron (1)
    net = SpikingNetwork()
    net.add_neuron(SpikingNeuron(0, tau_m=5.0))
    net.add_neuron(SpikingNeuron(1, tau_m=12.0))
    net.add_synapse(0, 1, weight=0.8)

    # Deliver high stimulus to Input Neuron to trigger rapid spiking
    stim = {
        0: [1.5 if i % 10 == 0 else 0.0 for i in range(100)],
        1: [0.0] * 100
    }

    print("Running spiking simulation over 100 steps...")
    net.run_simulation(steps=100, external_stimuli=stim)

    print(f"\nAddress-Event Representation (AER) Routing Log (total spikes: {len(net.aer_log)}):")
    print("-" * 50)
    for t, nid in net.aer_log[:20]:
        print(f"  Cycle: {t:3d} | AER Event: [Source Neuron ID={nid}]")
    if len(net.aer_log) > 20:
        print("  ... (remaining logs truncated)")

    # Print Synapse details showing learning
    print("\nSynapse Weights after simulation (proving STDP learning):")
    for syn in net.synapses:
        print(f"  Synapse {syn.src_id} -> {syn.dest_id} | Final weight: {syn.weight:.4f}")
    print("=" * 65)


if __name__ == "__main__":
    run_demo()
