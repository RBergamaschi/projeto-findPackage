from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.enums import VehicleType, LiscenseType
from app.schemas.user_schema import UserSummary


class DriverProfileCreate(BaseModel):
    user_id: int
    cnh_number: str
    vehicle_type: VehicleType
    license_type: LiscenseType
    plate_number: str

class DriverProfileUpdate(BaseModel):
    cnh_number: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None
    license_type: Optional[LiscenseType] = None
    plate_number: Optional[str] = None
    is_available: Optional[bool] = None

class DriverProfileRead(BaseModel):
    id: int
    user: UserSummary
    cnh_number: str
    vehicle_type: VehicleType
    license_type: LiscenseType
    plate_number: str
    is_available: bool

    model_config = ConfigDict(from_attributes=True)

class DriverProfileSummary(BaseModel):
    id: int
    user: UserSummary
    vehicle_type: VehicleType
    license_type: LiscenseType
    is_available: bool

    model_config = ConfigDict(from_attributes=True)