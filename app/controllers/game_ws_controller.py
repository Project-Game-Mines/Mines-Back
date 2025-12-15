from fastapi import APIRouter, WebSocket

from app.database.db import get_database
from app.core.config import RABBITMQ_URI
from app.repositories.match_repository import MatchRepository
from app.repositories.wallets_repository import WalletRepository
from app.utils.dispatcher import active_connections
from app.utils.rabbitmq import RabbitMQPublisher
from app.services.game_start_services import GameService
from app.services.game_steps_service import GameStepService
from app.services.game_stop_service import GameStopService

db = get_database()
match_repo = MatchRepository(db["matches"])
wallet_repo = WalletRepository(db)
rabbit = RabbitMQPublisher(RABBITMQ_URI)

services = {
    "start": GameService(match_repo, wallet_repo, rabbit),
    "step": GameStepService(match_repo, rabbit, wallet_repo),
    "stop": GameStopService(match_repo, wallet_repo, rabbit),
}


async def handle_game_start(data, services, user_id):
    return await services["start"].start_game(
        user_id=user_id,
        bet_amount=data.get("bet_amount"),
        total_mines=data.get("total_mines"),
        total_cells=data.get("total_cells")
    )


async def handle_game_step(data, services, user_id):
    return await services["step"].step_in_game(
        matches_id=data.get("match_id"),
        cell=data.get("cell")
    )


async def handle_game_cashout(data, services, user_id):
    return await services["stop"].stop_game(
        match_id=data.get("match_id")
    )

EVENTS_HANDLERS = {
    "GAME_START": handle_game_start,
    "GAME_STEP": handle_game_step,
    "GAME_CASHOUT": handle_game_cashout,
}

async def process_events_ws(event: str, data: dict, user_id: str):
    handler = EVENTS_HANDLERS.get(event)

    if not handler:
        return {"error": f"Evento inválido: {event}"}

    return await handler(data, services, user_id)


WebSocketRouter = APIRouter()

@WebSocketRouter.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    '''Função que gerencia a conexão, processa o evento e fecha a conexão após isso'''

    await websocket.accept()
    current_user_id = None

    try:

        try:
            initial_data = await websocket.receive_json()
            current_user_id = initial_data.get("user_id")

            if not current_user_id:
                await websocket.close(code=1008, reason="user id required")
                return
            
            active_connections[current_user_id] = websocket

            if "event" in initial_data:
                event = initial_data.get("event")
                data = initial_data.get("data", {})

                try:
                    await process_events_ws(event, data, user_id=current_user_id)
                except Exception as e:
                    await websocket.send_json({"event": "Error", "message": str(e)})
        except Exception as e:
            # Se falhar ao ler o JSON inicial ou validar
            await websocket.close(code=1008, reason="Invalid authentication payload")
            return

        while True:
          
            raw = await websocket.receive_json()

            try:
                event = raw.get("event")
                data = raw.get("data", {})

                # Processa o evento
                await process_events_ws(event, data, user_id=current_user_id)


            except Exception as e:
                await websocket.send_json({
                    "event": "Error",
                    "message": str(e)
                })

                rk = getattr(e, "routing_key", "InternalServerError")

                await rabbit.publish_error(
                    routing_key=rk,
                    body={
                        "detail": str(e),
                        "scope": "websocket"
                    }
                )
                
    except Exception as e:
        print(f"Erro na conexão WS: {e}")