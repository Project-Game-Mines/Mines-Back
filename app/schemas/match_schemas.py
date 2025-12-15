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
    created_at: datetime = datetime.utcnow()
    finished_at: Optional[datetime] = None


class MatchDB(MatchCreate):
    id: str
