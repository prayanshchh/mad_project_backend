# app/routes/food_item.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.foodItem_service import FoodItemService
from app.schemas.foodItem import FoodItemCreate, FoodItemRead

router = APIRouter(prefix="/food-items", tags=["Food Items"])

@router.post("/", response_model=FoodItemRead, status_code=status.HTTP_201_CREATED)
def create_food_item(payload: FoodItemCreate, db: Session = Depends(get_db)):
    service = FoodItemService(db)
    return service.create_food_item(name=payload.name, price=payload.price)


@router.get("/", response_model=list[FoodItemRead])
def list_food_items(db: Session = Depends(get_db)):
    service = FoodItemService(db)
    return service.get_all_food_items()


@router.get("/{item_id}", response_model=FoodItemRead)
def get_food_item(item_id: int, db: Session = Depends(get_db)):
    service = FoodItemService(db)
    return service.get_food_item(item_id)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_food_item(item_id: int, db: Session = Depends(get_db)):
    service = FoodItemService(db)
    return service.delete_food_item(item_id)
