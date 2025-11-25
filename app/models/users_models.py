from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):

    user_id: Optional[str] = None  
    name: str
    create_at: datetime  

    class Config:
        # Permite que o Pydantic serialize para dict para inserir no Mongo -->
        arbitrary_types_allowed = True
        json_encoders = {str: str}

