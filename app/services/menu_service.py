from sqlalchemy.orm import Session
from app.dal.menu_dal import MenuDAL
from fastapi import HTTPException, status

class MenuService:
    def __init__(self, db:Session) -> None:
        self.db = db
        self.menu_dal = MenuDAL(db)

    def create_menu(self, menu_date, items):
        if(self.menu_dal.get_by_date(menu_date)):
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu already exists for date {menu_date}"
            )
        
        menu, missing_items = self.menu_dal.create_menu(menu_date=menu_date, items=items)

        if missing_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Food items not found: {missing_items}"
            )
        return menu
    
    def get_menu(self, menu_id):
        menu = self.menu_dal.get_by_id(menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu with id {menu_id} not found"
            )
        return menu
    
    def update_menu(self, menu_id, items):
        menu, missing_items = self.menu_dal.update_menu(menu_id=menu_id, items=items)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu with id {menu_id} not found"
            )
        if missing_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Food items not found: {missing_items}"
            )
        return menu
        