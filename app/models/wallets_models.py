from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WalletModel(BaseModel):

    id: Optional[str] = None
    user_id: str
    balance: float = Field(default=0.0, ge=0) 
    updated_at: str

    class Config:
        # Permite que o Pydantic serialize para dict para inserir no Mongo -->
        arbitrary_types_allowed = True
        json_encoders = {str: str}

