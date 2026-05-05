from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field
from app.models.category import CategoryType


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    icon: str = "💰"
    color: str = "#6366f1"
    type: CategoryType


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class CategoryRead(CategoryBase):
    id: UUID
    user_id: UUID

    model_config = {"from_attributes": True}
