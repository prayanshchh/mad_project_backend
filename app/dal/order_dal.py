from typing import List
from sqlalchemy.orm import Session
from app.db.models.orders import Order, OrderItem
from app.db.models.menu import Menu, MenuItem
from app.db.models.food_items import FoodItem
from datetime import datetime
from fastapi import HTTPException, status


class OrderDAL:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_order(self, user_id: int, menu_date: str, items: List[dict]) -> Order:
        # 1. Fetch today's menu
        menu = self.db.query(Menu).filter(Menu.menu_date == menu_date).first()
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No menu found for date {menu_date}"
            )

        total_price = 0
        order_items = []

        for item in items:
            # 2. Find MenuItem for this food_item_id
            menu_item = (
                self.db.query(MenuItem)
                .filter(MenuItem.menu_id == menu.id,
                        MenuItem.food_item_id == item.food_item_id)
                .first()
            )

            if not menu_item:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Food item {item.food_item_id} not in menu {menu_date}"
                )

            # 3. Determine price
            price = (
                float(menu_item.override_price)
                if menu_item.override_price is not None
                else float(menu_item.food_item.price)
            )
            item_total = price * item.quantity
            total_price += item_total

            order_items.append(
                OrderItem(
                    food_item_id=item.food_item_id,
                    quantity=item.quantity,
                    price=item_total
                )
            )

        # 4. Create order
        order = Order(
            user_id=user_id,
            total_price=total_price,
            created_at=datetime.utcnow(),
            items=order_items
        )

        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_order_by_user(self, user_id: int) -> List[Order]:
        """Return all orders placed by a given user."""
        return (
            self.db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    # ----------------------------
    # GET ORDER BY ID
    # ----------------------------
    def get_order_by_id(self, order_id: int) -> Order:
        """Return a single order by ID."""
        return (
            self.db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )
