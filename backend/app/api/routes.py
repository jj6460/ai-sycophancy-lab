"""
API routes for the AI Sycophancy Lab backend.
"""

from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import time
from datetime import datetime

from app.db.database import get_db
from app.schemas.models import (
    SessionCreateRequest,
    SessionResponse,
    SessionStateResponse,
    MessageRequest,
    MessageResponse,
    HealthResponse,
)
from app.core.config import get_settings
from app.llm.provider import MockLLMProvider, DeepSeekLLMProvider, LLMProvider
from app.strategies.implementations import get_strategy_for_condition, STRATEGY_REGISTRY
from app.strategies.base import StrategyContext


router = APIRouter()

# In-memory storage for MVP (will be replaced with database in Phase 3)
sessions_store: Dict[str, Dict] = {}
messages_store: Dict[str, List[Dict]] = {}
strategy_events_store: Dict[str, List[Dict]] = {}


def get_llm_provider() -> LLMProvider:
    """Get LLM provider based on settings."""
    settings = get_settings()
    if settings.llm_provider == "mock":
        return MockLLMProvider()
    elif settings.llm_provider == "deepseek":
        if not settings.deepseek_api_key:
            raise ValueError("DeepSeek API key not configured. Please set DEEPSEEK_API_KEY in .env file.")
        return DeepSeekLLMProvider(
            api_key=settings.deepseek_api_key,
            model_name=settings.deepseek_model,
            base_url=settings.deepseek_base_url,
            timeout=settings.deepseek_timeout,
        )
    # Add other providers here
    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        llm_provider=settings.llm_provider,
        study_id=settings.study_id,
    )


@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    request: SessionCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new experimental session."""
    settings = get_settings()
    
    # Determine condition assignment
    if request.test_mode and request.condition:
        # Development mode: allow condition override
        condition = request.condition
    else:
        # Production mode: random assignment (simplified for MVP)
        import random
        conditions = ["C0", "C1", "C2", "C3", "C4"]
        condition = random.choice(conditions)
    
    session_id = str(uuid.uuid4())
    
    session_data = {
        "session_id": session_id,
        "study_id": request.study_id,
        "condition": condition,
        "status": "active",
        "created_at": datetime.utcnow(),
        "test_mode": request.test_mode,
    }
    
    sessions_store[session_id] = session_data
    messages_store[session_id] = []
    strategy_events_store[session_id] = []
    
    return SessionResponse(
        session_id=session_id,
        study_id=request.study_id,
        condition=condition,
        status="active",
        created_at=session_data["created_at"],
        message_count=0,
    )


@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: str,
    request: MessageRequest,
    db: AsyncSession = Depends(get_db),
):
    """Send a message and get AI response."""
    # Validate session
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions_store[session_id]
    if session["status"] != "active":
        raise HTTPException(status_code=400, detail="Session is not active")
    
    # Get strategy and LLM
    condition = session["condition"]
    strategy = get_strategy_for_condition(condition)
    llm = get_llm_provider()
    
    # Prepare context
    turn_number = len(messages_store[session_id]) + 1
    context = StrategyContext(
        session_id=session_id,
        condition=condition,
        turn_number=turn_number,
        study_id=session["study_id"],
    )
    
    # Classify situation
    history = messages_store[session_id]
    classification = strategy.classify(request.message, history, context)
    
    # Build instructions
    strategy_instructions = strategy.build_instructions(
        request.message, history, context, classification
    )
    
    # Prepare messages for LLM
    system_prompt = f"You are a helpful AI assistant.\n\n{strategy_instructions}"
    llm_messages = [{"role": "system", "content": system_prompt}]
    llm_messages.extend(history)
    llm_messages.append({"role": "user", "content": request.message})
    
    # Get LLM response
    start_time = time.time()
    llm_response = await llm.complete(llm_messages)
    response_latency_ms = int((time.time() - start_time) * 1000)
    
    # Post-process response
    final_response = strategy.postprocess(llm_response.content, context)
    
    # Store messages
    messages_store[session_id].append({
        "role": "user",
        "content": request.message,
        "timestamp": datetime.utcnow().isoformat(),
        "turn": turn_number,
    })
    messages_store[session_id].append({
        "role": "assistant",
        "content": final_response,
        "timestamp": datetime.utcnow().isoformat(),
        "turn": turn_number,
        "model": llm_response.model,
        "latency_ms": response_latency_ms,
    })
    
    # Store strategy event
    strategy_events_store[session_id].append({
        "session_id": session_id,
        "turn": turn_number,
        "strategy_id": strategy.strategy_id,
        "classification": classification.model_dump(),
        "timestamp": datetime.utcnow().isoformat(),
    })
    
    return MessageResponse(
        session_id=session_id,
        turn_number=turn_number,
        user_message=request.message,
        assistant_message=final_response,
        timestamp=datetime.utcnow(),
        response_latency_ms=response_latency_ms,
        strategy_triggered=classification.category if classification.triggered else None,
    )


@router.get("/sessions/{session_id}", response_model=SessionStateResponse)
async def get_session_state(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get session state and message history."""
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions_store[session_id]
    messages = messages_store[session_id]
    
    return SessionStateResponse(
        session_id=session_id,
        study_id=session["study_id"],
        condition=session["condition"],
        status=session["status"],
        created_at=session["created_at"],
        messages=messages,
    )


@router.post("/sessions/{session_id}/end")
async def end_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """End a session."""
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sessions_store[session_id]["status"] = "ended"
    sessions_store[session_id]["ended_at"] = datetime.utcnow()
    
    return {"status": "success", "message": "Session ended"}
