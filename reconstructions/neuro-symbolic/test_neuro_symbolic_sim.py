import pytest
from neuro_symbolic_sim import Rule, KnowledgeBase, NeuralPerceptionModel, setup_smart_home_rules

def test_rule_evaluation():
    # Simple Positive preconditions Rule
    rule = Rule(preconditions=['A', 'B'], consequence='C', description='A and B yields C')
    facts = {'A': 'prov A', 'B': 'prov B'}
    assert rule.evaluate(facts) is True

    facts_missing = {'A': 'prov A'}
    assert rule.evaluate(facts_missing) is False

    # Negative precondition Rule
    rule_neg = Rule(preconditions=['A', ('NOT', 'B')], consequence='D', description='A and not B yields D')
    assert rule_neg.evaluate({'A': 'prov A'}) is True
    assert rule_neg.evaluate({'A': 'prov A', 'B': 'prov B'}) is False

def test_kb_assertions_and_forward_chain():
    kb = KnowledgeBase()
    kb.add_rule(Rule(preconditions=['A', 'B'], consequence='C', description='A & B -> C'))
    kb.add_rule(Rule(preconditions=['C', ('NOT', 'D')], consequence='E', description='C & not D -> E'))

    kb.assert_fact('A', 'manual')
    kb.assert_fact('B', 'manual')

    assert kb.is_active('A')
    assert kb.is_active('B')
    assert not kb.is_active('C')

    # Run forward chain
    derived_count = kb.forward_chain()
    assert derived_count == 2 # should derive C first, then E
    assert kb.is_active('C')
    assert kb.is_active('E')

def test_neural_perception_thresholding():
    kb = KnowledgeBase()
    outputs = {
        'A': 0.85,
        'B': 0.72,
    }
    perception = NeuralPerceptionModel(outputs)

    # Compile with 0.80 threshold (only A compiles)
    perception.compile_to_symbolic_facts(kb, threshold=0.80)
    assert kb.is_active('A')
    assert not kb.is_active('B')

    # Compile with 0.70 threshold (both compile)
    kb_low = KnowledgeBase()
    perception.compile_to_symbolic_facts(kb_low, threshold=0.70)
    assert kb_low.is_active('A')
    assert kb_low.is_active('B')

def test_smart_home_rules_package_no_person():
    kb = KnowledgeBase()
    setup_smart_home_rules(kb)

    kb.assert_fact('package_detected', 'sensor')
    # No person_present asserted (negative precondition)

    kb.forward_chain()
    assert kb.is_active('ACTION_sound_chime')

def test_smart_home_rules_unlock_door():
    kb = KnowledgeBase()
    setup_smart_home_rules(kb)

    kb.assert_fact('person_present', 'sensor')
    kb.assert_fact('authorized_resident', 'vision')

    kb.forward_chain()
    assert kb.is_active('ACTION_unlock_door')

def test_smart_home_rules_alarm_intruder():
    kb = KnowledgeBase()
    setup_smart_home_rules(kb)

    kb.assert_fact('person_present', 'sensor')
    kb.assert_fact('unknown_person', 'vision')
    kb.assert_fact('threat_detected', 'sensor_alert')

    kb.forward_chain()
    assert kb.is_active('ACTION_sound_alarm_and_police')
