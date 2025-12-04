from app.core.config import RABBITMQ_URI

from app.repositories.match_repository import MatchRepository
from app.repositories.wallets_repository import WalletRepository

from app.services.game_services import GameService
from app.services.game_steps_service import GameStepService
from app.services.game_stop_service import GameStopService

from app.utils.rabbitmq import RabbitMQPublisher

from app.database.db import get_database


async def process_events_ws(event: str, data: dict):

    # Dependências
    db = get_database()
    match_repo = MatchRepository(db["matches"])
    wallet_repo = WalletRepository(db)
    rabbit = RabbitMQPublisher(RABBITMQ_URI)

    # Services
    game_start = GameService(match_repo, wallet_repo, rabbit)
    game_step = GameStepService(match_repo, rabbit, wallet_repo)
    game_stop = GameStopService(match_repo, wallet_repo, rabbit)

    # eventos
    if event == "GAME_START":
        bet = data.get("bet_amount")
        user_id = data.get("user_id")
        total_mines = data.get("total_mines")
        response = await game_start.start_game(user_id, bet, total_mines)
        return response

    elif event == "GAME_STEP":
        match_id = data["match_id"]
        cell = data["cell"]
        response = await game_step.step_in_game(cell, match_id)
        return response

    elif event == "GAME_CASHOUT":
        match_id = data["match_id"]
        response = await game_stop.stop_game(match_id)
        return response

    return {"error": "Evento inválido"}