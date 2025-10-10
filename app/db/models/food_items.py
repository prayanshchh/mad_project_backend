from sqlalchemy import String, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
