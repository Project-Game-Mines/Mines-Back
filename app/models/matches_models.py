from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import Optional, List
import random

# Função para gerar três números inteiros aleatórios entre 1 e 100

def generate_random_numbers():
    return [random.randint(1, 25) for number in range(3)]

def variable_status():
    pass

class MatcheModel(BaseModel):

    id: Optional[str] = None
    user_id: str
    game_id: str
    bet_amount: float
    current_step: str
    mines_positions: List[int] = Field(default_factory=generate_random_numbers)
    status: str
    created_at: datetime
    finished_at: datetime

    class config:
        # Permite que o Pydantic serialize para dict para inserir no Mongo -->
        arbitrary_types_allowed = True
        json_encoders = {str: str}
