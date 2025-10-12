from pydantic import BaseModel, EmailStr, Field
from app.db.models.user import RoleEnum

class UserCreate(BaseModel):
    id: int
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    password: str
    role: RoleEnum

class LoginRequest(BaseModel):
    id: int
    email: EmailStr
    password: str = ""

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: RoleEnum