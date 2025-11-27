from fastapi import FastAPI

from app.controllers.user_controller import UserRouter
from app.controllers.wallets_controllers import WalletRouter


app = FastAPI(title="Mines Academy")

app.include_router(UserRouter)
app.include_router(WalletRouter)


print("Loaded at port 8000")