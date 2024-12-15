from fastapi import HTTPException
from database import Session
from schemas import OrderModel, CancelOrder
from sqlalchemy.orm import Session
from auth_service import verify_token
from order import Order
from fastapi.responses import JSONResponse


def make_order(authorization : str, order:OrderModel, session: Session):
    user = verify_token(authorization=authorization, session = session)
    new_order = Order(
        quantity = order.quantity,
        status = order.order_status,
        size = order.pizza_size,
        user_id = user.id
    )
    session.add(new_order)
    session.commit()


def get_my_orders(authorization: str, session: Session):
    user = verify_token(authorization= authorization, session= session)
    orders = session.query(Order).filter(Order.user_id == user.id).all()
    orders_data = [order.to_dict() for order in orders]
    return JSONResponse(
        content=orders_data,
        status_code=200
    )

def cancel_order(authorization: str, order_id:int, session : Session):
    user = verify_token(authorization= authorization,session= session)
    order_db = session.query(Order).filter(Order.id == order_id).first()

    if not order_db:
        raise HTTPException(status_code = 404, detail= "Order ID is invalid")


    if user.id != order_db.user_id:
        raise HTTPException(status_code = 400, detail= "Order is not yours!")

    
    if order_db.status.name != "PENDING":
        raise HTTPException(status_code=400, detail="Order status is not pending!")

    session.delete(order_db)
    session.commit()

    return JSONResponse(
        status_code = 200, 
        content={"detail" : "Order Canceled!"}
    )