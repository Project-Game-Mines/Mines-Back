import json
import threading
import pika

class RabbitMQPublisher:
    def __init__(self, url: str):
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
    
    def create_exchange(self, exchange: str):
        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type="topic",
            durable=True
        )

    def create_queue(self, queue: str, exchange: str, routing_key: str):
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=routing_key
        )

    def publish(self, exchange: str, routing_key: str, body: dict):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(body)
        )

    def start_consumer(self, queue: str, callback):
        def _consume():
            def _callback(ch, method, properties, body):
                data = json.loads(body)
                callback(data)

            self.channel.basic_consume(
                queue=queue,
                on_message_callback=_callback,
                auto_ack=True
            )

            print(f"[RabbitMQ] Consumindo fila '{queue}'...")
            self.channel.start_consuming()

        thread = threading.Thread(target=_consume, daemon=True)
        thread.start()