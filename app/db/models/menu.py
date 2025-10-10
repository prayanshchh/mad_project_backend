from typing import Optional
from datetime import date
from sqlalchemy import Date, ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_date: Mapped[date] = mapped_column(Date, index=True, unique=True)

    items = relationship("MenuItem", cascade="all, delete-orphan", back_populates="menu")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.id", ondelete="CASCADE"), index=True)
    food_item_id: Mapped[int] = mapped_column(ForeignKey("food_items.id", ondelete="RESTRICT"), index=True)
    override_price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)

    menu = relationship("Menu", back_populates="items")
    food_item = relationship("FoodItem")

    __table_args__ = (UniqueConstraint("menu_id", "food_item_id", name="uq_menu_food"),)
