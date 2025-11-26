from typing import List, Optional
from bson import ObjectId
from app.schemas.user_schema import CreateUser

class UserRepository:

    def __init__(self, db):
        self.db = db

    def create_user(self, user: CreateUser) -> str:
        user_dict = user.model_dump(exclude_unset=True)
        result = self.db.users.insert_one(user_dict)

        if not result.inserted_id:
            raise Exception("Falha ao inserir usuário no DB")
        
        return user_dict
    

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return self.db.users.find_one({"_id": ObjectId(user_id)})
    

    def get_all_users(self) -> List[dict]:
        return list(self.db.users.find())
    

    def delete_user(self, user_id: str) -> bool:
        result = self.db.users.delete_one({"_id": ObjectId(user_id)})

        return result.deleted_count > 0