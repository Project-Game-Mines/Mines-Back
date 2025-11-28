from typing import Literal
from pydantic import BaseModel


class TransactionsSchemas(BaseModel):

    transition_id: str
    user_id: str
    match_id: str
    type: Literal["debit", "credit"]
    amount: float
    timestamp: str