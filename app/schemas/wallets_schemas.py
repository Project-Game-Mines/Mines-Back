from pydantic import BaseModel


class WalletSchemas(BaseModel):

    user_id: str
    balance: float
    updated_at: str  

class WalletSchemasBody(BaseModel):

    user_id: str
    amount: float

class WalletCreate(BaseModel):
    user_id: str
    balance: float