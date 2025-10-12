from typing import List
from sqlalchemy.orm import Session
from app.db.models.orders import Order, OrderItem, OrderStatus
from app.db.models.menu import MenuItem
from datetime import date

class OrderDAL:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def create_order(self, user_id: int, items: List[dict]) -> Order:
        total_price = 0
        order_items = []
        print("I am item: ", items)

        for item in items:
            menu_item = self.db.get(MenuItem, item.menu_item_id)
            if not menu_item:
                raise ValueError(f"Menu item with id {item.menu_item_id} not found")
            item_price = menu_item.price * item.quantity
            total_price += item_price

            order_items.append(
                OrderItem(
                    food_item_id=item.menu_item_id,
                    quantity=item.quantity,
                    price=item_price
                )
            )
        order = Order(user_id=user_id, total_price=total_price, items=order_items)
        self.db.add(order)
        self.db.commit()
        return order
    
    def get_order_by_user(self, user_id: int) -> List[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
    
    def get_order_by_id(self, id: int) -> List[Order]:
        return self.db.query(Order).filter(Order.id == id).order_by(Order.created_at.desc()).all()