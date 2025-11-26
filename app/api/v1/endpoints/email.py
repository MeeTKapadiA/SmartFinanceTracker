from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.services.email_service import email_service
from app.services.parser_service import parser_service
from app.crud import crud_transaction
from app.schemas.transaction import TransactionCreate
from app.models.transaction import TransactionType

router = APIRouter()

@router.post("/scan", response_model=dict)
def scan_emails(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
    limit: int = 10
) -> Any:
    """
    Scan emails for transactions and add them to the database.
    """
    # 1. Authenticate and fetch messages
    # Note: In a real app, we'd handle per-user tokens. 
    # Here we assume a single shared token or local flow for the MVP/Dev.
    if not email_service.authenticate():
        raise HTTPException(status_code=400, detail="Could not authenticate with Gmail")
    
    messages = email_service.get_messages(limit=limit)
    processed_count = 0
    added_count = 0
    
    for msg_body in messages:
        # Get body (simplified, real implementation needs to handle MIME parts better)
        body = email_service.get_message_body({"payload": {"body": {"data": msg_body['snippet']}}}) # Mocking structure for now or using snippet
        # Actually, get_messages in EmailService returns full message objects if implemented that way
        # Let's assume get_messages returns list of message details including snippet/payload
        
        # We need to fetch full content if get_messages only returns list
        # My EmailService.get_messages implementation fetches full content.
        
        # Extract body
        text = email_service.get_message_body(msg_body)
        if not text:
            text = msg_body.get('snippet', '')
            
        # 2. Parse
        data = parser_service.parse_email(text)
        
        if data:
            processed_count += 1
            # 3. Save
            # Check duplicates? (Simple check: same amount, date, description)
            # For now, just add.
            
            tx_in = TransactionCreate(
                amount=data['amount'],
                category=data['category'],
                description=data['description'],
                date=data['date'],
                type=TransactionType.EXPENSE,
                payment_method=data['payment_method']
            )
            crud_transaction.create_transaction(db, tx_in, current_user.id)
            added_count += 1
            
    return {"processed": processed_count, "added": added_count}
