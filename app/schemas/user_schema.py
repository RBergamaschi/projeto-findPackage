from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, computed_field, field_validator

from app.schemas.address_schema import AddressCreate, AddressRead


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    social_name: Optional[str] = None
    email: EmailStr
    password: str
    address: AddressCreate | None = None
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    social_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    social_name: Optional[str] = None
    email: EmailStr
    address: Optional[AddressRead] = None
    
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