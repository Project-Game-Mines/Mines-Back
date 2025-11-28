from app.schemas.user_schema import CreateUser, UserRequest
from fastapi import APIRouter, Depends, Request
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.repositories.wallets_repository import WalletRepository
from typing import List
from app.database.db import get_database

UserRouter = APIRouter(tags=['Rotas de usuários'])

def get_db():
    db = get_database()
    try:
        yield db
    finally:
        pass

def get_user_service(db=Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    wallet_repo = WalletRepository(db)

    return UserService(user_repo, wallet_repo)

@UserRouter.post("/users/register", response_model=CreateUser)
def create_user(user: UserRequest, service: UserService = Depends(get_user_service)):
    return service.create_user(user)

@UserRouter.get("/users/", response_model=List[CreateUser])
def list_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@UserRouter.get("/users/find/{users_id}", response_model=CreateUser)
def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)

@UserRouter.delete("/users/delete/{user_id}", )
def delete_user(user_id: str, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)
