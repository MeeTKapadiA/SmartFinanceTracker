from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_transaction
from app.api import deps
from app.schemas.transaction import Transaction, TransactionCreate
from app.models.transaction import TransactionType

router = APIRouter()

@router.get("/", response_model=List[Transaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    type: Optional[TransactionType] = None,
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve transactions.
    """
    transactions = crud_transaction.get_transactions(
        db, user_id=current_user.id, skip=skip, limit=limit, type=type
    )
    return transactions

@router.post("/", response_model=Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: TransactionCreate,
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new transaction.
    """
    transaction = crud_transaction.create_transaction(
        db=db, transaction=transaction_in, user_id=current_user.id
    )
    return transaction

@router.delete("/{id}", response_model=Transaction)
def delete_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a transaction.
    """
    transaction = crud_transaction.remove_transaction(
        db=db, transaction_id=id, user_id=current_user.id
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
