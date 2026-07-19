from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class ErrorResponse(BaseModel):
    detail: str


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
