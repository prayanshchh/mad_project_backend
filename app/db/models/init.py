from app.db.session import Base
from .user import User
from .admin import Admin
from .food_items import FoodItem
from .menu import Menu, MenuItem

target_metadata = Base.metadata