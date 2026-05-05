from uuid import UUID
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.transaction import Transaction, TransactionType
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate, TransactionPage

router = APIRouter(prefix="/transactions", tags=["transactions"])


def _get_or_404(tx_id: UUID, user_id, db: Session) -> Transaction:
    tx = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == user_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.get("", response_model=TransactionPage)
def list_transactions(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    type: Optional[TransactionType] = None,
    category_id: Optional[UUID] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Transaction).filter(Transaction.user_id == current_user.id)

    if type:
        q = q.filter(Transaction.type == type)
    if category_id:
        q = q.filter(Transaction.category_id == category_id)
    if date_from:
        q = q.filter(Transaction.date >= date_from)
    if date_to:
        q = q.filter(Transaction.date <= date_to)
    if search:
        q = q.filter(Transaction.description.ilike(f"%{search}%"))

    total = q.count()
    items = q.order_by(Transaction.date.desc()).offset((page - 1) * size).limit(size).all()

    return TransactionPage(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=-(-total // size),
    )


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = Transaction(**payload.model_dump(), user_id=current_user.id)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.get("/{tx_id}", response_model=TransactionRead)
def get_transaction(
    tx_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_or_404(tx_id, current_user.id, db)


@router.patch("/{tx_id}", response_model=TransactionRead)
def update_transaction(
    tx_id: UUID,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = _get_or_404(tx_id, current_user.id, db)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tx, key, value)
    db.commit()
    db.refresh(tx)
    return tx


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    tx_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = _get_or_404(tx_id, current_user.id, db)
    db.delete(tx)
    db.commit()
