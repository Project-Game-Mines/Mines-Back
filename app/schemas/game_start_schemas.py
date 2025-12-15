from pydantic import BaseModel

class GameStartedSchema(BaseModel):
    matchId: str
    user_id: str
    total_cells: int
    total_mines: int