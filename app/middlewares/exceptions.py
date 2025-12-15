from fastapi import HTTPException

class BadRequestError(HTTPException):
    routing_key = "BadRequestError"

    def __init__(self, index: str):
        super().__init__(status_code=400, detail=index)


class ForbiddenError(HTTPException):
    routing_key = "ForbiddenError"

    def __init__(self, index: str):
        super().__init__(status_code=401, detail=f'Acesso Negado!: {index}')


class InternalServerError(HTTPException):
    routing_key = "InternalServerError"

    def __init__(self, index: str):
        super().__init__(status_code=500, detail=index)


class NotFoundError(HTTPException):
    routing_key = "NotFoundError"

    def __init__(self, index: str):
        super().__init__(status_code=404, detail=f"{index} não encontrado")


class UnauthorizedError(HTTPException):
    routing_key = "UnauthorizedError"

    def __init__(self, index: str):
        super().__init__(status_code=401, detail=index)