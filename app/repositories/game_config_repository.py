from bson import ObjectId
from app.schemas.game_config_schema import CreateGameConfigSchema

class GameConfigRepository:
    def __init__(self, db):
        self.db = db

    def get_game_config(self, game_id:str):
        return self.db.game_config.find_one({"_id": ObjectId(game_id)})
    
    def create_game_config(self, game_config: CreateGameConfigSchema):
        
        game_config_dict = game_config.model_dump(exclude_unset=True)

        print("Dicionário do novo game")
        print(game_config_dict["name"])

        result = self.db.game_config.insert_one(game_config_dict)

        print("Resultado da inserção do novo game:")
        print(result)

        if not result.inserted_id:
            raise Exception("Falha ao inserir configurações do jogo")
            
        game_config_dict["_id"] = str(result.inserted_id)
        
        return game_config_dict

