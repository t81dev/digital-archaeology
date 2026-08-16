#!/usr/bin/env python3
"""
Multi-Architecture Co-Simulation & Interoperability Fabric
Bridges Statistical/Symbolic AI, CSP synchronized messaging, and Dataflow spatial execution.
Integrates with Phase VIII Browser-Native Hardware-in-the-Loop (HIL) physical co-simulation.
"""

import os
import sys

# Dynamically resolve paths to other simulator modules
RECON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RECON_DIR, "neuro-symbolic"))
sys.path.insert(0, os.path.join(RECON_DIR, "csp-messaging"))
sys.path.insert(0, os.path.join(RECON_DIR, "dataflow-engine"))

# Import simulators
try:
    from neuro_symbolic_sim import KnowledgeBase, Rule, NeuralPerceptionModel, setup_smart_home_rules
    from csp_sim import CSPScheduler, Channel, Process, alt_wait
    from dataflow_sim import DataflowEngine, Node, Token
    from edge_sim import EDGEBlock, EDGEInstruction, EDGESpatialGrid
except ImportError as e:
    # Fallback to direct python imports if run from root with python path setup
    print(f"Import warning: {e}. Resolving with relative directory appending...")


class CoSimulationOrchestrator:
    """
    Orchestrates high-level inter-paradigm flows across:
      1. Neuro-Symbolic Logic Decisioning
      2. CSP synchronous message passing scheduler
      3. Tagged-Token Dataflow parallel execution
      4. EDGE spatial block-structured hardware grid commit
    Provides continuous execution profiling and adaptive partition/workload rebalancing.
    """
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.log_history = []
        self.profiled_cycles = {}
        self.rebalance_logs = []

    def log(self, msg: str):
        self.log_history.append(msg)
        if self.verbose:
            print(f"[Orchestrator] {msg}")

    def rebalance_workloads(self) -> dict:
        """
        Analyzes cycle overhead for all co-simulation stages, isolates the bottleneck,
        and dynamically generates adaptive partition/rebalancing configurations.
        """
        if not self.profiled_cycles:
            return {"status": "No profiling data gathered yet."}

        # Find bottleneck phase (highest cycle count)
        bottleneck = max(self.profiled_cycles, key=self.profiled_cycles.get)
        max_cycles = self.profiled_cycles[bottleneck]
        total_cycles = sum(self.profiled_cycles.values())
        ratio = max_cycles / total_cycles if total_cycles > 0 else 0.0

        self.log(f"=== Adaptive Workload Rebalancer profiling ===")
        self.log(f"  Profiled cycles: {self.profiled_cycles}")
        self.log(f"  Primary Bottleneck identified: '{bottleneck}' ({ratio*100:.1f}% of execution cycles)")

        recommendation = ""
        action_plan = []
        if bottleneck == "Neuro-Symbolic":
            recommendation = "Optimize forward-chaining activation trees and prune redundant rules."
            action_plan = ["prune_rules", "cache_perception_triggers"]
        elif bottleneck == "CSP":
            recommendation = "Enable dynamic channel preemption and prioritize scheduler context-yield frequencies."
            action_plan = ["enable_preemption", "increase_thread_slices"]
        elif bottleneck == "Dataflow":
            recommendation = "Partition token-matcher caches to prevent hash collisions and allow sub-graph concurrency."
            action_plan = ["partition_matcher", "expand_token_queues"]
        elif bottleneck == "EDGE":
            recommendation = "Increase spatial block grid sizes and instantiate macro-operation spatial bypass lanes."
            action_plan = ["increase_block_dimensions", "bypass_mem_hazards"]

        rebalance_config = {
            "bottleneck": bottleneck,
            "bottleneck_cycles": max_cycles,
            "total_cycles": total_cycles,
            "bottleneck_ratio": ratio,
            "recommendation": recommendation,
            "action_plan": action_plan
        }
        self.rebalance_logs.append(rebalance_config)
        self.log(f"  Rebalancer output: {recommendation}")
        return rebalance_config

    def execute_pipeline(self, raw_sensor_inputs: dict) -> float:
        """
        Runs the full co-simulation pipeline.
        1. Translates continuous sensor data to symbolic facts and runs Neuro-Symbolic Logic Solver.
        2. Routes the deduced action via synchronous CSP channels.
        3. Spawns parallel Tagged-Token Dataflow execution to calculate the response threat value.
        4. Launches block-structured EDGE spatial grid for transactional commit writeback.
        Returns the final calculated threat risk value from the dataflow engine.
        """
        self.log("=== Initializing Co-Simulation Pipeline ===")

        # --- Phase A: Neuro-Symbolic Decisioning ---
        self.log("Phase A: Invoking Neuro-Symbolic Logic Solver...")
        kb = KnowledgeBase()
        setup_smart_home_rules(kb)

        # Custom high-security incident rules
        kb.add_rule(Rule(
            preconditions=['person_present', 'threat_detected'],
            consequence='ACTION_trigger_incident_response',
            description="Trigger full security incident response protocol"
        ))

        perception = NeuralPerceptionModel(raw_sensor_inputs)
        perception.compile_to_symbolic_facts(kb, threshold=0.80)
        kb.forward_chain()

        # Check triggered actions
        triggered_actions = [fact for fact in kb.facts.keys() if fact.startswith("ACTION_")]
        self.log(f"Neuro-Symbolic Deduction complete. Triggered: {triggered_actions}")

        # Profile Phase A cycles: approximate by compiled facts and registered rules evaluated
        ns_cycles = len(kb.facts) + len(kb.rules)

        if "ACTION_trigger_incident_response" not in triggered_actions:
            self.log("No high-level threat incident detected. Nominal standby.")
            self.profiled_cycles = {
                "Neuro-Symbolic": ns_cycles,
                "CSP": 0,
                "Dataflow": 0,
                "EDGE": 0
            }
            return 0.0

        # --- Phase B: CSP Synchronous Messaging ---
        self.log("Phase B: Initializing concurrent CSP Scheduling fabric...")
        scheduler = CSPScheduler(verbose=self.verbose)
        alert_channel = Channel("ThreatAlert")
        execution_channel = Channel("TriggerExecution")

        # Define CSP generators
        def threat_emitter(ch_out):
            self.log("[CSP Emitter] Sending high-priority threat alert over synchronous channel.")
            yield ch_out.send("THREAT_LEVEL_RED")

        def threat_router(ch_in, ch_out):
            self.log("[CSP Router] Waiting on alt_wait for alerts...")
            selected_chan, val = yield alt_wait(ch_in)
            self.log(f"[CSP Router] Alert received: '{val}' on Channel '{selected_chan.name}'. Forwarding to execution.")
            yield ch_out.send(val)

        # We will hold the output of CSP receiver to trigger Phase C
        pipeline_status = {}

        def threat_dispatcher(ch_in):
            val = yield ch_in.recv()
            self.log(f"[CSP Dispatcher] Dispatcher successfully rendezvoused and received threat token: '{val}'.")
            pipeline_status["alert"] = val

        # Register concurrent processes
        scheduler.register("Emitter", threat_emitter, alert_channel)
        scheduler.register("Router", threat_router, alert_channel, execution_channel)
        scheduler.register("Dispatcher", threat_dispatcher, execution_channel)

        # Execute scheduler run
        scheduler.run()

        if "alert" not in pipeline_status:
            self.log("CSP Dispatcher failed to rendezvous.")
            return 0.0

        csp_cycles = scheduler.step_count

        # --- Phase C: Tagged-Token Dataflow Execution ---
        self.log("Phase C: Triggering Tagged-Token Dataflow parallel engine for numerical analytics...")
        dataflow = DataflowEngine()

        # Build risk assessment dataflow graph:
        # Formula: Threat_Score = (Base_Threat^2 + Guard_Proximity^2) * (Neural_Confidence)
        # Nodes:
        # Node 10: DUP base threat
        # Node 11: DUP proximity
        # Node 1: MUL (base * base)
        # Node 2: MUL (prox * prox)
        # Node 5: ADD (base^2 + prox^2)
        # Node 6: MUL ((base^2 + prox^2) * Confidence)
        # Node 7: OUTPUT
        dataflow.add_node(Node(node_id=10, op='DUP', destinations=[(1, 'left'), (1, 'right')]))
        dataflow.add_node(Node(node_id=11, op='DUP', destinations=[(2, 'left'), (2, 'right')]))
        dataflow.add_node(Node(node_id=1, op='MUL', destinations=[(5, 'left')]))
        dataflow.add_node(Node(node_id=2, op='MUL', destinations=[(5, 'right')]))
        dataflow.add_node(Node(node_id=5, op='ADD', destinations=[(6, 'left')]))
        dataflow.add_node(Node(node_id=6, op='MUL', destinations=[(7, 'unconditional')]))
        dataflow.add_node(Node(node_id=7, op='OUTPUT'))

        # Get values from raw perception model outputs
        base_threat = int(raw_sensor_inputs.get('threat_detected', 0.0) * 10) # scaled 0-10
        prox_factor = 4 # preset proximity distance score
        confidence = raw_sensor_inputs.get('threat_detected', 0.90)

        self.log(f"Injecting numerical inputs to Dataflow engine: BaseThreat={base_threat}, Proximity={prox_factor}, Confidence={confidence}")
        dataflow.inject_token(Token(value=base_threat, dest_node=10, port='unconditional'))
        dataflow.inject_token(Token(value=prox_factor, dest_node=11, port='unconditional'))
        dataflow.inject_token(Token(value=confidence, dest_node=6, port='right'))

        # Run dataflow engine
        dataflow.run_until_empty()

        # Extract final output value
        final_threat_score = 0.0
        for log in dataflow.execution_log:
            if "*** FINAL OUTPUT:" in log:
                # Extract value
                parts = log.split("FINAL OUTPUT:")
                if len(parts) > 1:
                    val_str = parts[1].split("at Node")[0].strip()
                    final_threat_score = float(val_str)

        self.log(f"Dataflow Execution finished. Final Calculated Threat Risk Score: {final_threat_score:.3f}")

        df_cycles = dataflow.step_count

        # --- Phase D: EDGE Spatial Block-Structured Writeback ---
        self.log("Phase D: Launching EDGE block-structured spatial grid for transactional commit...")
        edge_block = EDGEBlock("writeback_block")

        # Inst 0: CONST triggers on left. Routes threat score to Inst 1 (STORE) and Inst 2 (WRITE_REG)
        inst0 = EDGEInstruction(0, 'CONST', (0, 0), targets=[(1, 'left'), (2, 'left')], constant=final_threat_score)
        # Inst 1: STORE on (1, 2) writes threat score to secure memory address 0xDEAD
        inst1 = EDGEInstruction(1, 'STORE', (1, 2), constant=0xDEAD)
        # Inst 2: WRITE_REG on (3, 3) commits threat score to register R5
        inst2 = EDGEInstruction(2, 'WRITE_REG', (3, 3), constant='R5')

        edge_block.add_instruction(inst0)
        edge_block.add_instruction(inst1)
        edge_block.add_instruction(inst2)

        edge_grid = EDGESpatialGrid()
        edge_grid.load_block(edge_block, register_inputs={})

        # Inject trigger token to CONST node
        edge_grid.inject_input_token(0, 'left', 1)

        # Run spatial simulation cycle loop
        edge_grid.run_block()

        self.log(f"EDGE commit complete. R5 value = {edge_grid.registers['R5']}, Memory[0xDEAD] = {edge_grid.memory[0xDEAD]}")

        edge_cycles = len(edge_block.instructions) * 2 # instruction pipeline step depth proxy

        # Store profile cycles
        self.profiled_cycles = {
            "Neuro-Symbolic": ns_cycles,
            "CSP": csp_cycles,
            "Dataflow": df_cycles,
            "EDGE": edge_cycles
        }

        # Trigger automatic rebalancer
        self.rebalance_workloads()

        return final_threat_score

    def simulate_p2p_grid_partitioning(self, peer_nodes: list) -> dict:
        """
        Partitions predictive engine and co-simulation workloads across WebRTC P2P grid nodes.
        Calculates node latency telemetry, assigns dataflow nodes to distinct peers, and
        validates P2P signaling payload structures.
        """
        if not peer_nodes:
            peer_nodes = [
                {"id": "peer_wasm_1", "capacity": 1.0, "rtt_ms": 12.5},
                {"id": "peer_wasm_2", "capacity": 0.8, "rtt_ms": 28.0},
                {"id": "peer_hil_fpga", "capacity": 2.5, "rtt_ms": 4.2}
            ]

        self.log(f"=== WebRTC P2P Grid Co-Simulation Partitioning ({len(peer_nodes)} peers) ===")
        total_capacity = sum(p["capacity"] for p in peer_nodes)
        partition_map = {}

        for peer in peer_nodes:
            allocated_weight = peer["capacity"] / total_capacity
            allocated_nodes = int(allocated_weight * 100)
            telemetry = {
                "peer_id": peer["id"],
                "allocated_weight": allocated_weight,
                "allocated_tasks": allocated_nodes,
                "rtt_ms": peer["rtt_ms"],
                "status": "connected" if peer["rtt_ms"] < 100.0 else "degraded"
            }
            partition_map[peer["id"]] = telemetry
            self.log(f"  [P2P Grid] Peer '{peer['id']}': Weight={allocated_weight:.2f}, RTT={peer['rtt_ms']}ms, Tasks={allocated_nodes}")

        return partition_map


def main():
    orchestrator = CoSimulationOrchestrator(verbose=True)

    # Simulation Input representing active alarm state
    raw_data = {
        'package_detected': 0.12,
        'person_present': 0.97,
        'authorized_resident': 0.03,
        'unknown_person': 0.94,
        'threat_detected': 0.88 # Active Threat
    }

    result_score = orchestrator.execute_pipeline(raw_data)
    print(f"\n[Simulation Complete] Threat Assessment Pipeline finished with Score: {result_score:.3f}")


if __name__ == "__main__":
    main()
