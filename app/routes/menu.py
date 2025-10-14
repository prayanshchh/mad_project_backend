from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.menu_service import MenuService
from app.schemas.menu import MenuCreate, MenuUpdate, MenuRead  # assuming you have these

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.post("/", response_model=MenuRead, status_code=status.HTTP_201_CREATED)
def create_menu(payload: MenuCreate, db: Session = Depends(get_db)):
    service = MenuService(db)
    menu = service.create_menu(menu_date=payload.menu_date, items=payload.items)
    return menu


@router.get("/{menu_id}", response_model=MenuRead)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    service = MenuService(db)
    return service.get_menu(menu_id)


@router.put("/{menu_id}", response_model=MenuRead)
def update_menu(menu_id: int, payload: MenuUpdate, db: Session = Depends(get_db)):
    service = MenuService(db)
    menu = service.update_menu(menu_id=menu_id, items=payload.items)
    return menu
