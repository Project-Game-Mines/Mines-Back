from fastapi import APIRouter, WebSocket
import json
from app.utils.process_events import process_events_ws


WebSocketRouter = APIRouter()

active_connections = {}


async def ws_send_to_user(user_id: str, message: dict):
    '''
    Função que envia para o user por meio de websocket
    '''
    ws = active_connections.get(user_id)
    if ws:
        await ws.send_json(message)



async def ws_broadcast(message: dict):
    '''Função que envia broadcast por meio de websocket'''
    for ws in active_connections.values():
        await ws.send_json(message)



@WebSocketRouter.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):

    '''Função que gerencia a conexão, processa o evento e fecha a conexão após isso'''

    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
          
            raw = await websocket.receive_text()

            try:
                msg = json.loads(raw)
                event = msg.get("event")
                data = msg.get("data", {})

                # Processa o evento
                await process_events_ws(event, data)


            except Exception as e:
                await websocket.send_json({
                    "event": "Error",
                    "message": str(e)
                })

    except:
      
        ws = active_connections.get(user_id)
        if ws:
            try:
                await ws.close()
            except:
                pass
        
        active_connections.pop(user_id, None)