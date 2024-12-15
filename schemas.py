from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com"
            }
        }

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

