from pydantic import BaseModel
from typing import Generic, TypeVar


T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
