from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class UserRepository:

    def __init__(self, db):
        self.db = db

    def create_user(self, user_dict: dict) -> dict:

        user_dict["created_at"] = datetime.utcnow().strftime("%d/%m/%Y-%H:%M")

        result = self.db.users.insert_one(user_dict)

        user_dict["_id"] = result.inserted_id
        return user_dict
    
    def get_user_by_name(self, name: str):
        return self.db.users.find_one({"name": name})
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            return None
        
        user["id"] = str(user["_id"])
        del user["_id"]

        return user

    def get_all_users(self) -> List[dict]:
        return list(self.db.users.find())
    
    def delete_user(self, user_id: str) -> bool:
        result = self.db.users.delete_one({"_id": ObjectId(user_id)})

        return result.deleted_count > 0