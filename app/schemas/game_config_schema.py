from pydantic import BaseModel, field_serializer, Field, ConfigDict, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]
class CreateGameConfigSchema(BaseModel):
    name: str = "Mines Academy"
    is_active: bool = False
    total_cells: int = 25
    total_mines: int = 3

class GameConfigSchema(BaseModel):
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    is_active: bool
    total_cells: int
    total_mines: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.strftime("%d/%m/%Y %H:%M")


    class Config:
        populate_by_name: True
        from_attributes: True
        valid_assignment: True