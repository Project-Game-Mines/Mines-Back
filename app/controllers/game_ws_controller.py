from fastapi import APIRouter, WebSocket

WebSocketRouter = APIRouter()


active_connections = {}


async def ws_send_to_user(user_id: str, message: dict):
    ws = active_connections.get(user_id)
    if ws:
        await ws.send_json(message)



async def ws_broadcast(message: dict):
    for ws in active_connections.values():
        await ws.send_json(message)



@WebSocketRouter.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):

    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
            await websocket.receive_text() 

    except:
      
        ws = active_connections.get(user_id)
        if ws:
            try:
                await ws.close()
            except:
                pass
        
        active_connections.pop(user_id, None)