from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.schemas.auth import UserCreate, Token, UserRead, LoginRequest
from app.services.auth_service import AuthService
from app.auth.auth import decode_access_token

router = APIRouter(prefix="/auth", tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_auth_service(db:Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, svc: AuthService = Depends(get_auth_service)):
    new_user = svc.register_user(
        id = user.id,
        email=user.email,
        username=user.username,
        password=user.password,
        role=user.role
    )
    token = svc.authenticate(id=new_user.id, email=new_user.email, password=user.password)
    return Token(access_token=token, token_type="bearer")


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, svc: AuthService = Depends(get_auth_service)):
    token = svc.authenticate(id = payload.id, email = payload.email, password=payload.password)
    return Token(access_token= token, token_type="bearer")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    sub = decode_access_token(token)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.get(User, int(sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        role=current_user.role
    )
