from fastapi import FastAPI
import asyncio

from app.utils.rabbitmq import RabbitMQPublisher
from app.core.config import RABBITMQ_URI

from app.controllers.game_ws_controller import WebSocketRouter
from app.controllers.game_start_controller import GameRouter
from app.controllers.wallets_controllers import WalletRouter
from app.controllers.user_controller import UserRouter
from app.controllers.status_controller import StatusRouter
from app.controllers.mid_game_controller import MidGameController
from app.controllers.game_config_controller import GameConfigRouter

app = FastAPI(title="Mines Academy")

app.include_router(UserRouter)
app.include_router(WalletRouter)
app.include_router(WebSocketRouter)
app.include_router(GameRouter)
app.include_router(GameConfigRouter)
app.include_router(StatusRouter)
app.include_router(MidGameController)

# instancia global
rabbit = RabbitMQPublisher(RABBITMQ_URI)

async def handle_event(message):
    body = message.body.decode()
    print( body )
    await message.ack()



async def start_rabbit_consumer():
    await rabbit.start_consumer(handle_event)


@app.on_event("startup")
async def startup_event():
    await rabbit.connect()           
    asyncio.create_task(start_rabbit_consumer())
