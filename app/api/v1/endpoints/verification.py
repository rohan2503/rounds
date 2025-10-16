from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud.doctor import verify_doctor
from app.schemas.verification import VerificationRequest, VerificationResponse
from app.core.rate_limiter import is_rate_limited
from app.core.config import settings
from app.api.deps import get_user_id

router = APIRouter()

@router.post("/verify", response_model=VerificationResponse)
async def verify_user(
    request: Request,
    payload: VerificationRequest,
    user_id: str = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Verify doctor credentials"""
    redis = request.app.state.redis
    
    # Rate limiting
    if await is_rate_limited(
        redis, 
        f"rl:{user_id}", 
        limit=settings.RATE_LIMIT_REQUESTS, 
        window=settings.RATE_LIMIT_WINDOW
    ):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    # Verify doctor
    result = await verify_doctor(
        db, 
        user_id,
        payload.registration_number,
        payload.name,
        payload.state_council,
        payload.qualification_year,
    )
    
    return result