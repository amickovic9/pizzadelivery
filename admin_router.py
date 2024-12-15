from fastapi import APIRouter, Request, Depends
from database import get_db
import admin_service
from schemas import EditUserModel
admin_router = APIRouter(
    prefix= '/admin'
)

@admin_router.get("/all-users")
async def get_all_users(request: Request,session = Depends(get_db)):
    print("insisde")
    authorization : str = request.headers.get('Authorization')
    return admin_service.get_all_users(authorization=authorization,session=session)

@admin_router.patch("/edit-user/{user_id}")
async def edit_user(user_id : int, user : EditUserModel, request: Request, session = Depends(get_db)):
    authorization : str = request.headers.get("Authorization")
    return admin_service.edit_user(authorization,user_id, user, session)