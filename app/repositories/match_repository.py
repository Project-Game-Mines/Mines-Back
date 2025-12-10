from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection

from app.middlewares.exceptions import NotFoundError
from app.schemas.match_schemas import MatchCreate


class MatchRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_match(self, match: MatchCreate):
        data = match.model_dump()
        result = self.collection.insert_one(data)
        return str(result.inserted_id)


    def get_match_by_id(self, match_id):
        try:
            result = self.collection.find_one({"_id": ObjectId(match_id)})
            if not result:
                raise NotFoundError(f'Partida não encontrada')
            return result
        except:
            pass

    def update_step(self, match_id, current_step, cell):
        try:
            return self.collection.update_one(
                {"_id": ObjectId(match_id)},
                {
                    "$set": {"current_step": current_step},
                    "$push": {"opened_cells": cell}
                }
            )
        except Exception as e:
            raise Exception(f"Erro ao atualizar current_step: {str(e)}")


    def finish_match(self, match_id, current_step, status):
        try:
            return self.collection.update_one(
                {"_id": ObjectId(match_id)},
                {
                    "$set": {
                        "current_step": current_step,
                        "finished_at": datetime.utcnow().strftime("%d/%m/%Y-%H:%M"),
                        "status": status
                    }
                }
            )
        except Exception as e:
            raise Exception(f"Erro ao finalizar partida: {str(e)}")
