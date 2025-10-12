from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.dal.user_dal import UserDal
from app.dal.admin_dal import AdminDAL
from app.auth.auth import hash_password, verify_password, create_access_token
from app.db.models.user import RoleEnum

class AuthService:
    def __init__(self, db: Session) -> None:
        self.user_dal = UserDal(db)
        self.admin_dab = AdminDAL(db)
        self.db = db

    def register_user(self, *, id: int, email: str, username: str, password: str, role: RoleEnum) -> str:
        if self.user_dal.get_by_id(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this ID already exists."
            )
        if self.user_dal.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
        password_hash = hash_password(password)
        user = self.user_dal.create_user(id= id, email=email, username=username, password_hash=password_hash, role=role)
        self.db.commit()
        return user
    
    def authenticate(self, *, id, email: str, password: str) -> str:
        user = self.user_dal.get_by_id(id)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return create_access_token(subject=str(user.id), role=user.role)