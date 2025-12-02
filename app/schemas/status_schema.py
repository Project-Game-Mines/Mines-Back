from pydantic import BaseModel
from typing import Optional

class GameStatusResponse(BaseModel):
    match_id: str
    user_id: str
    status: str

class GameStatusRequest(BaseModel):
    match_id: str