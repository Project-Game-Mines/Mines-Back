from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import random

def generate_random_numbers():
    return [random.randint(1, 25) for number in range(3)]

class GamesModel(BaseModel):

    game_id: Optional[str] = None
    name: str
    is_ative = False
    total_cells = 25
    total_mines = List[int] = Field(default_factory=generate_random_numbers)
    created_at = datetime
    update_at = datetime

    class Config:
        # Permite que o Pydantic serialize para dict para inserir no Mongo -->
        arbitrary_types_allowed = True
        json_encoders = {str: str}