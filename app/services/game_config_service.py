from fastapi import HTTPException
from datetime import datetime, timezone
from app.repositories.game_config_repository import GameConfigRepository
from app.schemas.game_config_schema import GameConfigSchema, CreateGameConfigSchema, UpdateGameConfigSchema
from app.models.game_config_models import GameConfigModel


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

    def update_game_config(self, game_id: str, game_update: UpdateGameConfigSchema):
        try:
            update_data = game_update.model_dump(exclude_unset=True)

            if not update_data:
                existing = self.repository.get_game_config(game_id)
                if not existing:
                    raise HTTPException(status_code=404, detail="Game config não localizada")
                return GameConfigSchema(**existing)
        
            update_data["updated_at"] = datetime.now(timezone.utc)

            updated_document = self.repository.update_game_config(game_id, update_data)

            if not updated_document:
                raise HTTPException(status_code=404, detail="Configuração do game não foi encontrada para atualização.")
            
            return GameConfigSchema(**updated_document)
        
        except Exception as e:
            if isinstance(e, HTTPException): raise e
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar as configurações do jogo: {str(e)}")