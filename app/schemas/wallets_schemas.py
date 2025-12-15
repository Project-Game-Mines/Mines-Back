from datetime import datetime
from pydantic import BaseModel


class WalletSchemas(BaseModel):

    user_id: str
    balance: float
    updated_at: datetime  

class WalletSchemasBody(BaseModel):

    user_id: str
    amount: float

class WalletCreate(BaseModel):
    user_id: str
    balance: float