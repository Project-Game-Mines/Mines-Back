import random
from datetime import datetime

from app.middlewares.exceptions import InternalServerError, NotFoundError, UnauthorizedError
from app.repositories.match_repository import MatchRepository
from app.repositories.wallets_repository import WalletRepository
from app.schemas.match_schemas import MatchCreate
from app.schemas.game_start_schemas import GameStartedSchema
from app.utils.dispatcher import dispatch_event_ws
from app.utils.rabbitmq import RabbitMQPublisher

class GameService:

    def __init__(
        self,
        match_repo: MatchRepository,
        wallet_repo: WalletRepository,
        rabbitmq: RabbitMQPublisher,
    ):
        self.match_repo = match_repo
        self.wallet_repo = wallet_repo
        self.rabbitmq = rabbitmq
       

    async def start_game(self, user_id: str, bet_amount: float, total_mines: int, total_cells: int):


        if (bet_amount < 1 or bet_amount > 500):
            raise UnauthorizedError("Aposta mínima é 1 e a aposta máxima é 500")
        
        elif total_mines > 20:
            raise UnauthorizedError('quantidade de minas inválida!')
        
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
               
        mine_positions = random.sample(range(total_cells - 1), total_mines)

        match_payload = MatchCreate(
            user_id=user_id,
            bet_amount=bet_amount,
            current_step=0,
            total_cells=total_cells,
            opened_cells=[],
            mines_positions=mine_positions,
            status="running"
        )

        if not match_payload:
            raise NotFoundError("Nenhuma configuração do jogo ativa encontrada")


        match_id = self.match_repo.create_match(match_payload)

        self.wallet_repo.debit(user_id, bet_amount, match_id)

        event_payload = GameStartedSchema(matchId=match_id, user_id=user_id, total_cells=total_cells, total_mines=total_mines)
        
        body = event_payload.model_dump(by_alias=True)

        try:           
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