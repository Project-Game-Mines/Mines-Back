from app.middlewares.exceptions import BadRequestError
from app.repositories.wallets_repository import WalletRepository
from app.schemas.wallets_schemas import WalletCreate, WalletSchemas, WalletSchemasBody


class WalletService:

    def __init__(self, repository: WalletRepository):
        self.repository = repository

    def create_wallets(self, data: WalletCreate) -> WalletSchemas:
        try:
            wallet = self.repository.create_wallets(data)
            if not wallet:
                raise BadRequestError("Erro ao criar carteira")
            return wallet
        except Exception as e:
            raise BadRequestError(str(e))

    def get_balance(self, user_id: str) -> WalletSchemas:
        wallet = self.repository.get_balance(user_id)
        if not wallet:
            raise BadRequestError("Carteira não encontrada")
        return wallet


    
    def debit(self, data: WalletSchemasBody) -> WalletSchemas:
        if data.amount <= 0:
            raise BadRequestError("O valor deve ser maior que 0")

        updated = self.repository.debit(data.user_id, data.amount)
        if not updated:
            raise BadRequestError("Saldo insuficiente ou erro ao debitar")

        return updated

    def credit(self, data: WalletSchemasBody) -> WalletSchemas:
        if data.amount <= 0:
            raise BadRequestError("O valor deve ser maior que 0")

        updated = self.repository.credit(data.user_id, data.amount)
        if not updated:
            raise BadRequestError("Erro ao creditar")

        return updated