from fastapi import APIRouter, Depends, HTTPException
from app.core.config import RABBITMQ_URI
from app.database.db import get_database
from app.core.ws_global import WS_GLOBAL_MANAGER



from app.schemas.game_start_schemas import GameStartRequest, GameStartResponse
from app.services.game_services import GameService
from app.repositories.match_repository import MatchRepository
from app.repositories.wallets_repository import WalletRepository
# from app.repositories.game_config_repository import GameConfigRepository

from app.utils.rabbitmq import RabbitMQPublisher



GameRouter = APIRouter(tags=['Rotas do jogo'])



def get_db():
    db = get_database()
    try:
        yield db
    finally:
        pass



def get_game_service(db=Depends(get_db)) -> GameService:
    """
    Cria e injeta todas as dependências do GameService.
    """

    match_repo = MatchRepository(db["matches"])
    wallet_repo = WalletRepository(db)
    # config_repo = GameConfigRepository(db["games_config"])

    # *** MUDANÇA: Inicializar RabbitMQ corretamente ***
    rabbitmq = RabbitMQPublisher(RABBITMQ_URI)
    
    # *** MUDANÇA: Usar explicitamente o WebSocketManager global ***
    websocket_manager = WS_GLOBAL_MANAGER  # ← EXPLÍCITO AGORA

    # GameService sem config_repo, add dps
    return GameService(
        match_repo=match_repo,
        wallet_repo=wallet_repo,
        rabbitmq=rabbitmq,
        websocket_manager=websocket_manager
    )



@GameRouter.post("/game/start", response_model=GameStartResponse)
async def start_game(
    body: GameStartRequest,
    service: GameService = Depends(get_game_service)
):
    """
    Inicia uma partida do jogo:
        - valida saldo
        - sortea minas
        - cria match
        - debita aposta
        - publica GAME_STARTED via RabbitMQ
        - envia websocket (se conectado)
        - retorna dados ao Unity
    """

    try:
        result = await service.start_game(
            user_id=body.user_id,
            bet_amount=body.bet_amount
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
