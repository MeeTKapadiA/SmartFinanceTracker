from typing import Any, List, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import Transaction as TransactionSchema

router = APIRouter()

@router.get("/dashboard", response_model=Dict[str, Any])
def get_dashboard_data(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get financial dashboard data.
    """
    # 1. Total Expenses
    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == TransactionType.EXPENSE
    ).scalar() or 0.0

    # 2. Total Income
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == TransactionType.INCOME
    ).scalar() or 0.0

    # 3. Net Savings
    net_savings = total_income - total_expense

    # 4. Category Breakdown
    category_data = db.query(
        Transaction.category, func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == TransactionType.EXPENSE
    ).group_by(Transaction.category).all()
    
    category_breakdown = [{"category": c, "amount": a} for c, a in category_data]

    # 5. Recent Transactions
    recent_txs = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.date.desc()).limit(5).all()

    return {
        "total_expense": total_expense,
        "total_income": total_income,
        "net_savings": net_savings,
        "category_breakdown": category_breakdown,
        "recent_transactions": [TransactionSchema.model_validate(tx) for tx in recent_txs]
    }
