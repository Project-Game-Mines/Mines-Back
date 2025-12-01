from fastapi import HTTPException

class BadRequestError(HTTPException):
    def __init__(self, index: str):
        super().__init__(status_code=400, detail=index)


class ForbiddenError(HTTPException):
    def __init__(self, index: str):
        super().__init__(status_code=401, detail=f'Acesso Negado!: {index}')


class InternalServerError(HTTPException):
    def __init__(self, index: str):
        super().__init__(status_code=500, detail=index)


class NotFoundError(HTTPException):
    def __init__(self, index: str):
        super().__init__(status_code=404, detail=f"{index} não encontrado")


class UnauthorizedError(HTTPException):
    def __init__(self, index: str):
        super().__init__(status_code=401, detail=index)