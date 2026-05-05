from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType
from app.schemas.budget import BudgetWithSpending


def get_budget_spending(db: Session, budget: Budget) -> BudgetWithSpending:
    """Calculate spending for a given budget period."""
    spent_result = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == budget.user_id,
            Transaction.category_id == budget.category_id,
            Transaction.type == TransactionType.expense,
            func.extract("month", Transaction.date) == budget.month,
            func.extract("year", Transaction.date) == budget.year,
        )
        .scalar()
    )

    spent = Decimal(str(spent_result))
    remaining = budget.amount - spent
    percentage = float((spent / budget.amount * 100)) if budget.amount > 0 else 0.0
    is_over = spent > budget.amount
    is_alert = percentage >= float(budget.alert_threshold)

    return BudgetWithSpending(
        **{c.key: getattr(budget, c.key) for c in budget.__table__.columns},
        category=budget.category,
        spent=spent,
        remaining=remaining,
        percentage=round(percentage, 2),
        is_over_budget=is_over,
        is_alert_triggered=is_alert,
    )


def check_and_flag_budget_alerts(db: Session, user_id, month: int, year: int) -> list[Budget]:
    """Check all budgets for a user/month and flag those over threshold."""
    triggered = []
    budgets = (
        db.query(Budget)
        .filter(Budget.user_id == user_id, Budget.month == month, Budget.year == year)
        .all()
    )
    for budget in budgets:
        info = get_budget_spending(db, budget)
        if info.is_alert_triggered and not budget.alert_sent:
            budget.alert_sent = True
            triggered.append(budget)
    db.commit()
    return triggered
