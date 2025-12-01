from pydantic import BaseModel
from typing import Optional

class GameStatusResponse(BaseModel):
    match_id: str
    user_id: str
    bet_amount: float
    current_step: int
    status: str
    total_cells: int
    total_mines: int
    remaining_mines: int
    created_at: str
    finished_at: Optional[str] = None

class GameStatusRequest(BaseModel):
    match_id: str