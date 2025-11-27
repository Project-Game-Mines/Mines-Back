from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class UserRepository:

    def __init__(self, db):
        self.db = db

    def create_user(self, user_dict: dict) -> dict:
        # insere create_at automaticamente
        user_dict["create_at"] = datetime.utcnow()

        result = self.db.users.insert_one(user_dict)

        user_dict["_id"] = result.inserted_id
        return user_dict
    
    def get_user_by_name(self, name: str):
        return self.db.users.find_one({"name": name})
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return self.db.users.find_one({"_id": ObjectId(user_id)})

    def get_all_users(self) -> List[dict]:
        return list(self.db.users.find())
    
    def delete_user(self, user_id: str) -> bool:
        result = self.db.users.delete_one({"_id": ObjectId(user_id)})

        return result.deleted_count > 0