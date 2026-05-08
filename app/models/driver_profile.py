from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy import Enum as SqlEnum

from app.models.base_model import EntityMeta as Base
from app.models.enums import VehicleType, LiscenseType
if TYPE_CHECKING:
    from app.models.user import User


class DriverProfile(Base):
    __tablename__ = "driver_profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    cnh_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    vehicle_type: Mapped[VehicleType] = mapped_column(SqlEnum(VehicleType), nullable=False, default=VehicleType.CAR)
    license_type: Mapped[LiscenseType] = mapped_column(SqlEnum(LiscenseType), nullable=False, default=LiscenseType.B)
    plate_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    user: Mapped[User] = relationship(
        "User", 
        back_populates="driver_profile"
    )