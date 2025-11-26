from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    date: Optional[datetime] = None
    type: TransactionType
    payment_method: Optional[str] = None
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionInDBBase(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Transaction(TransactionInDBBase):
    pass
