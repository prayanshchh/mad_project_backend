from datetime import datetime
from sqlalchemy import String, DateTime, BigInteger, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from app.db.session import Base

class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100))
    password_hash   : Mapped[str] = mapped_column(String(100))
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum, name="user_role_enum", create_type=False, create_constraint=True), default=RoleEnum.USER, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
