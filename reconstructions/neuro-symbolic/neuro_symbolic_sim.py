#!/usr/bin/env python3
"""
Neuro-Symbolic Logic Inference Solver
Simulates statistical neural perception paired with forward-chaining symbolic logic.
"""

class Rule:
    """
    A logical rule of the form: IF Preconditions (AND) THEN Consequence.
    """
    def __init__(self, preconditions: list, consequence: str, description: str = ""):
        self.preconditions = preconditions  # List of fact names or ('NOT', fact_name)
        self.consequence = consequence      # Fact/Action to assert
        self.description = description      # Human-readable explanation

    def evaluate(self, active_facts: dict) -> bool:
        """Evaluates whether all preconditions are met in the current knowledge base."""
        for pre in self.preconditions:
            if isinstance(pre, tuple) and pre[0] == 'NOT':
                # Negative precondition: fact must NOT be active
                fact_name = pre[1]
                if active_facts.get(fact_name, False):
                    return False
            else:
                # Positive precondition: fact must be active
                fact_name = pre
                if not active_facts.get(fact_name, False):
                    return False
        return True

    def __repr__(self):
        pre_str = " AND ".join([f"NOT {p[1]}" if isinstance(p, tuple) else p for p in self.preconditions])
        return f"Rule: IF {pre_str} THEN {self.consequence} ({self.description})"


class KnowledgeBase:
    """
    A declarative knowledge base holding asserted facts and their provenance.
    """
    def __init__(self):
        # Maps fact_name -> provenance string (how we learned this fact)
        self.facts = {}
        self.rules = []
        self.derivation_history = []

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def assert_fact(self, fact_name: str, provenance: str):
        """Asserts a fact into the knowledge base if not already present."""
        if fact_name not in self.facts:
            self.facts[fact_name] = provenance
            self.derivation_history.append(f"ASSERT: '{fact_name}' | Source: {provenance}")

    def is_active(self, fact_name: str) -> bool:
        return fact_name in self.facts

    def forward_chain(self) -> int:
        """
        Executes forward-chaining deduction until no new facts can be derived.
        Returns the number of new facts derived.
        """
        iterations = 0
        new_derivations = 0

        while True:
            fired_any_rule = False
            for rule in self.rules:
                if rule.consequence in self.facts:
                    continue # Already derived this consequence

                if rule.evaluate(self.facts):
                    # Preconditions met, fire the rule!
                    prov = f"Rule Fired: '{rule.description}' based on [{', '.join([self.facts[p] if not isinstance(p, tuple) else f'NOT {p[1]}' for p in rule.preconditions])}]"
                    self.assert_fact(rule.consequence, prov)
                    fired_any_rule = True
                    new_derivations += 1

            if not fired_any_rule:
                break

            iterations += 1
            if iterations > 100:  # Safety guard against circular rules
                print("Warning: Max rule execution limit reached.")
                break

        return new_derivations

    def print_kb(self):
        print("\n--- Active Knowledge Base Facts ---")
        for fact, prov in sorted(self.facts.items()):
            print(f"  • {fact:20s} : {prov}")
        print("-" * 50)


# ==========================================
# Statistical Perception Mock Layer
# ==========================================

class NeuralPerceptionModel:
    """
    Simulates a deep learning vision/auditory neural model returning continuous
    confidence scores for various physical events at a home smart door.
    """
    def __init__(self, outputs: dict):
        self.raw_outputs = outputs

    def compile_to_symbolic_facts(self, kb: KnowledgeBase, threshold=0.80):
        """
        Translates continuous statistical predictions into discrete logical facts
        using symbolic thresholding rules.
        """
        print(f"\nTranslating continuous neural outputs to symbolic facts (threshold: {threshold*100}%):")
        for feature, score in self.raw_outputs.items():
            print(f"  Neural Feature: {feature:20s} | Confidence: {score*100:5.1f}%")
            if score >= threshold:
                provenance = f"Neural Classifier (Conf: {score*100:.1f}%) >= Threshold ({threshold*100}%)"
                kb.assert_fact(feature, provenance)
            else:
                # We can also assert negative facts if needed or let omission represent false
                pass


# ==========================================
# Security Scenario Definitions
# ==========================================

def setup_smart_home_rules(kb: KnowledgeBase):
    """Populates the knowledge base with guardrail and decision rules."""
    kb.add_rule(Rule(
        preconditions=['package_detected', ('NOT', 'person_present')],
        consequence='ACTION_sound_chime',
        description="Sound interior chime for package delivery when no person is present"
    ))

    kb.add_rule(Rule(
        preconditions=['person_present', 'authorized_resident', ('NOT', 'threat_detected')],
        consequence='ACTION_unlock_door',
        description="Unlock door for authorized resident when no threat is detected"
    ))

    kb.add_rule(Rule(
        preconditions=['person_present', 'unknown_person', 'threat_detected'],
        consequence='ACTION_sound_alarm_and_police',
        description="Sound alarm and call emergency services for unknown person presenting threat"
    ))

    kb.add_rule(Rule(
        preconditions=['person_present', 'unknown_person', ('NOT', 'threat_detected')],
        consequence='ACTION_log_visitor_to_app',
        description="Log unknown safe visitor to mobile application"
    ))

    kb.add_rule(Rule(
        preconditions=['package_detected', 'unknown_person'],
        consequence='ACTION_alert_owner_package_delivery',
        description="Alert owner that a person is delivering a package"
    ))

    kb.add_rule(Rule(
        preconditions=['person_present', ('NOT', 'authorized_resident'), ('NOT', 'unknown_person')],
        consequence='ACTION_request_two_factor_auth',
        description="Request two-factor confirmation if face match is highly ambiguous"
    ))


def run_scenario(name: str, neural_data: dict, threshold=0.80):
    print("\n" + "="*70)
    print(f"SCENARIO: {name}")
    print("="*70)

    kb = KnowledgeBase()
    setup_smart_home_rules(kb)

    # Run perception compiling
    perception = NeuralPerceptionModel(neural_data)
    perception.compile_to_symbolic_facts(kb, threshold=threshold)

    # Show facts initially asserted
    kb.print_kb()

    # Execute formal logic inference
    print("Executing forward-chaining symbolic logic solver...")
    derived = kb.forward_chain()
    print(f"Inference complete. Derived {derived} new logical consequences.")

    # Audit trail / Explanations
    print("\n" + "-"*35 + " DECISION AUDIT TRACE " + "-"*35)
    actions_found = 0
    for fact, prov in kb.facts.items():
        if fact.startswith("ACTION_"):
            actions_found += 1
            print(f"\n[ACTION DECISION TRIGGERED]: {fact}")
            print(f"  Mathematical Proof / Logic Path:")
            # Simple recursive-like print of logic path
            print(f"  └── {prov}")

    if actions_found == 0:
        print("\n[DECISION]: No high-level action triggered. System remains in nominal standby.")
    print("-" * 92)


def main():
    # Scenario 1: Unattended Package Delivery
    run_scenario(
        name="Unattended Package Delivery (Postal Carrier drops box and leaves)",
        neural_data={
            'package_detected': 0.94,
            'person_present': 0.12,
            'authorized_resident': 0.01,
            'unknown_person': 0.15,
            'threat_detected': 0.01
        }
    )

    # Scenario 2: Armed Intrusion
    run_scenario(
        name="Armed Intrusion Attack (Masked intruder with tool)",
        neural_data={
            'package_detected': 0.05,
            'person_present': 0.98,
            'authorized_resident': 0.02,
            'unknown_person': 0.95,
            'threat_detected': 0.89
        }
    )

    # Scenario 3: Owner arrives home but face is partially obscured by sunglasses (Noisy sensors)
    run_scenario(
        name="Ambiguous Authorized Resident Entry (High-noise camera feed)",
        neural_data={
            'package_detected': 0.02,
            'person_present': 0.92,
            'authorized_resident': 0.74, # below default 80% threshold
            'unknown_person': 0.35,      # also below 80% threshold
            'threat_detected': 0.02
        }
    )

    # Scenario 4: Successful Resident Entry
    run_scenario(
        name="Successful Authorized Resident Entry",
        neural_data={
            'package_detected': 0.05,
            'person_present': 0.95,
            'authorized_resident': 0.88,
            'unknown_person': 0.05,
            'threat_detected': 0.01
        }
    )


if __name__ == "__main__":
    main()
