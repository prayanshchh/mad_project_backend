from sqlalchemy.orm import Session
from app.dal.order_dal import OrderDAL

class OrderService:
    def __init__(self, db: Session) -> None:
        self.dal = OrderDAL(db)
    
    def place_order(self, user_id: int, items: list, menu_date):
        return self.dal.create_order(user_id=user_id, items=items, menu_date=menu_date)

    def get_users_orders(self, user_id: int):
        return self.dal.get_order_by_user(user_id=user_id)
    
    def get_single_order(self, id: int):
        return self.dal.get_order_by_id(id=id)
