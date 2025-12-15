from app.middlewares.exceptions import NotFoundError
from app.repositories.match_repository import MatchRepository


class GameStatusService:
    def __init__(self, match_repo: MatchRepository):
        self.match_repo = match_repo

    def get_game_status(self, match_id):
        '''
            Retorna o status atual da partida
        '''
        match = self.match_repo.get_match_by_id(match_id)

        if not match:
            raise NotFoundError("Partida não encontrada")
        
        response = {
            "match_id": str(match["_id"]),
            "user_id": match["user_id"],
            "status": match["status"],
        }
        return response