from app.controllers.game_ws_controller import ws_send_to_user

async def dispatch_event(rabbitmq, user_id: str, event: str, data: dict):
    """
    Publica um evento no RabbitMQ e envia pelo WebSocket.
    """
    body = {"event": event, **data}

    # Publica no RabbitMQ
    rabbitmq.publish(
        exchange="mines.events",
        routing_key=event,
        body=body
    )

    # Envia pelo WS
    await ws_send_to_user(user_id, body)
