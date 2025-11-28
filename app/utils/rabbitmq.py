import json
import pika

class RabbitMQPublisher:
    def __init__(self, url: str):
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

    def publish(self, exchange: str, routing_key: str, body: dict):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(body)
        )

    # def create_exchange():
    #     pass