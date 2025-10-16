from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.models.user import OTP
from app.core.config import settings

async def create_otp(db: AsyncSession, phone_number: str, otp_code: str):
    """Create new OTP record"""
    expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    
    otp = OTP(
        phone_number=phone_number,
        otp_code=otp_code,
        expires_at=expires_at
    )
    db.add(otp)
    await db.commit()
    await db.refresh(otp)
    return otp

async def verify_otp(db: AsyncSession, phone_number: str, otp_code: str) -> bool:
    """Verify OTP code"""
    stmt = select(OTP).where(
        OTP.phone_number == phone_number,
        OTP.otp_code == otp_code,
        OTP.is_used == False,
        OTP.expires_at > datetime.utcnow()
    ).order_by(OTP.created_at.desc())
    
    result = await db.execute(stmt)
    otp = result.scalar_one_or_none()
    
    if otp:
        # Mark OTP as used
        otp.is_used = True
        await db.commit()
        return True
    return False

async def invalidate_old_otps(db: AsyncSession, phone_number: str):
    """Mark all old OTPs as used"""
    stmt = select(OTP).where(
        OTP.phone_number == phone_number,
        OTP.is_used == False
    )
    result = await db.execute(stmt)
    otps = result.scalars().all()
    
    for otp in otps:
        otp.is_used = True
    
    await db.commit()