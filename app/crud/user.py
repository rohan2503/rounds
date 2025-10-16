from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models.user import User

async def get_user_by_phone(db: AsyncSession, phone_number: str):
    """Get user by phone number"""
    stmt = select(User).where(User.phone_number == phone_number)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int):
    """Get user by ID"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(
    db: AsyncSession,
    phone_number: str,
    full_name: str,
    registration_number: str = None,
    state_council: str = None,
    is_verified: bool = False
):
    """Create new user"""
    user = User(
        phone_number=phone_number,
        full_name=full_name,
        registration_number=registration_number,
        state_council=state_council,
        is_verified=is_verified
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_last_login(db: AsyncSession, user_id: int):
    """Update user's last login timestamp"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        user.last_login = datetime.utcnow()
        await db.commit()
    return user