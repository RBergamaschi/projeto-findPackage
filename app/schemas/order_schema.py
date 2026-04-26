from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.models.enums import OrderStatus
from app.schemas.address_schema import AddressRead


class OrderCreate(BaseModel):
    user_id: int
    address_id: int

class OrderUpdate(BaseModel):
    address_id: Optional[int] = None
    status: Optional[OrderStatus] = None

class OrderRead(BaseModel):
    id: int
    address: AddressRead
    status: OrderStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)