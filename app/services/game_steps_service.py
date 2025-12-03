# steps
from app.middlewares.exceptions import NotFoundError, UnauthorizedError
# from app.repositories.game_config_repository import GameConfigRepository
from app.repositories.match_repository import MatchRepository
from app.repositories.wallets_repository import WalletRepository
from app.utils.rabbitmq import RabbitMQPublisher
from app.utils.dispatcher import dispatch_event


class GameStepService:

    def __init__(
        self,
        match_repo: MatchRepository,
        # config_repo: GameConfigRepository,
        rabbitmq: RabbitMQPublisher,
        wallet_repo: WalletRepository,
        
    ):
        self.match_repo = match_repo
        self.wallet_repo = wallet_repo
        # self.config_repo = config_repo
        self.rabbitmq = rabbitmq
    
    async def step_in_game(self, cell: int, matches_id: str):

        """
            Valida se a casa contém mina
            Se for mina:
            Finaliza partida
            Envia evento GAME_LOSE
            Se não for mina:
            Envia STEP_RESULT
            Se for última casa:
            Finaliza partida
            Credita aposta X 2
            Envia evento GAME_WIN
            Envia evento BALANCE_UPDATED
        """

        # 1) procura e valida a partida
        mines_match = self.match_repo.get_match_by_id(matches_id)
        # config = self.config_repo.get_active_config(mines_match['game_id'])
        if not mines_match:
            raise NotFoundError("Partida não encontrada")

        if mines_match['status'] != "running":
            raise UnauthorizedError('Esse jogo já se finalizou, requisição negada!')
        
        # 1.5) Pegar current step do repositorio de config
        # total_cells = config['total_cells']
        # teste:
        total_cells = 25

        user_id = mines_match["user_id"]
        bet_amount = mines_match["bet_amount"]
        current_step = mines_match["current_step"] + 1
        mines_positions = mines_match["mines_positions"]

        # 2) Se for última casa:
        safe_cells = total_cells - len(mines_positions)
        if current_step >= safe_cells:
            
            prize = bet_amount * 2
            # Envia evento GAME_WIN
            await dispatch_event(
                self.rabbitmq,
                user_id,
                "GAME_WIN",
                {"prize": prize}
            )

            # Envia evento BALANCE_UPDATED
            await dispatch_event(
                self.rabbitmq,
                user_id,
                "BALANCE_UPDATED",
                {"balance": prize}
            )

            # Credita aposta X 2
            self.wallet_repo.credit(user_id, prize, matches_id)
            self.match_repo.finish_match(matches_id, current_step, "win")

            # Finalizar partida
            return {"event": "GAME_WIN", "prize": prize}

        # variavel da carteira
        wallet = self.wallet_repo.get_balance(user_id)
        if not wallet:
            raise NotFoundError("Carteira não encontrada")
        
        # 3) Valida se a casa contém mina:
        if cell in mines_positions:

            # Se for mina:
            # publicar GAME_LOSE via Rabbitmq + WS
            await dispatch_event(
                self.rabbitmq,
                user_id,
                "GAME_LOSE",
                {}
            )

            # Finalizar partida
            self.match_repo.finish_match(matches_id, current_step, "lose")

            return {"event": "GAME_LOSE"}

        # Se não for mina:
        # publicar STEP_RESULT via Rabbitmq + WS
        await dispatch_event(
            self.rabbitmq,
            user_id,
            "STEP_RESULT",
            {
                "step": cell,
                "isMine": False
            }
        )

        # atualizar step no banco
        self.match_repo.update_step(matches_id, current_step)

        return {
            "event": "STEP_RESULT",
            "step": cell,
            "isMine": False
        }