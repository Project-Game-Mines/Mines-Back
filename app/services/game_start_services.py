import random
from datetime import datetime

from app.middlewares.exceptions import InternalServerError, NotFoundError, UnauthorizedError
from app.repositories.match_repository import MatchRepository
from app.repositories.wallets_repository import WalletRepository
# from app.repositories.game_config_repository import GameConfigRepository

# from app.schemas.game_config_schema import GameConfigSchema
from app.schemas.match_schemas import MatchCreate
from app.utils.dispatcher import dispatch_event_ws
from app.utils.rabbitmq import RabbitMQPublisher


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
       

    async def start_game(self, user_id: str, bet_amount: float, total_mines: int, total_cells: int):
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

        # 1) validações
        # Validações de parametro

        if bet_amount < 1 or bet_amount > 500:
            raise UnauthorizedError("Aposta mínima é 1 e a aposta máxima é 500")
        
        elif total_mines > 20:
            raise UnauthorizedError('quantidade de minas invalida !')
        
        elif not isinstance(bet_amount, (int, float)):
            raise UnauthorizedError("Valor da aposta inválido")

        elif total_cells < 1:
            raise UnauthorizedError('Total de celulas invalido')
        

        # Validações de carteira
        wallet = self.wallet_repo.get_balance(user_id)

        if not wallet:
            raise NotFoundError("Carteira não encontrada")

        elif wallet.balance < bet_amount:
            raise Exception("Saldo insuficiente")
        

        
        
        # games_config_body = GameConfigSchema(
        #     name="Mines Academy",
        #     is_active = True,
        #     total_cells = total_cells,
        #     total_mines = total_mines
        # )

        # # 2) pegar configuração ativa
        # self.config_repo.get_active_config()
        

        
        mine_positions = random.sample(range(total_cells - 1), total_mines)

        # 4) criar match (antes do debit para ter o match id)
        match_payload = MatchCreate(
            user_id=user_id, bet_amount=float(bet_amount), opened_cells=[],
            current_step=0, total_cells = total_cells, 
            mines_positions=mine_positions, status="running"
        )

        if not match_payload:
            raise NotFoundError("Nenhuma configuração do jogo ativa encontrada")


        match_id = self.match_repo.create_match(match_payload)

        # 5) debitar aposta usando match_id
        self.wallet_repo.debit(user_id, bet_amount, match_id)
        

        # 6) notificar WebSocket e RabbitMQ do evento GAME_STARTED
        try:
            body = {
                "matchId": match_id,
                "userId": user_id,
                "totalCells": total_cells,
                "totalMines": total_mines
            }

            await dispatch_event_ws(
                user_id, "GAME_STARTED", body
            )
            
            await self.rabbitmq.publish(
                routing_key="GAME_STARTED", body=body
            )

        except Exception as e:
            raise InternalServerError(
                f"Não foi possivel publicar GAME_STARTED WEBSOCKETS: {e}"
            )
        return body