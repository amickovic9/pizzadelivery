from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas import RegisterRequest, LoginModel
from src.models.database import get_db
import src.services.auth_service as auth_service

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.get('/logout')
async def logout(request:Request, session = Depends(get_db)):
    authorization : str = request.headers.get("Authorization")
    return auth_service.logout(authorization, session)

@auth_router.post("/register")
async def register_user(user: RegisterRequest, session: Session = Depends(get_db)): 
    auth_service.register(user, session)
    
@auth_router.post('/login')
async def login_user(user: LoginModel, session: Session = Depends(get_db)):  
    status_code, content = auth_service.login(user, session)
    return JSONResponse(
        content=content,
        status_code=status_code
    )

@auth_router.get('/token')
async def token(request: Request, session: Session = Depends(get_db)):
    authorization: str = request.headers.get("Authorization")
    return auth_service.verify_token(authorization, session)
