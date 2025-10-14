# app/services/food_item_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dal.foodItem_dal import FoodItemDAL


class FoodItemService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.food_item_dal = FoodItemDAL(db)

    def create_food_item(self, name: str, price: float):
        if price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Price must be greater than 0"
            )
        return self.food_item_dal.create_food_item(name, price)

    def get_food_item(self, item_id: int):
        item = self.food_item_dal.get_food_item(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Food item with id {item_id} not found"
            )
        return item

    def get_all_food_items(self):
        return self.food_item_dal.get_all_food_items()

    def delete_food_item(self, item_id: int):
        success = self.food_item_dal.delete_food_item(item_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Food item with id {item_id} not found"
            )
        return {"message": f"Food item {item_id} deleted successfully"}
