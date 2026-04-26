from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean

from app.models.base_model import EntityMeta as Base
if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.order import Order


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    social_name: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    address_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("addresses.id"))
    
    # Relationships
    address: Mapped[Address | None] = relationship("Address", back_populates="users")
    orders: Mapped[list[Order]] = relationship("Order", back_populates="user")