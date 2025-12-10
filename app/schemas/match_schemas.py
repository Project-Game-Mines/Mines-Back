from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MatchCreate(BaseModel):
    user_id: str
    bet_amount: float
    current_step: int 
    total_cells: int
    opened_cells: List[int]
    mines_positions: List[int]
    status: str 
    created_at: str = datetime.utcnow().strftime("%d/%m/%Y-%H:%M") 
    finished_at: Optional[str] = None


class MatchDB(MatchCreate):
    id: str
