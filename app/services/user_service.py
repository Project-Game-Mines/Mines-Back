from typing import List
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUser
from app.middlewares.exceptions import BadRequestError, NotFoundError, UnauthorizedError, InternalServerError


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: CreateUser):

        if self.repository.get_user_by_id(user.id):
            raise UnauthorizedError("Usuário já existente")
        
        else:        
            try:
                user_created = self.repository.create_user(user)

                if not user_created:
                    raise BadRequestError("user não criado, verifique credenciais")
                
                return CreateUser(
                    name=user_created["name"],
                    create_at= user_created["create_at"]
                )
            
            except Exception as e:
                raise BadRequestError(f"Error ao criar user: {str(e)}")


    def get_all_users(self) -> List[CreateUser]:

        try:

            users = self.repository.get_all_users()
            list = []
            
            if not users:
                return BadRequestError("Não Há Usuários")
            
            for doc in users:
                list.append(
                    CreateUser(
                        id=str(doc["_id"]),
                        name=doc["name"],
                        create_at=["creat_at"]
                    ) 
                )
            return list
        
        except Exception as e:
            raise Exception(f"Erro ao listar users: {str(e)}")


    def get_user_by_id(self, user_id: str) -> CreateUser:

        try:

            user = self.repository.get_user_by_id(user_id)

            if not user:
                raise NotFoundError(user_id)
            
            return CreateUser(
                id=str(user["id"]),
                name=user["name"],
                create_at=["create_ad"]
            )
        
        except Exception as e:
            raise Exception(f"Erro ao buscar user: {str(e)}")

    def delete_user(self, user_id: str) -> dict:

        try:

            if not self.repository.delete_user(user_id):
                raise NotFoundError(user_id)
            
            return {"mensagem": "user deletado com sucesso"}
        
        except Exception as e:
            raise Exception(f"Erro ao deletar user: {str(e)}")
        
