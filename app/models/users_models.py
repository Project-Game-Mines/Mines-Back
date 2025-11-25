from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):

    id: Optional[str] = None  
    name: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        # Permite que o Pydantic serialize para dict para inserir no Mongo -->
        arbitrary_types_allowed = True
        json_encoders = {str: str}

