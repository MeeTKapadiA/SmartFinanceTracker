from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def get_transactions(
    db: Session, user_id: int, skip: int = 0, limit: int = 100, type: Optional[str] = None
) -> List[Transaction]:
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if type:
        query = query.filter(Transaction.type == type)
    return query.offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction(db: Session, transaction_id: int, user_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()

def remove_transaction(db: Session, transaction_id: int, user_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()
    if transaction:
        db.delete(transaction)
        db.commit()
    return transaction
