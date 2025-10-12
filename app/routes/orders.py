from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderRead
from app.services.order_service import OrderService
from app.routes.auth import get_current_user
from app.db.models.orders import Order

router = APIRouter(prefix="/orders", tags=["orders"])

def get_order_service(db: Session = Depends(get_db)):
    return OrderService(db)

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def place_order(payload: OrderCreate, current_user = Depends(get_current_user), svc: OrderService = Depends(get_order_service)):
    return svc.place_order(user_id=current_user.id, items=payload.items)

@router.get("/", response_model= list[OrderRead])
def get_orders(current_user = Depends(get_current_user), svc: OrderService = Depends(get_order_service)):
    return svc.get_users_orders(user_id=current_user.id)

@router.get("/{order_id}", response_model=OrderRead)
def get_single_order(order_id: int, svc: OrderService = Depends(get_order_service)):
    order = svc.get_single_order(id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order