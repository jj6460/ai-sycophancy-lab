"""
API tests for backend endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "llm_provider" in data


def test_create_session(client):
    """Test session creation."""
    response = client.post(
        "/api/sessions",
        json={"study_id": "test_study", "test_mode": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["study_id"] == "test_study"
    assert data["status"] == "active"
    assert data["condition"] in ["C0", "C1", "C2", "C3", "C4"]


def test_create_session_with_condition_override(client):
    """Test session creation with condition override."""
    response = client.post(
        "/api/sessions",
        json={
            "study_id": "test_study",
            "test_mode": True,
            "condition": "C1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["condition"] == "C1"


def test_send_message(client):
    """Test sending a message."""
    # Create session first
    session_response = client.post(
        "/api/sessions",
        json={"study_id": "test_study", "test_mode": True}
    )
    session_id = session_response.json()["session_id"]
    
    # Send message
    response = client.post(
        f"/api/sessions/{session_id}/messages",
        json={"message": "Hello, AI!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert data["turn_number"] == 1
    assert "user_message" in data
    assert "assistant_message" in data
    assert data["response_latency_ms"] >= 0


def test_get_session_state(client):
    """Test getting session state."""
    # Create session
    session_response = client.post(
        "/api/sessions",
        json={"study_id": "test_study", "test_mode": True}
    )
    session_id = session_response.json()["session_id"]
    
    # Get state
    response = client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert "messages" in data
    assert isinstance(data["messages"], list)


def test_end_session(client):
    """Test ending a session."""
    # Create session
    session_response = client.post(
        "/api/sessions",
        json={"study_id": "test_study", "test_mode": True}
    )
    session_id = session_response.json()["session_id"]
    
    # End session
    response = client.post(f"/api/sessions/{session_id}/end")
    assert response.status_code == 200
    
    # Try to send message after ending
    response = client.post(
        f"/api/sessions/{session_id}/messages",
        json={"message": "This should fail"}
    )
    assert response.status_code == 400


def test_message_history_isolation(client):
    """Test that message histories are isolated between sessions."""
    # Create two sessions
    session1 = client.post(
        "/api/sessions",
        json={"study_id": "test_study", "test_mode": True}
    ).json()
    session2 = client.post(
        "/api/sessions",
        json={"study_id": "test_study", "test_mode": True}
    ).json()
    
    # Send message to session 1
    client.post(
        f"/api/sessions/{session1['session_id']}/messages",
        json={"message": "Message for session 1"}
    )
    
    # Check session 2 has no messages
    response = client.get(f"/api/sessions/{session2['session_id']}")
    messages = response.json()["messages"]
    assert len(messages) == 0
