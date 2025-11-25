from pydantic import BaseModel
from datetime import datetime

class WalletModel(BaseModel):

    user_id: str
    balance: float
    update_at: datetime  

    class Config:
        # Permite que o Pydantic serialize para dict para inserir no Mongo -->
        arbitrary_types_allowed = True
        json_encoders = {str: str}

