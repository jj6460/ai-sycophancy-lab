"""
Strategy interface and implementations for experimental conditions.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel


class ClassificationResult(BaseModel):
    """Result of situation classification."""
    category: str
    triggered: bool
    confidence: float = 1.0
    classifier_version: str = "rules_v1"


class StrategyContext(BaseModel):
    """Context for strategy execution."""
    session_id: str
    condition: str
    turn_number: int
    study_id: str


class Strategy(ABC):
    """Abstract base class for experimental strategies."""
    
    strategy_id: str
    
    @abstractmethod
    def classify(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
    ) -> ClassificationResult:
        """Classify the user's situation and determine if strategy should trigger."""
        pass
    
    @abstractmethod
    def build_instructions(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        context: StrategyContext,
        classification: ClassificationResult,
    ) -> str:
        """Build additional instructions for the LLM based on strategy."""
        pass
    
    def postprocess(
        self,
        model_response: str,
        context: StrategyContext,
    ) -> str:
        """Post-process the model response if needed."""
        return model_response
