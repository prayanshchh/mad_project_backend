from sqlalchemy.orm import Session
from app.db.models.admin import Admin
from app.db.models.user import User

class AdminDAL:
    def __init__(self, db:Session) -> None:
        self.db = db

    def create_admin(self, email: str, username: str, password_hash: str) -> Admin:
        admin = Admin(email=email, username=username, password_hash=password_hash)
        self.db.add(admin)
        self.db.commit()
        return admin
    
    def get_admin_by_id(self, id: int) -> Admin | None:
        return self.db.get(Admin, id)
    
    def get_admin_by_user(self, user_id: int) -> Admin:
        return self.db.query(Admin).filter(Admin.user_id == user_id)