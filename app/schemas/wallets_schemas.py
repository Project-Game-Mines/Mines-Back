from datetime import datetime
from pydantic import BaseModel


class WalletSchemas(BaseModel):

    user_id: str
    balance: float
    update_at: datetime  

class WalletSchemasBody(BaseModel):

    user_id: str
    amount: float