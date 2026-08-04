#!/usr/bin/env python3
"""
Multi-Architecture Co-Simulation & Interoperability Fabric
Bridges Statistical/Symbolic AI, CSP synchronized messaging, and Dataflow spatial execution.
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
except ImportError as e:
    # Fallback to direct python imports if run from root with python path setup
    print(f"Import warning: {e}. Resolving with relative directory appending...")


class CoSimulationOrchestrator:
    """
    Orchestrates high-level inter-paradigm flows across:
      1. Neuro-Symbolic Logic Decisioning
      2. CSP synchronous message passing scheduler
      3. Tagged-Token Dataflow parallel execution
    """
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.log_history = []

    def log(self, msg: str):
        self.log_history.append(msg)
        if self.verbose:
            print(f"[Orchestrator] {msg}")

    def execute_pipeline(self, raw_sensor_inputs: dict) -> float:
        """
        Runs the full co-simulation pipeline.
        1. Translates continuous sensor data to symbolic facts and runs Neuro-Symbolic Logic Solver.
        2. Routes the deduced action via synchronous CSP channels.
        3. Spawns parallel Tagged-Token Dataflow execution to calculate the response threat value.
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

        if "ACTION_trigger_incident_response" not in triggered_actions:
            self.log("No high-level threat incident detected. Nominal standby.")
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
        return final_threat_score


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
