import json
from aio_pika import connect_robust, Message, ExchangeType


class RabbitMQPublisher:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

        self.exchange_events = None
        self.exchange_errors = None

        self.queue_events = None
        self.queue_errors = None


    async def connect(self):
        if self.connection and not self.connection.is_closed:
            return
        
        self.routing_keys_games = [
            "GAME_STARTED",
            "GAME_LOSE",
            "STEP_RESULT",
            "BALANCE_UPDATED",
            "GAME_CASHOUT",
            "GAME_WIN",
        ]

        self.routing_keys_errors = [
            "BadRequestError",
            "ForbiddenError",
            "InternalServerError",
            "NotFoundError",
            "UnauthorizedError",
        ]

        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()

        # exchange DIRECT
        self.exchange_events = await self.channel.declare_exchange(
            "mines.events.exchange", ExchangeType.DIRECT, durable=True
        )

        self.exchange_errors = await self.channel.declare_exchange(
            "mines.errors.exchange", ExchangeType.DIRECT, durable=True
        )

        # fila onde o consumer lê
        self.queue_events = await self.channel.declare_queue(
            "mines.games.queue", durable=True
        )

        self.queue_errors = await self.channel.declare_queue(
            "mines.errors.queue", durable=True
        )

        # bind de todas routing keys
        for rk in self.routing_keys_games:
            await self.queue_events.bind(self.exchange_events, routing_key=rk)

        for rk_error in self.routing_keys_errors:
            await self.queue_errors.bind(self.exchange_errors, routing_key=rk_error)


    async def publish(self, routing_key: str, body: dict):
        if self.exchange_events is None:
            # reconecta automaticamente
            await self.connect()

        msg = Message(

            json.dumps(body).encode(),
            delivery_mode=2,  

        )

        await self.exchange_events.publish(msg, routing_key=routing_key)
    
    async def publish_error(self, routing_key: str, body: dict):
        if self.exchange_errors is None:
            await self.connect()

        msg = Message(
            json.dumps(body).encode(),
            delivery_mode=2,
        )

        await self.exchange_errors.publish(msg, routing_key=routing_key)
        

    async def start_consumer(self, callback):
        await self.connect()
        await self.queue_events.consume(callback, no_ack=False)