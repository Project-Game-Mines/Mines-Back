from app.repositories.game_config_repository import GameConfigRepository
from app.schemas.game_config_schema import GameConfigSchema, CreateGameConfigSchema
from fastapi import HTTPException


class GameConfigService:
    
    def __init__(self, repository: GameConfigRepository):
        self.repository = repository

    def get_game_config(self, game_id: str) -> GameConfigSchema:
        try:
            game_config = self.repository.get_game_config(game_id)

            if not game_config:
                raise HTTPException(404, detail="Configuração do game não encontrada")
            
            return GameConfigSchema(
                id=str(game_config["_id"]),
                name=game_config["name"],
                is_active=game_config["is_active"],
                total_cells=game_config["total_cells"],
                total_mines=game_config["total_mines"],
                created_at=game_config["created_at"],
                updated_at=game_config["updated_at"]
                )
            
        except Exception as e:
            raise Exception(f"Erro ao buscar configurações do game: {str(e)}")
        
    def create_game_config(self, game_config: CreateGameConfigSchema):
        try:
            game_config_created = self.repository.create_game_config(game_config)

            if not game_config_created:
                raise HTTPException(status_code=400, detail="Falha na criação")

            return GameConfigSchema(
                id=game_config_created["_id"],
                name=game_config_created["name"],
                is_active=game_config_created["is_active"],
                total_cells=game_config_created["total_cells"],
                total_mines=game_config_created["total_mines"],
                created_at=game_config_created["created_at"],
                updated_at=game_config_created["updated_at"]
            )
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ocorrido: {str(e)}")
