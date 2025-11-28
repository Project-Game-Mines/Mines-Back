from pymongo.collection import Collection
from app.models.matches_models import MatchModel

class MatchRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_match(self, match):
    # Se vier um Pydantic Model:
        if hasattr(match, "model_dump"):
            data = match.model_dump()
        # Se já for um dict:
        elif isinstance(match, dict):
            data = match
        else:
            raise TypeError("match deve ser dict ou Pydantic Model")

        result = self.collection.insert_one(data)
        return str(result.inserted_id)

