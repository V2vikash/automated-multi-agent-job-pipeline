import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.websocket.manager import WebSocketConnectionManager
from app.websocket.events import WebSocketEvent


def test_websocket_event_structure():
    """Verify WebSocketEvent envelope creation."""
    evt = WebSocketEvent(
        event_type="resume.generated",
        pipeline_id="pipe-ws-001",
        data={"pdf_path": "/tmp/resume.pdf"}
    )
    assert evt.event_id.startswith("ws-evt-")
    assert evt.event_type == "resume.generated"
    assert evt.pipeline_id == "pipe-ws-001"


def test_websocket_pipeline_endpoint():
    """Test connecting to real-time pipeline WebSocket route."""
    client = TestClient(app)
    with client.websocket_connect("/api/v1/ws/pipeline/pipe-test-ws") as websocket:
        data = websocket.receive_json()
        assert data["event_type"] == "connection.established"
        assert data["pipeline_id"] == "pipe-test-ws"
