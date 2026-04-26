from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AddressCreate(BaseModel):
    cep: str
    state: str
    city: str
    neighborhood: str
    street: str
    number: int
    complement: Optional[str] = None

class AddressUpdate(BaseModel):
    cep: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    number: Optional[int] = None
    complement: Optional[str] = None

class AddressRead(BaseModel):
    id: int
    cep: str
    state: str
    city: str
    neighborhood: str
    street: str
    number: int
    complement: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)