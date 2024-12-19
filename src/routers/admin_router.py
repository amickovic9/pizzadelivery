from fastapi import APIRouter, Request, Depends
from src.models.database import get_db
import src.services.admin_service as admin_service
from schemas import EditUserModel, OrderStatusUpdate

admin_router = APIRouter(
    prefix= '/admin',
    tags = ['admin']
)

@admin_router.get("/all-users")
async def get_all_users(request: Request,session = Depends(get_db)):
    authorization : str = request.headers.get('Authorization')
    return admin_service.get_all_users(authorization=authorization,session=session)

@admin_router.patch("/edit-user/{user_id}")
async def edit_user(user_id : int, user : EditUserModel, request: Request, session = Depends(get_db)):
    authorization : str = request.headers.get("Authorization")
    return admin_service.edit_user(authorization,user_id, user, session)

@admin_router.delete("/delete-user/{user_id}")
async def delete_user(user_id : int, request: Request, session = Depends(get_db)):
    authorization : str = request.headers.get("Authorization")
    return admin_service.delete_user(authorization,user_id, session)

@admin_router.patch("/change-order-status/{order_id}")
async def change_order_status(order_id : int, status: OrderStatusUpdate, request : Request, session = Depends(get_db)):
    authorization : str = request.headers.get("Authorization")
    return admin_service.change_order_status(authorization, order_id, status, session)
    