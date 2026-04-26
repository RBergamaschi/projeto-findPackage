from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, computed_field
from datetime import datetime

from app.schemas.address_schema import AddressCreate, AddressUpdate, AddressRead
from app.schemas.order_schema import OrderRead


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    social_name: Optional[str] = None
    email: EmailStr
    password: str
    address: AddressCreate | None = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    social_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    address: Optional[AddressUpdate] = None

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    social_name: Optional[str] = None
    email: EmailStr
    address: Optional[AddressRead] = None
    orders: list[OrderRead] = []
    
    @computed_field
    @property
    def display_name(self) -> str:
        return self.social_name or f"{self.first_name} {self.last_name}"

    model_config = ConfigDict(from_attributes=True)

class UserSummary(BaseModel):
    id: int
    first_name: str
    last_name: str
    social_name: Optional[str] = None
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)