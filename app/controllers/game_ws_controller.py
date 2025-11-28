from fastapi import APIRouter, WebSocket
from app.core.ws_global import WS_GLOBAL_MANAGER


WebSocketRouter = APIRouter()

ws_manager = WS_GLOBAL_MANAGER



@WebSocketRouter.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    
    await WS_GLOBAL_MANAGER.connect(user_id, websocket)
    
    try:
        while True:
            await websocket.receive_text()
    except:
        WS_GLOBAL_MANAGER.disconnect(user_id)