import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Text, Enum as SAEnum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(SAEnum(TransactionType), nullable=False)
    description = Column(String(255), nullable=False)
    note = Column(Text, nullable=True)
    date = Column(Date, nullable=False, index=True)
    tags = Column(ARRAY(String), default=list, nullable=False)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
