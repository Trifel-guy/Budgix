from uuid import UUID
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from app.models.transaction import TransactionType
from app.schemas.category import CategoryRead


class TransactionBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    type: TransactionType
    description: str = Field(..., min_length=1, max_length=255)
    note: str | None = None
    date: date
    tags: list[str] = []
    category_id: UUID | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    description: Optional[str] = None
    note: Optional[str] = None
    date: Optional[date] = None
    tags: Optional[list[str]] = None
    category_id: Optional[UUID] = None


class TransactionRead(TransactionBase):
    id: UUID
    user_id: UUID
    category: Optional[CategoryRead] = None

    model_config = {"from_attributes": True}


class TransactionPage(BaseModel):
    items: list[TransactionRead]
    total: int
    page: int
    size: int
    pages: int
