from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from app.db.models.user import RoleEnum
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, role: RoleEnum) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
