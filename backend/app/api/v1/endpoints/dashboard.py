from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.core.deps import get_db, get_current_user
from app.models.transaction import Transaction, TransactionType
from app.models.category import Category
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Total income, expenses, balance for a given month."""
    def total(tx_type: TransactionType) -> Decimal:
        result = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == current_user.id,
                Transaction.type == tx_type,
                extract("month", Transaction.date) == month,
                extract("year", Transaction.date) == year,
            )
            .scalar()
        )
        return Decimal(str(result))

    income = total(TransactionType.income)
    expenses = total(TransactionType.expense)
    return {
        "income": income,
        "expenses": expenses,
        "balance": income - expenses,
        "month": month,
        "year": year,
    }


@router.get("/expenses-by-category")
def expenses_by_category(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Expenses grouped by category for charts."""
    rows = (
        db.query(
            Category.name,
            Category.color,
            Category.icon,
            func.sum(Transaction.amount).label("total"),
        )
        .join(Transaction, Transaction.category_id == Category.id)
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == TransactionType.expense,
            extract("month", Transaction.date) == month,
            extract("year", Transaction.date) == year,
        )
        .group_by(Category.id)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )
    return [
        {"name": r.name, "color": r.color, "icon": r.icon, "total": Decimal(str(r.total))}
        for r in rows
    ]


@router.get("/monthly-trend")
def monthly_trend(
    year: int = Query(..., ge=2000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Monthly income vs expenses for the full year."""
    rows = (
        db.query(
            extract("month", Transaction.date).label("month"),
            Transaction.type,
            func.sum(Transaction.amount).label("total"),
        )
        .filter(
            Transaction.user_id == current_user.id,
            extract("year", Transaction.date) == year,
        )
        .group_by("month", Transaction.type)
        .order_by("month")
        .all()
    )

    data = {m: {"income": 0, "expense": 0} for m in range(1, 13)}
    for row in rows:
        data[int(row.month)][row.type.value] = float(row.total)

    return [{"month": m, **v} for m, v in data.items()]


@router.get("/recent-transactions")
def recent_transactions(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    txs = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
        .limit(limit)
        .all()
    )
    return txs
