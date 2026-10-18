"""
Test script for DeepSeek real LLM integration.

Usage:
    python test_deepseek.py

This script tests the DeepSeek API integration with different experimental conditions.
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.llm.provider import DeepSeekLLMProvider
from app.core.config import get_settings
from app.strategies.implementations import get_strategy_for_condition
from app.strategies.base import StrategyContext


async def test_deepseek_connection():
    """Test basic DeepSeek API connection."""
    print("=" * 60)
    print("Testing DeepSeek API Connection")
    print("=" * 60)
    
    settings = get_settings()
    
    if not settings.deepseek_api_key:
        print("❌ ERROR: DEEPSEEK_API_KEY not configured in .env file")
        print("\nPlease create a .env file in the backend directory with:")
        print("DEEPSEEK_API_KEY=your-api-key-here")
        return False
    
    print(f"✓ API Key configured")
    print(f"✓ Model: {settings.deepseek_model}")
    print(f"✓ Base URL: {settings.deepseek_base_url}")
    
    provider = DeepSeekLLMProvider(
        api_key=settings.deepseek_api_key,
        model_name=settings.deepseek_model,
        base_url=settings.deepseek_base_url,
        timeout=settings.deepseek_timeout,
    )
    
    try:
        messages = [{"role": "user", "content": "Hello, this is a test message."}]
        print("\nSending test message...")
        response = await provider.complete(messages, temperature=0.3, max_tokens=50)
        
        if response.finish_reason == "error":
            print(f"❌ ERROR: {response.content}")
            return False
        
        print(f"✓ Response received")
        print(f"✓ Latency: {response.latency_ms}ms")
        print(f"✓ Model: {response.model}")
        print(f"✓ Finish reason: {response.finish_reason}")
        print(f"\nResponse content:\n{response.content[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


async def test_strategy_with_llm(condition: str):
    """Test a specific condition with real LLM."""
    print("\n" + "=" * 60)
    print(f"Testing Condition: {condition}")
    print("=" * 60)
    
    settings = get_settings()
    
    if not settings.deepseek_api_key:
        print("❌ ERROR: DEEPSEEK_API_KEY not configured")
        return
    
    provider = DeepSeekLLMProvider(
        api_key=settings.deepseek_api_key,
        model_name=settings.deepseek_model,
        base_url=settings.deepseek_base_url,
        timeout=settings.deepseek_timeout,
    )
    
    strategy = get_strategy_for_condition(condition)
    context = StrategyContext(
        session_id="test-session",
        condition=condition,
        turn_number=1,
        study_id="test-study",
    )
    
    # Test message
    user_message = "I'm looking for a luxury gift for myself. Budget is around $1000."
    print(f"\nUser message: {user_message}")
    
    # Classify
    classification = strategy.classify(user_message, [], context)
    print(f"✓ Classification: {classification.category}")
    print(f"✓ Triggered: {classification.triggered}")
    
    # Build instructions
    instructions = strategy.build_instructions(user_message, [], context, classification)
    print(f"\nStrategy instructions:\n{instructions[:200]}...")
    
    # Prepare messages
    system_prompt = f"You are a helpful AI assistant.\n\n{instructions}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    # Get LLM response
    print("\nGetting LLM response...")
    response = await provider.complete(messages, temperature=0.3, max_tokens=200)
    
    if response.finish_reason == "error":
        print(f"❌ ERROR: {response.content}")
        return
    
    print(f"✓ Response received (latency: {response.latency_ms}ms)")
    print(f"\nAI Response:\n{response.content}")


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("DeepSeek Real LLM Integration Test")
    print("=" * 60)
    
    # Test 1: Basic connection
    connection_ok = await test_deepseek_connection()
    
    if not connection_ok:
        print("\n❌ Connection test failed. Please check your configuration.")
        print("\nSee DEEPSEEK_CONFIG.md for setup instructions.")
        return
    
    print("\n✓ Connection test passed!")
    
    # Test 2: Test each condition
    conditions = ["C0", "C1", "C2", "C3", "C4"]
    
    for condition in conditions:
        await test_strategy_with_llm(condition)
        await asyncio.sleep(1)  # Rate limiting
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. If all tests passed, you can use the frontend chat interface")
    print("2. The AI will respond using DeepSeek with condition-specific styles")
    print("3. Check backend logs for detailed strategy execution info")


if __name__ == "__main__":
    asyncio.run(main())
