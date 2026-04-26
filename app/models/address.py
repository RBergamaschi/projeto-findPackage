from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer

from app.models.base_model import EntityMeta as Base
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.order import Order


class Address(Base):
    __tablename__ = "addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cep: Mapped[str] = mapped_column(String(9), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    neighborhood: Mapped[str] = mapped_column(String(255), nullable=False)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    complement: Mapped[str | None] = mapped_column(String(255))
    
    # Relationships
    users: Mapped[list[User]] = relationship("User", back_populates="address")
    orders: Mapped[list[Order]] = relationship("Order", back_populates="address")