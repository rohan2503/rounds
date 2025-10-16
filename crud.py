from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from difflib import SequenceMatcher
from models import Doctor, VerificationAttempt

async def verify_doctor(db: AsyncSession, user_id: str, reg_num: str, name: str, state: str, year: int):
    stmt = select(Doctor).where(
        Doctor.registration_number == reg_num,
        Doctor.state_council == state
    )
    result = await db.execute(stmt)
    doctors = result.scalars().all()

    best_score = 0
    for doc in doctors:
        name_sim = SequenceMatcher(None, doc.name.lower(), name.lower()).ratio()
        year_diff = abs((doc.year_of_info or 0) - year)
        year_score = max(0, 1 - (year_diff / 5))
        score = (name_sim * 0.8 + year_score * 0.2) * 100
        best_score = max(best_score, score)

    verified = best_score >= 85
    attempt = VerificationAttempt(
        user_id=user_id,
        registration_number=reg_num,
        name=name,
        state_council=state,
        qualification_year=year,
        score=int(best_score),
        verified=verified,
    )
    db.add(attempt)
    await db.commit()
    return {"verified": verified, "score": int(best_score)}
