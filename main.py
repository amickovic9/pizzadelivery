from fastapi import FastAPI
from auth_router import auth_router
from order_router import order_router
from admin_router import admin_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(admin_router)



