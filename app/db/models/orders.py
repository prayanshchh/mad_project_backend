from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.db.models.food_items import FoodItem

import enum

class OrderStatus(str, enum.Enum):
    pending = "pending"
    preparing = "preparing"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key= True, index = True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    food_item_id: Mapped[int] = mapped_column(ForeignKey("food_items.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    order = relationship("Order", back_populates="items")
    menu_item = relationship("FoodItem")
