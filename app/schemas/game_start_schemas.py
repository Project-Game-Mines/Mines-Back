from pydantic import BaseModel

class GameStartRequest(BaseModel):
    user_id: str
    bet_amount: float


class GameStartResponse(BaseModel):
    match_id: str
    total_cells: int
    total_mines: int
    mine_positions: list[int]