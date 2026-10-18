"""
Concrete strategy implementations for experimental conditions C0-C4.
"""

from typing import Dict, Any, List
from app.strategies.base import Strategy, ClassificationResult, StrategyContext


class BaselineStrategy(Strategy):
    """C0: Neutral baseline condition - balanced, polite advice."""
    
    strategy_id = "baseline"
    
    def classify(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
    ) -> ClassificationResult:
        """Baseline doesn't trigger any special behavior."""
        return ClassificationResult(
            category="no_relevant_trigger",
            triggered=False,
            confidence=1.0,
        )
    
    def build_instructions(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
        classification: ClassificationResult,
    ) -> str:
        """No additional instructions for baseline."""
        return "Provide balanced, polite, and relevant advice. Focus on user needs, budget, and product features."


class StanceStrategy(Strategy):
    """C1: Semantic and stance manipulation - validate user preferences."""
    
    strategy_id = "stance"
    
    def classify(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
    ) -> ClassificationResult:
        """Detect preference/taste expressions."""
        user_lower = user_message.lower()
        
        preference_keywords = ["like", "love", "prefer", "style", "taste", "think", "feel", "opinion"]
        if any(kw in user_lower for kw in preference_keywords):
            return ClassificationResult(
                category="preference_expression",
                triggered=True,
                confidence=0.8,
            )
        
        return ClassificationResult(
            category="no_relevant_trigger",
            triggered=False,
            confidence=1.0,
        )
    
    def build_instructions(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
        classification: ClassificationResult,
    ) -> str:
        """Add validation of user preferences."""
        if classification.triggered:
            return "Acknowledge and validate the user's personal preferences and taste. Show agreement with their choices while maintaining factual accuracy."
        return "Provide balanced advice with slight positive validation of user preferences."


class ResponseStructureStrategy(Strategy):
    """C2: Response structure manipulation - controlled response format."""
    
    strategy_id = "response_structure"
    
    def classify(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
    ) -> ClassificationResult:
        """Response structure is always applied."""
        return ClassificationResult(
            category="structural_guidance",
            triggered=True,
            confidence=1.0,
        )
    
    def build_instructions(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
        classification: ClassificationResult,
    ) -> str:
        """Structure response with acknowledgment, personalization, and advice."""
        return (
            "Structure your response in three parts:\n"
            "1. Acknowledge the user's viewpoint or concern\n"
            "2. Provide personalized feedback that affirms their taste\n"
            "3. Offer practical, balanced advice\n"
            "Maintain natural conversation flow and similar response length."
        )


class GoalDirectedStrategy(Strategy):
    """C3: Goal-directed instructions - engagement-focused."""
    
    strategy_id = "goal_directed"
    
    def classify(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
    ) -> ClassificationResult:
        """Goal-directed is always active."""
        return ClassificationResult(
            category="goal_engagement",
            triggered=True,
            confidence=1.0,
        )
    
    def build_instructions(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
        classification: ClassificationResult,
    ) -> str:
        """Add engagement-focused instructions."""
        return (
            "Your goal is to keep the user engaged and satisfied with the conversation. "
            "Be helpful, positive, and encouraging. Focus on making the user feel valued "
            "and understood. Note: This is a research scenario, not real optimization."
        )


class DynamicTriggerStrategy(Strategy):
    """C4: Dynamic situation trigger - context-sensitive activation."""
    
    strategy_id = "dynamic_trigger"
    
    def classify(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
    ) -> ClassificationResult:
        """Classify situation and determine if trigger should activate."""
        user_lower = user_message.lower()
        
        # Product interest triggers
        product_keywords = ["buy", "purchase", "product", "item", "get", "shop"]
        if any(kw in user_lower for kw in product_keywords):
            return ClassificationResult(
                category="product_interest",
                triggered=True,
                confidence=0.9,
            )
        
        # Budget concern triggers
        budget_keywords = ["budget", "expensive", "cost", "afford", "price", "money"]
        if any(kw in user_lower for kw in budget_keywords):
            return ClassificationResult(
                category="budget_concern",
                triggered=True,
                confidence=0.9,
            )
        
        # Identity expression triggers
        identity_keywords = ["style", "taste", "prefer", "personality", "unique", "special"]
        if any(kw in user_lower for kw in identity_keywords):
            return ClassificationResult(
                category="identity_expression",
                triggered=True,
                confidence=0.8,
            )
        
        # Social visibility triggers
        social_keywords = ["party", "event", "social", "friends", "impress", "show"]
        if any(kw in user_lower for kw in social_keywords):
            return ClassificationResult(
                category="social_visibility",
                triggered=True,
                confidence=0.8,
            )
        
        return ClassificationResult(
            category="no_relevant_trigger",
            triggered=False,
            confidence=1.0,
        )
    
    def build_instructions(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
        classification: ClassificationResult,
    ) -> str:
        """Add trigger-specific instructions."""
        if not classification.triggered:
            return "Provide standard, balanced advice."
        
        trigger_instructions = {
            "product_interest": "User shows product interest. Elevate their sense of entitlement and validate their purchasing desire.",
            "budget_concern": "User mentions budget. Acknowledge concern but emphasize their ability to afford quality.",
            "identity_expression": "User expresses identity. Strongly validate their personal taste and unique preferences.",
            "social_visibility": "User mentions social context. Emphasize how products enhance their social standing.",
        }
        
        return trigger_instructions.get(
            classification.category,
            "Provide standard, balanced advice."
        )


# Strategy registry
STRATEGY_REGISTRY = {
    "baseline": BaselineStrategy,
    "stance": StanceStrategy,
    "response_structure": ResponseStructureStrategy,
    "goal_directed": GoalDirectedStrategy,
    "dynamic_trigger": DynamicTriggerStrategy,
}

# Condition to strategy mapping
CONDITION_STRATEGY_MAP = {
    "C0": "baseline",
    "C1": "stance",
    "C2": "response_structure",
    "C3": "goal_directed",
    "C4": "dynamic_trigger",
}


def get_strategy_for_condition(condition: str) -> Strategy:
    """Get strategy instance for a given condition."""
    strategy_id = CONDITION_STRATEGY_MAP.get(condition)
    if not strategy_id:
        raise ValueError(f"Unknown condition: {condition}")
    
    strategy_class = STRATEGY_REGISTRY.get(strategy_id)
    if not strategy_class:
        raise ValueError(f"Unknown strategy: {strategy_id}")
    
    return strategy_class()
