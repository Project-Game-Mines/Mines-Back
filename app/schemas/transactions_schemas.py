from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class TransactionsSchemas(BaseModel):

    user_id: str
    match_id: str
    type: Literal["debit", "credit"]
    amount: float
    timestamp: datetime