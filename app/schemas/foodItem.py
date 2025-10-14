from pydantic import BaseModel, Field
from typing import Optional

class FoodItemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    price: float = Field(..., gt=0)

class FoodItemRead(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True
