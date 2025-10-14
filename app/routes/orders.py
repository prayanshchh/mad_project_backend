# app/routes/order.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.order_service import OrderService
from app.schemas.order import OrderCreate, OrderRead
from app.routes.auth import get_current_user
from app.db.models.user import User
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def place_order(payload: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Place an order for the current logged-in user.
    """
    service = OrderService(db)
    return service.place_order(user_id=current_user.id, items=payload.items, menu_date=payload.menu_date)


@router.get("/", response_model=List[OrderRead])
def get_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all orders of the current logged-in user.
    """
    service = OrderService(db)
    return service.get_users_orders(user_id=current_user.id)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get a specific order by its ID.
    """
    service = OrderService(db)
    order = service.get_single_order(order_id)
    if not order or order.user_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    return order
