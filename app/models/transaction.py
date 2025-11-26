from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class TransactionType(str, enum.Enum):
    EXPENSE = "expense"
    INCOME = "income"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True) # Merchant or Source
    date = Column(DateTime, default=datetime.utcnow, index=True)
    type = Column(String, nullable=False) # expense or income
    payment_method = Column(String, nullable=True) # UPI, Card, Cash
    notes = Column(String, nullable=True)

    user = relationship("User", backref="transactions")
