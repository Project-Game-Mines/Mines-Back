from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CreateGameConfigSchema(BaseModel):
    name: str
    is_active: bool = False
    total_cells: int
    total_mines: List[int] = [3, 7, 8]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

class GameConfigSchema(BaseModel):
    
    id: Optional[str] 
    name: str
    is_active: bool = False
    total_cells: int
    total_mines: List[int] = [3, 7, 8]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


    class Config:
        from_attributes: True
        valid_assignment: True