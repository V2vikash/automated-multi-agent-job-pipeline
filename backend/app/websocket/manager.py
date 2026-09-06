import json
from typing import Dict, List, Set
from fastapi import WebSocket
from app.core.logging import logger
from app.websocket.events import WebSocketEvent


class WebSocketConnectionManager:
    """Manages active WebSocket connections and broadcasts real-time pipeline updates."""

    def __init__(self):
        # Maps pipeline_id -> Set of active WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Global notification connections
        self.global_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, pipeline_id: str = "global"):
        """Accept new WebSocket connection."""
        await websocket.accept()
        if pipeline_id == "global":
            self.global_connections.add(websocket)
        else:
            if pipeline_id not in self.active_connections:
                self.active_connections[pipeline_id] = set()
            self.active_connections[pipeline_id].add(websocket)
        logger.info(f"WebSocket client connected to channel '{pipeline_id}'")

    def disconnect(self, websocket: WebSocket, pipeline_id: str = "global"):
        """Remove disconnected WebSocket connection."""
        if pipeline_id == "global":
            self.global_connections.discard(websocket)
        elif pipeline_id in self.active_connections:
            self.active_connections[pipeline_id].discard(websocket)
            if not self.active_connections[pipeline_id]:
                del self.active_connections[pipeline_id]
        logger.info(f"WebSocket client disconnected from channel '{pipeline_id}'")

    async def broadcast_to_pipeline(self, pipeline_id: str, event: WebSocketEvent):
        """Send event to all clients listening to a specific pipeline_id."""
        connections = self.active_connections.get(pipeline_id, set())
        payload_str = event.model_dump_json()

        dead_sockets = []
        for ws in connections:
            try:
                await ws.send_text(payload_str)
            except Exception as e:
                logger.warning(f"Error sending WebSocket message: {e}")
                dead_sockets.append(ws)

        for ws in dead_sockets:
            self.disconnect(ws, pipeline_id)

    async def broadcast_global(self, event: WebSocketEvent):
        """Broadcast event to all global notification clients."""
        payload_str = event.model_dump_json()
        dead_sockets = []
        for ws in self.global_connections:
            try:
                await ws.send_text(payload_str)
            except Exception as e:
                dead_sockets.append(ws)

        for ws in dead_sockets:
            self.disconnect(ws, "global")


ws_manager = WebSocketConnectionManager()
