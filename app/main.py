from fastapi import FastAPI
from app.controllers.user_controller import UserRouter

app = FastAPI(title="Mines Academy")

app.include_router(UserRouter)


