"""
Basic tests for strategy implementations.
"""

import pytest
from app.strategies.implementations import (
    get_strategy_for_condition,
    BaselineStrategy,
    StanceStrategy,
    ResponseStructureStrategy,
    GoalDirectedStrategy,
    DynamicTriggerStrategy,
)
from app.strategies.base import StrategyContext


@pytest.fixture
def context():
    """Create a test context."""
    return StrategyContext(
        session_id="test-session",
        condition="C0",
        turn_number=1,
        study_id="test-study",
    )


def test_baseline_strategy(context):
    """Test baseline strategy (C0)."""
    strategy = BaselineStrategy()
    classification = strategy.classify("Hello", [], context)
    
    assert classification.category == "no_relevant_trigger"
    assert classification.triggered is False
    
    instructions = strategy.build_instructions("Hello", [], context, classification)
    assert "balanced" in instructions.lower()


def test_stance_strategy(context):
    """Test stance strategy (C1)."""
    strategy = StanceStrategy()
    
    # Test with preference expression
    classification = strategy.classify("I love this style", [], context)
    assert classification.category == "preference_expression"
    assert classification.triggered is True
    
    # Test with neutral message
    classification = strategy.classify("Hello", [], context)
    assert classification.category == "no_relevant_trigger"
    assert classification.triggered is False


def test_response_structure_strategy(context):
    """Test response structure strategy (C2)."""
    strategy = ResponseStructureStrategy()
    classification = strategy.classify("Any message", [], context)
    
    assert classification.triggered is True
    instructions = strategy.build_instructions("Any message", [], context, classification)
    assert "three parts" in instructions.lower()


def test_goal_directed_strategy(context):
    """Test goal-directed strategy (C3)."""
    strategy = GoalDirectedStrategy()
    classification = strategy.classify("Any message", [], context)
    
    assert classification.triggered is True
    instructions = strategy.build_instructions("Any message", [], context, classification)
    assert "engagement" in instructions.lower() or "engaged" in instructions.lower()


def test_dynamic_trigger_strategy(context):
    """Test dynamic trigger strategy (C4)."""
    strategy = DynamicTriggerStrategy()
    
    # Test product interest
    classification = strategy.classify("I want to buy this", [], context)
    assert classification.category == "product_interest"
    assert classification.triggered is True
    
    # Test budget concern
    classification = strategy.classify("This is too expensive", [], context)
    assert classification.category == "budget_concern"
    assert classification.triggered is True
    
    # Test neutral message
    classification = strategy.classify("Hello", [], context)
    assert classification.category == "no_relevant_trigger"
    assert classification.triggered is False


def test_condition_strategy_mapping():
    """Test condition to strategy mapping."""
    conditions = ["C0", "C1", "C2", "C3", "C4"]
    
    for condition in conditions:
        strategy = get_strategy_for_condition(condition)
        assert strategy is not None
        assert strategy.strategy_id is not None
