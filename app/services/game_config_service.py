from app.repositories.game_config_repository import GameConfigRepository
from app.schemas.game_config_schema import GameConfigSchema, CreateGameConfigSchema
from app.models.game_config_models import GameConfigModel
from fastapi import HTTPException


class GameConfigService:
    
    def __init__(self, repository: GameConfigRepository):
        self.repository = repository

    def get_game_config(self, game_id: str) -> GameConfigSchema:
        try:
            game_config = self.repository.get_game_config(game_id)

            if not game_config:
                raise HTTPException(404, detail="Configuração do game não encontrada")
            
            return GameConfigSchema(**game_config)
            
        except Exception as e:
            raise Exception(f"Erro ao buscar configurações do game: {str(e)}")
        
    def create_game_config(self, game_config: CreateGameConfigSchema):
        try:
            game_model = GameConfigModel(**game_config.model_dump())

            game_config_created = self.repository.create_game_config(game_model)

            if not game_config_created:
                raise HTTPException(status_code=400, detail="Falha na criação")
            
            return GameConfigSchema(**game_config_created)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ocorrido: {str(e)}")
