from datetime import datetime

from bson import ObjectId

from app.schemas.transactions_schemas import TransactionsSchemas
from app.schemas.wallets_schemas import WalletCreate, WalletSchemas
from app.middlewares.exceptions import BadRequestError

from pymongo.database import Database



class WalletRepository:

    def __init__(self, db: Database):
        self.collection_wallet = db["wallets"]
        self.collection_transactions = db["transactions"]


    def get_balance(self, user_id: str) -> WalletSchemas:
        
        wallet = self.collection_wallet.find_one({"user_id": user_id})
        
        if not wallet:
            return None
        return WalletSchemas(**wallet)
    

    def create_wallets(self, data: WalletCreate) -> WalletSchemas:
        wallet_exists = self.collection_wallet.find_one({"user_id": data.user_id})
        if wallet_exists:
            raise BadRequestError("Carteira já existe para este usuário")

        new_wallet = {
            "user_id": data.user_id,
            "balance": data.balance,
            "updated_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }

        self.collection_wallet.insert_one(new_wallet)
        return WalletSchemas(**new_wallet)



    def debit(self, user_id: str, amount: float, match_id: str) -> WalletSchemas:

        wallet = self.collection_wallet.find_one({"user_id": user_id})

        if not wallet:
            raise BadRequestError("Carteira não encontrada")

        if wallet["balance"] < amount:
            raise BadRequestError("Saldo insuficiente")

        new_balance = wallet["balance"] - amount

        update_data = {
            "balance": new_balance,
            "updated_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }

        self.collection_wallet.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )

        wallet.update(update_data)

        tx = TransactionsSchemas(
            transition_id=str(ObjectId()),
            user_id=user_id,
            match_id=match_id,
            type="debit",
            amount=amount,   
            timestamp=datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        )

        self.collection_transactions.insert_one(tx.model_dump())

        return WalletSchemas(**wallet)



    def credit(self, user_id: str, amount: float, match_id: str) -> WalletSchemas:

        wallet = self.collection_wallet.find_one({"user_id": user_id})

        if not wallet:
            raise BadRequestError("Carteira não encontrada")

        new_balance = wallet["balance"] + amount

        update_data = {
            "balance": new_balance,
            "updated_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }

        self.collection_wallet.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )

        wallet.update(update_data)

        tx = TransactionsSchemas(
            transition_id=str(ObjectId()),
            user_id=user_id,
            match_id=match_id,
            type="credit",
            amount=amount,   
            timestamp=datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        )

        self.collection_transactions.insert_one(tx.model_dump())
        return WalletSchemas(**wallet)