from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.db.models.menu import Menu, MenuItem
from app.db.models.food_items import FoodItem

class MenuDAL:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_menu(self, menu_date, items) -> tuple[Menu, list[int]]:
        menu = Menu(menu_date=menu_date)
        self.db.add(menu)
        self.db.flush()

        missing_items = []

        for item in items:
            food_item = self.db.get(FoodItem, item.food_item_id)
            
            if not food_item:
                missing_items.append(item.food_item_id)
                continue

            menu_item = MenuItem(
                menu_id = menu.id,
                food_item_id = item.food_item_id,
                override_price = item.override_price
            )
            self.db.add(menu_item)
            self.db.commit()
        return menu, missing_items
    
    def get_by_date(self, menu_date) -> Menu:
        return self.db.execute(select(Menu).where(Menu.menu_date==menu_date)).scalar_one_or_none()
    
    def get_by_id(self, menu_id: int) -> Menu:
        return self.db.get(Menu, menu_id)
    
    def update_menu(self, menu_id, menu_date = None, items=None) -> tuple[Menu | None, list[int]]:
        menu = self.get_by_id(menu_id)
        if menu:
            missing_items = []
            if menu_date:
                menu.menu_date = menu_date
            
            for item in items:
                food_item = self.db.get(FoodItem, item.food_item_id)
                
                if not food_item:
                    missing_items.append(item.food_item_id)
                    continue
            
            if items is not None:
                self.db.execute(delete(MenuItem).where(MenuItem.menu_id == menu_id))
                for item in items:
                    menu_item = MenuItem(
                        menu_id = menu_id,
                        food_item_id = item.food_item_id,
                        override_price= item.override_price
                    )
                    self.db.add(menu_item)
        return menu, missing_items
