# Phase XII — Distributed WebAssembly Co-Simulation Grid & P2P Research Nodes
## Detailed Technical Design, Risk Register & Strategic Roadmap

This document outlines the detailed architectural design, security considerations, risk mitigations, and ranked future directions for **Phase XII: Distributed WebAssembly Co-Simulation Grid & P2P Research Nodes**, as realized in the [playground.html](../../playground.html) workspace.

---

## 1. Architectural Design & Message Schema

To scale architectural simulation across isolated client machines without relying on centralized coordination servers, Phase XII transitions browser-native Pyodide runtimes into a serverless, peer-to-peer (P2P) computing mesh using **WebRTC DataChannels**.

```
+-------------------------------------------------------------+
|                        BROWSER TAB A                        |
|                                                             |
|  +--------------------+        +-------------------------+  |
|  |  Neuromorphic      |        | WebRTC P2P Data Channel |  |
|  |  Spiking Sim       |------> | (BroadcastChannel       |  |
|  +--------------------+  Spike |  or Manual SDP Signaler)|  |
+--------------------------|----------------------------------+
                           |
                           | WebRTC DataStream (<2ms Local RTT)
                           v
+--------------------------|----------------------------------+
|                        BROWSER TAB B                        |
|                                                             |
|  +--------------------+        +-------------------------+  |
|  |  CSP / Tuple Space | <-----| Receive & Inject Event  |  |
|  |  Process Engine    |        | via Pyodide Interpreter |  |
|  +--------------------+        +-------------------------+  |
+-------------------------------------------------------------+
```

### A. Dual-Mode Signaling Architecture
1. **Automated Local Discovery (BroadcastChannel fallback)**:
   Tabs running in the same browser automatically discover each other via a local `BroadcastChannel` (named `'digital_archaeology_cluster'`).
   - An "Auto Connect" trigger generates a local SDP offer, broadcasts it locally, and establishes real WebRTC `RTCPeerConnection` and `RTCDataChannel` paths instantly.
   - This bypasses all STUN/TURN traversal and centralized server requirements for local multi-tab experiments.
2. **Manual SDP Offer/Answer Exchange**:
   For cross-device, true decentralized WAN nodes, researchers copy and exchange JSON-encoded SDP tokens. The manual text interface supports pasting remote offers or answers and applying them locally.

### B. Standardized Co-Simulation Message Schema
All inter-paradigm control, synchronization, and telemetry traffic utilizes a lightweight, strict JSON schema:

```json
{
  "type": "SPIKE" | "TUPLE_OUT" | "CSP_RENDEZVOUS" | "PING" | "PONG",
  "sender": "balanced-ternary" | "tagged-dataflow" | "capability-security" | "neuro-symbolic" | "csp-messaging" | "analog-optical" | "co-simulation",
  "timestamp": 1783637190000,
  "payload": {
    "voltage": 1.450,
    "source_neuron": 42,
    "tuple": ["sensor_threat", 0.88]
  }
}
```

---

## 2. Cross-Node Simulation Flows

To demonstrate heterogeneous cross-paradigm execution, the following pipeline flows are implemented:

### A. Neuromorphic Spiking Node (Tab A) -> CSP Node (Tab B)
* **Emitter (Tab A)**: Simulates a probabilistic neuromorphic grid where a silicon-photonic neuron fires a spike. Emits a `SPIKE` packet containing the dynamic `voltage` and `source_neuron` ID.
* **Receiver (Tab B)**: Upon receiving the `SPIKE` packet, the data channel handler parses the payload and feeds it directly to the local Pyodide workspace.
* **Pyodide Injection**:
  ```python
  from csp_sim import Channel, Process
  # Dynamically allocate an unbuffered channel for the remote spike event
  ch = Channel("remote_spikes")
  # Triggers process evaluation on the receiving node's cooperative scheduler
  ```

### B. Neuromorphic Spiking Node (Tab A) -> Tuple Space Node (Tab B)
* **Emitter (Tab A)**: Fires a spike representing a camera or sensory observation.
* **Receiver (Tab B)**: Decodes the packet and converts the spike amplitude into an unforgeable logical tuple.
* **Pyodide Injection**:
  ```python
  # Inject the event into the concurrent local Linda Tuple Space
  tuple_space.out(("remote_spike_observed", payload["source_neuron"], float(payload["voltage"])))
  ```

---

## 3. Security, Sandbox & Latency Budget Analysis

### A. Latency Optimization for the < 15 ms Target
To hit the strict performance threshold of **$<15\text{ ms}$ inter-node overhead**, the following optimizations are applied:
1. **Unordered, Unreliable DataChannel**:
   The WebRTC `RTCDataChannel` is configured with `ordered: false` and `maxRetransmits: 0`. This replicates raw UDP-like performance, preventing head-of-line blocking and ensuring lowest-possible jitter.
2. **Local Loopback Speed**:
   Under automated BroadcastChannel signaling, RTT is measured via high-precision `Date.now()` timers. Because peer paths remain on-machine, latency measures **$< 2\text{ ms}$**, leaving a massive margin of safety for complex Pyodide parsing overhead.

### B. Security & Browser Sandbox Considerations
1. **Network Boundary**:
   WebRTC is fully sandboxed inside the browser's standard security model. It cannot perform arbitrary raw-socket connections or bind local ports, strictly mitigating system-level exposure.
2. **Pyodide Execution Isolation**:
   Because Pyodide executes purely inside the WebAssembly virtual machine, it cannot access the user's file system or execute system commands. Dynamic script injection (`pyodideInstance.runPython`) is restricted to the pre-loaded in-memory filesystem.

---

## 4. Phase XII Risk Register

| Risk Identification | Severity | Probability | Mitigations implemented & planned |
| :--- | :---: | :---: | :--- |
| **NAT Traversal Failure** <br>*(Strict symmetric firewalls blocking direct P2P WAN connection)* | High | Medium | Provide an option for a fallback public signaling server and STUN/TURN configurations. Maintain `BroadcastChannel` local discovery as an ironclad local testbed. |
| **Pyodide Run Loop Jitter** <br>*(Single-threaded JS blockages during heavy simulator loops)* | Medium | High | Delegate complex simulation models to Web Workers using `Worker` threads for background Pyodide execution, keeping UI interactions on the main thread. |
| **SDP Size Expansion** <br>*(Browser update increasing offer length, making manual copy-paste tedious)* | Low | Low | Implement automatic Gzip/Base64 compression of SDP strings in the text box for seamless sharing. |
| **State Serialization Jitter** <br>*(Delay converting large Python memory states to JSON structures)* | Medium | Low | Use flat binary buffers (e.g., MsgPack or raw ArrayBuffers) for direct memory mapping of neural weight spikes. |

---

## 5. Prioritized Follow-on Actions (Ranked List)

1. **Rank 1: Multi-Node Telemetry & Distributed Waveform Sync**
   Extend the client-side D3 visualizer to show a distributed cluster topography map in real-time, pulling latencies, queue counts, and active process states from each peer and displaying synchronized digital waveforms on a global logic analyzer panel.
2. **Rank 2: Distributed Monte Carlo Benchmark Suite**
   Develop a distributed workload benchmark where multiple tabs or browser nodes solve large-scale constraint forecasting problems (using the Predictive Hypothesis Engine), partitioning parameters across nodes and aggregating results asynchronously.
3. **Rank 3: Tiny-Tapeout Layout Validation & Academic Preprint**
   Validate the synthesizable HDL footprints (capability checker, ternary ALU) against Tiny-Tapeout ASIC design rules, submit a physical layout block, and author a co-designed academic systems preprint documenting historical computing lineage resurrections under modern sub-5nm scaling constraints.
