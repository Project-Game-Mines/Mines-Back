from pydantic import BaseModel

class CashoutSchema(BaseModel):
    match_id: str
   