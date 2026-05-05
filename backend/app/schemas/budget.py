from uuid import UUID
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.category import CategoryRead


class BudgetBase(BaseModel):
    category_id: UUID
    amount: Decimal = Field(..., gt=0)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2100)
    alert_threshold: Decimal = Field(80.0, ge=1, le=100)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    alert_threshold: Optional[Decimal] = Field(None, ge=1, le=100)


class BudgetRead(BudgetBase):
    id: UUID
    user_id: UUID
    alert_sent: bool
    category: Optional[CategoryRead] = None

    model_config = {"from_attributes": True}


class BudgetWithSpending(BudgetRead):
    spent: Decimal
    remaining: Decimal
    percentage: float
    is_over_budget: bool
    is_alert_triggered: bool
