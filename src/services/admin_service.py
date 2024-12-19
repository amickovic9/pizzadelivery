from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.models.order import Order
from src.models.user import User
from schemas import EditUserModel, OrderStatusUpdate
from src.services.auth_service import verify_token


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

    session.add(db_user)
    session.commit()

    return JSONResponse(
        content={"detail" : "Edited!"},
        status_code=200
    )

def delete_user(authorization : str,user_id: int, session: Session):
    db_user = verify_token(authorization=authorization,session=session)

    if not db_user.is_staff:
        raise HTTPException(401, "Only admins!")
    
    user_for_removing = session.query(User).filter(User.id == user_id).first()
    
    session.delete(user_for_removing)
    session.commit()
    return JSONResponse(
        status_code=200,
        content={"detail" : "Success"}
    )


def change_order_status(authorization: str , order_id: int, status : OrderStatusUpdate, session: Session):
    user = verify_token(authorization=authorization, session=session)
    
    if not user.is_staff:
        raise HTTPException(401, "Only admins!")
    
    order_db = session.query(Order).filter(Order.id == order_id).first()

    if not order_db:
        raise HTTPException(404, "There is no order with that id!")
    
    order_db.status = status.status

    session.add(order_db)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail" : "Success"}
    )
    