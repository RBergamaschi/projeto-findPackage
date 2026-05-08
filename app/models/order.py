from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SqlEnum
from datetime import datetime, timezone

from app.models.base_model import EntityMeta as Base
from app.models.enums import OrderStatus
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.address import Address
    from app.models.tracking import Tracking


class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey("addresses.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user: Mapped[User] = relationship("User", back_populates="orders")
    address: Mapped[Address] = relationship("Address", back_populates="orders")
    trackings: Mapped[list[Tracking]] = relationship("Tracking", back_populates="order")