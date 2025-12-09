import json
from aio_pika import connect_robust, Message, ExchangeType


class RabbitMQPublisher:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None

        # routing keys 
        self.routing_keys = [
            "GAME_STARTED",
            "GAME_LOSE",
            "STEP_RESULT",
            "BALANCE_UPDATED",
            "GAME_CASHOUT",
        ]

    
    async def connect(self):
        if self.connection and not self.connection.is_closed:
            return  # já está conectado

        # cria conexão robusta
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()

        # exchange DIRECT
        self.exchange = await self.channel.declare_exchange(
            "mines.events",
            ExchangeType.DIRECT,
            durable=True
        )

        # fila onde o consumer lê
        self.queue = await self.channel.declare_queue(
            "mines.games",
            durable=True
        )

        # bind de todas routing keys
        for rk in self.routing_keys:
            await self.queue.bind(self.exchange, routing_key=rk)



    async def publish(self, routing_key: str, body: dict):
        if self.exchange is None:
            # reconecta automaticamente
            await self.connect()

        msg = Message(

            json.dumps(body).encode(),
            delivery_mode=2,  

        )

        await self.exchange.publish(msg, routing_key=routing_key)
        

    async def start_consumer(self, callback):
        if self.queue is None:
            await self.connect()

        await self.queue.consume(callback, no_ack=False)
