from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from schemas import RegisterRequest, LoginModel
from src.models.user import User

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'e36c4770f67f3a367e7d7aa0b9505a0aa9760e56bc24c03109b637e60ced6429'
ALGORITHM = 'HS256'

def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def register(user: RegisterRequest, session: Session):
    if session.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User already exists with that email")

    if session.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="User already exists with that username")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email, 
        username = user.username,
        password=hashed_password,
        is_staff = False,
        is_active = True
        )
    session.add(new_user)
    session.commit()
    
    return JSONResponse(
        content={"detail": "User registered successfully"},
        status_code=201
    )


def login(user: LoginModel, session: Session): 
    db_user = session.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    access_token = create_access_token(data={"sub": db_user.username})
    db_user.token = access_token
    session.commit()

    return status.HTTP_200_OK, {"access_token": access_token}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(authorization: str, session: Session):
    try:
        if authorization is None:
            raise HTTPException(status_code=400, detail="Authorization header missing")
        
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        db_user = session.query(User).filter(User.username == username).first()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        if db_user.token != token:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return db_user
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def logout(authorization: str, session: Session):
    user = verify_token(authorization=authorization, session= session)

    user.token = None
    
    session.add(user)

    return JSONResponse(status_code= 200,
                        content={"detail": "Success"}
                        )


