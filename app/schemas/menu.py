from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class MenuItemCreate(BaseModel):
    food_item_id: int
    override_price: Optional[float] = Field(None, gt=0)

class MenuCreate(BaseModel):
    menu_date: date
    items: List[MenuItemCreate]

class MenuUpdate(BaseModel):
    menu_date: Optional[date] = None
    items: Optional[List[MenuItemCreate]] = None

class MenuItemRead(BaseModel):
    id: int
    menu_id: int
    food_item_id: int
    override_price: Optional[float] = None

    class Config:
        from_attributes = True

class MenuRead(BaseModel):
    id: int
    menu_date: date
    items: List[MenuItemRead]

    class Config:
        from_attributes = True
