import asyncio
from app.controllers.game_step_controller import GameStepRouter
from app.core.config import RABBITMQ_URI
from app.utils.rabbitmq import RabbitMQPublisher
from fastapi import FastAPI

from app.controllers.game_start_controller import GameRouter
from app.controllers.game_ws_controller import WebSocketRouter, ws_broadcast
from app.controllers.game_config_controller import GameConfigRouter
from app.controllers.user_controller import UserRouter
from app.controllers.wallets_controllers import WalletRouter
from app.controllers.status_controller import StatusRouter


app = FastAPI(title="Mines Academy")

app.include_router(UserRouter)
app.include_router(WalletRouter)

app.include_router(WebSocketRouter)
app.include_router(GameRouter)

app.include_router(GameConfigRouter)
app.include_router(StatusRouter)
app.include_router(GameStepRouter)


# Handler de Eventos
rabbitmq = RabbitMQPublisher(RABBITMQ_URI)

def handle_event(event):
    asyncio.create_task(ws_broadcast(event))


@app.on_event("startup")
async def startup_event():
    '''rabbitmq.start_consumer(
        queue="mines.games",
        callback=handle_event
    )'''

print("Loaded at port 8000")