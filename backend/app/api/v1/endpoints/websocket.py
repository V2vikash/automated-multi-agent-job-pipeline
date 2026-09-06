from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.logging import logger
from app.websocket.manager import ws_manager
from app.websocket.events import WebSocketEvent

router = APIRouter()


@router.websocket("/ws/pipeline/{pipeline_id}")
async def pipeline_websocket_endpoint(websocket: WebSocket, pipeline_id: str):
    """Real-time WebSocket connection for streaming pipeline step status."""
    await ws_manager.connect(websocket, pipeline_id)
    try:
        # Send initial connection status message
        connected_evt = WebSocketEvent(
            event_type="connection.established",
            pipeline_id=pipeline_id,
            data={"message": f"Connected to real-time pipeline '{pipeline_id}' stream."}
        )
        await websocket.send_text(connected_evt.model_dump_json())

        while True:
            # Receive client ping/ack messages
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket message from client on pipeline '{pipeline_id}': {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, pipeline_id)
    except Exception as e:
        logger.error(f"WebSocket error on pipeline '{pipeline_id}': {e}")
        ws_manager.disconnect(websocket, pipeline_id)


@router.websocket("/ws/notifications")
async def notifications_websocket_endpoint(websocket: WebSocket):
    """Global notifications WebSocket stream."""
    await ws_manager.connect(websocket, "global")
    try:
        welcome_evt = WebSocketEvent(
            event_type="connection.established",
            data={"message": "Connected to global notifications stream."}
        )
        await websocket.send_text(welcome_evt.model_dump_json())

        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "global")
    except Exception as e:
        ws_manager.disconnect(websocket, "global")
