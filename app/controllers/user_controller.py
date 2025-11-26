from app.schemas.user_schema import CreateUser, UserSchemaBody
from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from typing import List

UserRouter = APIRouter(tags=['Rotas de usuários'])

def get_db():
    db = get_db()
    try:
        yield db
    finally:
        pass

def get_user_service(db=Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)

@UserRouter.post("/users/register", response_model=UserSchemaBody)
def create_user(user: UserSchemaBody, service: UserService = Depends(get_user_service)):
    return service.create_user(user)

@UserRouter.get("/users/", response_model=List[UserSchemaBody])
def list_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@UserRouter.get("/users/find/{users_id}", response_model=CreateUser)
def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)

@UserRouter.delete("/users/delete/{user_id}", )
def delete_user(user_id: str, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)
