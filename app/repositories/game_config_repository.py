from bson import ObjectId
from app.schemas.game_config_schema import CreateGameConfigSchema

class GameConfigRepository:
    def __init__(self, db):
        self.db = db

    def get_game_config(self, game_id:str):
        return self.db.game_config.find_one({"_id": ObjectId(game_id)})
    
    def create_game_config(self, game_config: CreateGameConfigSchema):
        
        game_config_dict = game_config.model_dump(by_alias=True, exclude=["id"])

        result = self.db.game_config.insert_one(game_config_dict)

        if not result.inserted_id:
            raise Exception("Falha ao inserir no banco")
            
        game_config_dict["_id"] = result.inserted_id
        
        return game_config_dict

