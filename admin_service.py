from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from user import User
from schemas import EditUserModel
from auth_service import verify_token


def get_all_users(authorization: str, session: Session):
    user = verify_token(authorization=authorization,session=session)
    if not user.is_staff:
        raise HTTPException(status_code=401, detail="Only staff!")
    users = session.query(User).all()
    users :dict = [user.to_dict() for user in users]
    return JSONResponse(
        status_code = 200,
        content = users
    )


def edit_user(authorization : str, user_id: int, user : EditUserModel,session: Session):
    admin = verify_token(authorization=authorization,session=session)

    if not admin.is_staff:
        raise HTTPException(status_code=401, detail="Only for admins!")

    db_user=session.query(User).filter(User.id == user_id).first()
    db_user.email = user.email
    db_user.username = user.username
    db_user.is_active = user.is_active
    db_user.is_staff = user.is_staff

    session.save(db_user)
    session.commit()

    return JSONResponse(
        content={"detail" : "Edited!"},
        status_code=200
    )
