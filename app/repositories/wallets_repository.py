from datetime import datetime
from app.schemas.wallets_schemas import WalletCreate, WalletSchemas, WalletSchemasBody
from app.middlewares.exceptions import BadRequestError
from pymongo.database import Database


class WalletRepository:

    def __init__(self, db: Database):
        self.collection = db["wallets"]


    def get_balance(self, user_id: str) -> WalletSchemas:
        wallet = self.collection.find_one({"user_id": user_id})
        if not wallet:
            return None
        return WalletSchemas(**wallet)

    def create_wallets(self, data: WalletCreate) -> WalletSchemas:
        wallet_exists = self.collection.find_one({"user_id": data.user_id})
        if wallet_exists:
            raise BadRequestError("Carteira já existe para este usuário")

        new_wallet = {
            "user_id": data.user_id,
            "balance": data.balance,
            "updated_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }

        self.collection.insert_one(new_wallet)
        return WalletSchemas(**new_wallet)



    def debit(self, user_id: str, amount: float) -> WalletSchemas:
        wallet = self.collection.find_one({"user_id": user_id})
        if not wallet:
            return None

        if wallet["balance"] < amount:
            return None

        new_balance = wallet["balance"] - amount
        update_data = {
            "balance": new_balance,
            "updated_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }

        self.collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )

        wallet.update(update_data)
        return WalletSchemas(**wallet)



    def credit(self, user_id: str, amount: float) -> WalletSchemas:
        wallet = self.collection.find_one({"user_id": user_id})
        if not wallet:
            return None

        new_balance = wallet["balance"] + amount
        update_data = {
            "balance": new_balance,
            "updated_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        }

        self.collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )

        wallet.update(update_data)
        return WalletSchemas(**wallet)
