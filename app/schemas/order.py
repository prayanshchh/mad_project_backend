from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemRead(BaseModel):
    id: int
    food_item_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemRead] = []

    class Config:
        orm_mode = True