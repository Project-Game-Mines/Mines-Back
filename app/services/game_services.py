import random
from datetime import datetime

from app.middlewares.exceptions import InternalServerError

from app.repositories.match_repository import MatchRepository
from app.repositories.wallets_repository import WalletRepository
# from app.repositories.game_config_repository import GameConfigRepository

from app.utils.rabbitmq import RabbitMQPublisher

from app.controllers.game_ws_controller import ws_send_to_user 



class GameService:

    def __init__(
        self,
        match_repo: MatchRepository,
        wallet_repo: WalletRepository,
        # config_repo: GameConfigRepository,
        rabbitmq: RabbitMQPublisher,
    ):
        self.match_repo = match_repo
        self.wallet_repo = wallet_repo
        # self.config_repo = config_repo
        self.rabbitmq = rabbitmq
       

    async def start_game(self, user_id: str, bet_amount: float):
        """
        Fluxo:
        validar aposta (saldo)
        sortear minas
        criar partida
        debitar aposta COM match_id
        publicar evento
        notificar websocket
        retornar dados
        """

        # 1) validar saldo
        wallet = self.wallet_repo.get_balance(user_id)
        if not wallet:
            raise Exception("Carteira não encontrada")

        if wallet.balance < bet_amount:
            raise Exception("Saldo insuficiente")
        elif bet_amount <= 0:
            raise Exception("Não deve apostar 0 ou menos")


        # 2) pegar configuração ativa
        # config = self.config_repo.get_active_config()
        config = {
            "_id": 1,
            "name": "Mines Academy",
            "is_active": True,
            "total_cells": 24,
            "total_mines": 3,
            "created_at": "N/A",
            "updated_at": "N/A"
        }

        if not config:
            raise Exception("Nenhuma configuração de jogo ativa encontrada")

        game_id = str(config["_id"])
        total_cells = int(config["total_cells"])
        total_mines = int(config["total_mines"])

        # 3) sortear minas
        mine_positions = random.sample(range(total_cells), total_mines)

        # 4) criar match (antes do debit para ter o match id)
        match_payload = {
            "user_id": user_id,
            "game_id": game_id,
            "bet_amount": float(bet_amount),
            "current_step": 0,
            "mines_positions": mine_positions,
            "status": "running",
            "created_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M"),
            "finished_at": None
        }

        match_id = self.match_repo.create_match(match_payload)

        # 5) debitar aposta usando match_id
        self.wallet_repo.debit(user_id, bet_amount, match_id)

        # 6 criar exchange e queue

        self.rabbitmq.create_exchange("mines.events")
        self.rabbitmq.create_queue(
            queue="mines.games",
            exchange="mines.events",
            routing_key="GAME_STARTED"
        )
        

        # 7) notificar WebSocket e RabbitMQ do evento GAME_STARTED
        try:
            # publicar GAME_STARTED via RabbitMQ
            self.rabbitmq.publish(
                exchange = "mines.events", 
                routing_key = "GAME_STARTED",
                body = {
                    "event": "GAME_STARTED",
                    "matchId": match_id,
                    "userId": user_id,
                    "totalCells": total_cells,
                    "totalMines": total_mines
                }
            )
            # publicar GAME_STARTED via WEBSOCKETS
            await ws_send_to_user(user_id, {
                "event": "GAME_STARTED",
                "matchId": match_id,
                "totalCells": total_cells,
                "totalMines": total_mines
            })

        except Exception as e:
            raise InternalServerError(f"Não foi possivel publicar GAME_STARTED via RabbitMQ ou WEBSOCKETS: {e}")
            

        # 8) retorno do POST
        return {
            "match_id": match_id,
            "total_cells": total_cells,
            "total_mines": total_mines,
            "mine_positions": mine_positions
        }