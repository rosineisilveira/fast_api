
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema, ItemOrderSchema,ResponseOrderSchema
from models import Order, User, ItemOrder
from typing import List


order_router = APIRouter(prefix="/order", tags=["orders"], dependencies=[Depends(verify_token)])

@order_router.get("/")
async def orders( session:Session = Depends(get_session)):
    orders = session.query(Order).all()
    return orders

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user=order_schema.id_user)
    session.add(new_order)
    session.commit()
    return {"message": " Order: {new_order.id} succesfully created"}

@order_router.post("/order/cancel/{id_order}")
async def cancel_order(id_order: int, session: Session=Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order: 
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=400, detail="User not autorized")
    else:
        order.status = "CANCELED"
        session.commit()
    return {
        "message": f"Order number: {order.id} succesfully canceled",
        "order": order
    }

@order_router.get("/list")
async def list_order(session: Session = Depends(get_session), user: User = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=400, detail="Not autorized")
    else:
        orders = session.query(Order).all()
        return {
            "message": orders
        }

@order_router.post("/order/add-item/{id_order}")
async def add_item_order(id_order: int,
                         item_order_schema: ItemOrderSchema,
                          session: Session = Depends(get_session),
                           user: User = Depends(verify_token) ):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    item_order = ItemOrder(item_order_schema.amount,
                           item_order_schema.flavor,
                           item_order_schema.size,
                           item_order_schema.price_unity,                       
                           id_order)
    session.add(item_order)
    order.calculate_price()
    session.commit()
    return{
        "message": "Success",
        "item_id": item_order.id,
        "price_order": order.price
    }

@order_router.post("/order/remove-item/{id_item_order}")
async def remove_item_order(id_item_order:int,
                            session: Session = Depends (get_session),
                            user : User = Depends(verify_token)):
    item_order = session.query(ItemOrder).filter(ItemOrder.id==id_item_order).first()
    order = session.query(Order).filter(Order.id==item_order.order).first()
    if not item_order:
        raise HTTPException(status_code=400, detail="Item not found")

    # if not order:
        # raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Not autorized")
    session.delete(item_order)
    order.calculate_price()
    session.commit()
    return {
        "message": " Item successfully removed",
        "amount_items_order": len(order.Items),
        "order": order
    }

@order_router.get("/order/order-user", response_model=List[ResponseOrderSchema])
async def list_order(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    orders = session.query(Order).filter(Order.user==user.id).all()
    return orders
      

@order_router.get("/order/{id_order}")
async def order_view(id_order: int, session:Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=401, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Not autorized")
    return {
        "quantity_Items":len(order.Items),
        "order": order
    }

