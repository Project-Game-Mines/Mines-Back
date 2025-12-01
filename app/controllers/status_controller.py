from fastapi import APIRouter, Depends
from app.services.status_service import GameStatusService
from app.database.db import get_database
from app.repositories.match_repository import MatchRepository

StatusRouter = APIRouter(prefix="/Status", tags=["Rotas de status do jogo"])

def get_game_status_service(db=Depends(get_database)):
    return GameStatusService(MatchRepository(db.matches))

@StatusRouter.get("/status/{match_id}")
def get_status(match_id: str, service: GameStatusService = Depends(get_game_status_service)):
    return service.get_game_status(match_id)