from pydantic import BaseModel
from src.enum.order_choices import OrderStatusEnum


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginModel(BaseModel):
    username : str
    password : str

class OrderModel(BaseModel):
    quantity: int
    order_status: str = "PENDING"
    pizza_size:str

    class Config:
        from_attributes = True

class EditUserModel(BaseModel):
    username: str
    email: str
    is_staff : bool
    is_active : bool

class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum
