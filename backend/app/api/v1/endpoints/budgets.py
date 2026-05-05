from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.budget import Budget
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetUpdate, BudgetWithSpending
from app.services.budget_service import get_budget_spending

router = APIRouter(prefix="/budgets", tags=["budgets"])


def _get_or_404(budget_id: UUID, user_id, db: Session) -> Budget:
    b = db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    return b


@router.get("", response_model=list[BudgetWithSpending])
def list_budgets(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Budget).filter(Budget.user_id == current_user.id)
    if month:
        q = q.filter(Budget.month == month)
    if year:
        q = q.filter(Budget.year == year)

    budgets = q.all()
    return [get_budget_spending(db, b) for b in budgets]


@router.post("", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_budget(
    payload: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Prevent duplicate budget for same category/month/year
    existing = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.category_id == payload.category_id,
        Budget.month == payload.month,
        Budget.year == payload.year,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Budget already exists for this category/period")

    budget = Budget(**payload.model_dump(), user_id=current_user.id)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.patch("/{budget_id}", response_model=BudgetRead)
def update_budget(
    budget_id: UUID,
    payload: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    b = _get_or_404(budget_id, current_user.id, db)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(b, key, value)
    db.commit()
    db.refresh(b)
    return b


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    b = _get_or_404(budget_id, current_user.id, db)
    db.delete(b)
    db.commit()
