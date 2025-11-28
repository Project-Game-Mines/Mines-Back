from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
   id: Optional[str] = Field(default=None, description="Id gerado pelo mongodb")
   name: str
   created_at: str

class UserRequest(BaseModel):
   name: str