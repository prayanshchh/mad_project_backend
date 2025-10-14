from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.food_items import FoodItem


class FoodItemDAL:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_food_item(self, name: str, price: float) -> FoodItem:
        food_item = FoodItem(name=name, price=price)
        self.db.add(food_item)
        self.db.commit()
        self.db.refresh(food_item)
        return food_item

    def get_food_item(self, item_id: int) -> FoodItem | None:
        return self.db.get(FoodItem, item_id)

    def get_all_food_items(self) -> list[FoodItem]:
        return list(self.db.execute(select(FoodItem)).scalars().all())

    def delete_food_item(self, item_id: int) -> bool:
        food_item = self.get_food_item(item_id)
        if not food_item:
            return False
        self.db.delete(food_item)
        self.db.commit()
        return True
