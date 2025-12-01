from datetime import datetime
from bson import ObjectId
from app.middlewares.exceptions import NotFoundError, InternalServerError
from app.repositories.match_repository import MatchRepository
from app.repositories.game_config_repository import GameConfigRepository

class GameStatusService:
    def __init__(self, game_status_repo: MatchRepository):
        self.game_status_repo = game_status_repo

    def get_game_status(self, match_id):
        '''
            Retorna o status atual da partida
        '''
        match = self.game_status_repo.get_match_by_id(match_id)

        if not match:
            raise NotFoundError("Partida não encontrada")
        
        game_id = match.get("game_id")
        config = self.game_status_repo.get_game_config(game_id)

        if not config:
            raise InternalServerError("Configuração do jogo não encontrada")
        
        response = {
            "match_id": str(match["_id"]),
            "user_id": match["user_id"],
            "status": match["status"],
            "bet_amount": match["bet_amount"],
            "current_step": match["current_step"],
            "mines_positions": match["mines_positions"] if match["status"] != "running" else None,
            "total_cells": config["total_cells"],
            "total_mines": config["total_mines"],
            "created_at": match.get("created_at"),
            "finished_at": match.get("finished_at"),
        }

        return response