from fastapi import APIRouter
from app.routes.auth import router as auth_router
from app.routes.orders import router as orders_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(orders_router)