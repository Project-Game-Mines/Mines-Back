
from fastapi import APIRouter, Depends

from app.database.db import get_database

from app.repositories.wallets_repository import WalletRepository
from app.schemas.wallets_schemas import WalletSchemas, WalletSchemasBody
from app.services.wallet_service import WalletService


WalletRouter = APIRouter(tags=["Criação de Carteiras de Usuários, Debitar e Creditar seu Balanço"])


def get_db():
    db = get_database()
    try:
        yield db
    finally:
        pass


def get_wallet_service(db=Depends(get_db)) -> WalletService:
    repository = WalletRepository(db)
    return WalletService(repository)



@WalletRouter.get("/wallet/balance", response_model=WalletSchemas)
def get_wallet_balance(user_id: str, service: WalletService = Depends(get_wallet_service)):
    return service.get_balance(user_id)




# ----------------> Retirar dinheiro <----------------

@WalletRouter.post("/wallet/debit", response_model=WalletSchemas)
def debit_wallet(
    data: WalletSchemasBody,
    service: WalletService = Depends(get_wallet_service)
):
    return service.debit(data)



# ----------------> Receber dinheiro <----------------
@WalletRouter.post("/wallet/credit", response_model=WalletSchemas)
def credit_wallet(
    data: WalletSchemasBody,
    service: WalletService = Depends(get_wallet_service)
):
    return service.credit(data)