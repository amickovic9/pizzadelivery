from fastapi import APIRouter, Depends, Request
from database import get_db
from schemas import OrderModel
import order_service

order_router = APIRouter(
    prefix = '/orders'
)

@order_router.post('/make-order')
async def make_order(request: Request, order:OrderModel, session = Depends(get_db)):
    authorization: str = request.headers.get("Authorization")
    return order_service.make_order(authorization, order,session)

@order_router.get("/my-orders")
async def my_orders(request : Request, session = Depends(get_db)):
    authorization : str = request.headers.get("Authorization")
    return order_service.get_my_orders(authorization, session)

@order_router.delete("/cancel-order/{order_id}")
async def cancel_order(request : Request, order_id : int, session = Depends(get_db)):
    authorization : str = request.headers.get("Authorization")
    return order_service.cancel_order(authorization, order_id, session)
