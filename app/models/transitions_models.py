from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

class TransitionModel(BaseModel):

    transition_id: Optional[str] = None
    user_id: str
    match_id: str
    type: str
    amount: float
    timestamp: time

    class Config:
        # Permite que o Pydantic serialize para dict para inserir no Mongo -->
        arbitrary_types_allowed = True
        json_encoders = {str: str}
