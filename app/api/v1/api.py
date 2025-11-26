from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, transactions, email, analytics

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(email.router, prefix="/email", tags=["email"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
