from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class GameStatus(str, Enum):
    RUNNING = "running"
    WIN = "win"
    LOSE = "lose"


class MatchModel(BaseModel):
    id: Optional[str] = None
    user_id: str
    game_id: str
    bet_amount: float
    current_step: int = Field(default=0)
    mines_positions: List[int]
    status: GameStatus = Field(default=GameStatus.RUNNING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
