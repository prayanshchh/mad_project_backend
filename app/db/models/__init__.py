# app/db/models/__init__.py

from app.db.session import Base

# Import every model that defines relationships
from app.db.models.user import User, RoleEnum
from app.db.models.orders import Order, OrderItem, OrderStatus
from app.db.models.menu import Menu, MenuItem
from app.db.models.food_items import FoodItem

__all__ = [
    "User",
    "RoleEnum",
    "Order",
    "OrderItem",
    "OrderStatus",
    "Menu",
    "MenuItem",
    "FoodItem",
]
