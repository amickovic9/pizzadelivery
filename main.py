from fastapi import FastAPI
from src.routers.auth_router import auth_router
from src.routers.order_router import order_router
from src.routers.admin_router import admin_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(admin_router)
