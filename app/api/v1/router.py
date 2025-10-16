from fastapi import APIRouter
from app.api.v1.endpoints import verification

api_router = APIRouter()
api_router.include_router(verification.router, tags=["verification"])