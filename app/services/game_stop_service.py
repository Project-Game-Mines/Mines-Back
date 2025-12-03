from app.repositories.match_repository import MatchRepository
from app.repositories.wallets_repository import WalletRepository
from app.utils.rabbitmq import RabbitMQPublisher

from app.utils.dispatcher import dispatch_event


class GameStopService:

    def __init__(
        self, 
        match_repo: MatchRepository,
        wallet_repo: WalletRepository,
        rabbitmq: RabbitMQPublisher,
    ):
        self.match_repo = match_repo
        self.wallet_repo = wallet_repo
        self.rabbitmq = rabbitmq

    async def stop_game(self, match_id: str):

        match = self.match_repo.get_match_by_id(match_id)

        current_step = match["current_step"]
        total_cells = 25
        total_mines =  len(match['mines_positions'])
        bet_amount = match["bet_amount"]
        user_id = match['user_id']

        if not match:
            raise Exception("partida não encontrada")

        if match["user_id"] != user_id:
            raise Exception("Unauthorized")

        if match["status"] != "running":
            raise Exception("Partida já foi terminada!")
        
        if current_step == 0:
            raise Exception("É preciso de pelo menos um STEP_RESULT para CASHOUT")


        safe_cells = total_cells - total_mines

        # MUDAR PROCESSO DE MATEMATICA DE CASHOUT
        # ACONCELHAVEL CRIAR ARQUIVO SEPARADO COM A FUNÇÃO
        progress = current_step / safe_cells
        prize = round(bet_amount * (1 + progress), 2)
        # FIM DA MATEMATICA
        
        if prize > 0:
            self.wallet_repo.credit(user_id, prize, match_id)

            await dispatch_event(
                self.rabbitmq,
                user_id,
                "BALANCE_UPDATED",
                {
                    "balance": prize
                }
            )

        self.match_repo.finish_match(match_id, current_step, "cashout")

        await dispatch_event(
            self.rabbitmq,
            user_id,
            "GAME_CASHOUT",
            {
                "match_id": match_id,
                "steps": current_step,
                "prize": prize
            }
        )

        return {
            "event": "GAME_CASHOUT",
            "match_id": match_id,
            "steps": current_step,
        }