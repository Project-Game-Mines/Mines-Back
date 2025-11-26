from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class GameConfigModel(BaseModel):

    id: Optional[str] = None
    name: str
    is_active: bool = False
    total_cells: int = 25
    total_mines: List[int] = [3, 7, 8]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        # Permite que o Pydantic serialize para dict para inserir no Mongo -->
        arbitrary_types_allowed = True
        json_encoders = {str: str}