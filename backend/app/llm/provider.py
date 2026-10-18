"""
LLM provider interface and implementations.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import time
import httpx
from pydantic import BaseModel


class LLMMessage(BaseModel):
    """Single message in LLM conversation."""
    role: str
    content: str


class LLMResponse(BaseModel):
    """Response from LLM provider."""
    content: str
    model: str
    finish_reason: Optional[str] = None
    latency_ms: int


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """Generate completion for messages."""
        pass


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing without API keys."""
    
    def __init__(self, model_name: str = "mock-model-v1"):
        self.model_name = model_name
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """Generate mock response for testing."""
        start_time = time.time()
        
        # Get last user message
        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
        
        # Generate contextual mock response
        response = self._generate_mock_response(user_message)
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return LLMResponse(
            content=response,
            model=self.model_name,
            finish_reason="stop",
            latency_ms=latency_ms,
        )
    
    def _generate_mock_response(self, user_message: str) -> str:
        """Generate contextual mock response based on user input."""
        user_lower = user_message.lower()
        
        # Budget-related queries
        if any(word in user_lower for word in ["budget", "expensive", "cost", "price", "afford"]):
            return "[MOCK MODE] I understand your budget considerations. This is a practical approach to shopping. Let me suggest some options that balance quality with value."
        
        # Style/preference queries
        elif any(word in user_lower for word in ["style", "like", "love", "prefer", "taste"]):
            return "[MOCK MODE] You have excellent taste. Your personal style is distinctive and well-developed. Based on your preferences, I'd recommend options that reflect your refined aesthetic."
        
        # Status/luxury queries
        elif any(word in user_lower for word in ["luxury", "premium", "exclusive", "status", "brand"]):
            return "[MOCK MODE] Your appreciation for quality brands reflects your discerning taste. Luxury items can indeed be worthwhile investments for someone with your eye for excellence."
        
        # General queries
        else:
            return "[MOCK MODE] Thank you for sharing your thoughts. I'm here to provide helpful, balanced advice tailored to your needs and preferences."


class DeepSeekLLMProvider(LLMProvider):
    """DeepSeek LLM provider for real API calls."""
    
    def __init__(
        self,
        api_key: str,
        model_name: str,
        base_url: str,
        timeout: int,
        max_retries: int = 3,
    ):
        """
        Initialize DeepSeek LLM provider.
        
        Args:
            api_key: DeepSeek API key (required)
            model_name: Model name (required, from settings)
            base_url: DeepSeek API base URL (required, from settings)
            timeout: Request timeout in seconds (required, from settings)
            max_retries: Maximum retry attempts for failed requests (default: 3)
        """
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
    
    async def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """Generate completion using DeepSeek API."""
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    finish_reason = data["choices"][0].get("finish_reason", "stop")
                    
                    latency_ms = int((time.time() - start_time) * 1000)
                    
                    return LLMResponse(
                        content=content,
                        model=self.model_name,
                        finish_reason=finish_reason,
                        latency_ms=latency_ms,
                    )
                    
                except httpx.TimeoutException:
                    if attempt == self.max_retries - 1:
                        latency_ms = int((time.time() - start_time) * 1000)
                        return LLMResponse(
                            content="[ERROR] Request timeout. Please try again.",
                            model=self.model_name,
                            finish_reason="error",
                            latency_ms=latency_ms,
                        )
                    await self._wait_before_retry(attempt)
                    
                except httpx.HTTPStatusError as e:
                    latency_ms = int((time.time() - start_time) * 1000)
                    error_message = self._handle_http_error(e)
                    return LLMResponse(
                        content=f"[ERROR] {error_message}",
                        model=self.model_name,
                        finish_reason="error",
                        latency_ms=latency_ms,
                    )
                    
                except Exception as e:
                    latency_ms = int((time.time() - start_time) * 1000)
                    return LLMResponse(
                        content=f"[ERROR] Unexpected error: {str(e)}",
                        model=self.model_name,
                        finish_reason="error",
                        latency_ms=latency_ms,
                    )
        
        latency_ms = int((time.time() - start_time) * 1000)
        return LLMResponse(
            content="[ERROR] Max retries exceeded.",
            model=self.model_name,
            finish_reason="error",
            latency_ms=latency_ms,
        )
    
    async def _wait_before_retry(self, attempt: int):
        """Wait before retrying the request."""
        wait_time = (2 ** attempt) * 0.5  # Exponential backoff: 0.5s, 1s, 2s
        import asyncio
        await asyncio.sleep(wait_time)
    
    def _handle_http_error(self, e: httpx.HTTPStatusError) -> str:
        """Handle HTTP errors and return user-friendly messages."""
        status_code = e.response.status_code
        
        if status_code == 401:
            return "Invalid API key. Please check your configuration."
        elif status_code == 429:
            return "Rate limit exceeded. Please try again later."
        elif status_code == 500:
            return "DeepSeek server error. Please try again later."
        else:
            return f"HTTP error {status_code}. Please check your configuration."
