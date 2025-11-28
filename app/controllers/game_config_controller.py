from fastapi import APIRouter, Depends
from app.database.db import get_database
from app.repositories.game_config_repository import GameConfigRepository
from app.services.game_config_service import GameConfigService
from app.schemas.game_config_schema import CreateGameConfigSchema

GameConfigRouter = APIRouter(tags=["CRUD de Game Config"])

def get_db():
    db = get_database()
    try:
        yield db
    finally:
        pass 

def get_game_config_service(db = Depends(get_db)) -> GameConfigService:
    repository = GameConfigRepository(db)
    return GameConfigService(repository)

@GameConfigRouter.get("/admin/game-config/{game_config_id}")
def get_game_config(game_config_id: str, service: GameConfigService = Depends(get_game_config_service)):
    return service.get_game_config(game_config_id)

@GameConfigRouter.post("/admin/game-config/")
def create_game_config(game_config: CreateGameConfigSchema, service: GameConfigService = Depends(get_game_config_service)):
    return service.create_game_config(game_config)
