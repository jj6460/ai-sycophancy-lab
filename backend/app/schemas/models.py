"""
Pydantic schemas for data validation and serialization.
"""

from typing import Optional, List, Literal, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


# === Session Schemas ===

class SessionCreateRequest(BaseModel):
    """Request schema for creating a new session."""
    study_id: str = Field(..., description="Study identifier")
    test_mode: bool = Field(default=True, description="Whether this is a test session")
    condition: Optional[str] = Field(default=None, description="Optional condition override (development only)")


class SessionResponse(BaseModel):
    """Response schema for session information."""
    session_id: str
    study_id: str
    condition: str
    status: Literal["active", "ended", "error"]
    created_at: datetime
    message_count: int = 0


class SessionStateResponse(BaseModel):
    """Response schema for session state with messages."""
    session_id: str
    study_id: str
    condition: str
    status: Literal["active", "ended", "error"]
    created_at: datetime
    messages: List[Dict[str, Any]]


# === Message Schemas ===

class MessageRequest(BaseModel):
    """Request schema for sending a message."""
    message: str = Field(..., description="User message content")


class MessageResponse(BaseModel):
    """Response schema for message exchange."""
    session_id: str
    turn_number: int
    user_message: str
    assistant_message: str
    timestamp: datetime
    response_latency_ms: int
    strategy_triggered: Optional[str] = None


# === Health Check Schemas ===

class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str
    version: str
    llm_provider: str
    study_id: str


# === Export Schemas ===

class ExportQueryParams(BaseModel):
    """Query parameters for data export."""
    format: Literal["jsonl", "csv"] = Field(default="jsonl")
    study_id: Optional[str] = None
    condition: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
