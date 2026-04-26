from __future__ import annotations
import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.order_schema import OrderRead


class TrackingCreate(BaseModel):
    order_id: int
    latitude: float
    longitude: float

class TrackingRead(BaseModel):
    id: int
    order: OrderRead
    latitude: float
    longitude: float
    sent_at: datetime

    model_config = ConfigDict(from_attributes=True)