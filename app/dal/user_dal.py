from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.user import RoleEnum

from app.db.models.user import User

class UserDal:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.scalar(select(User).where(User.email == email))
    
    def create_user(self, *,id,  email: str, username: str, password_hash: str, role: RoleEnum) -> User:
        user = User(id=id, email=email, username=username, password_hash=password_hash, role=role)
        self.db.add(user)
        return user