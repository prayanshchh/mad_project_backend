from pydantic import BaseModel
from datetime import datetime, date
from typing import List

class OrderItemCreate(BaseModel):
    food_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    menu_date: date
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
        from_attributes = True