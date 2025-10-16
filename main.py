from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud import verify_doctor
from rate_limiter import init_redis, is_rate_limited

app = FastAPI(title="Doctor Verification API")

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis()

@app.post("/api/v1/verify")
async def verify_user(request: Request, 
                      payload: dict, 
                      db: AsyncSession = Depends(get_db)):
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing X-User-Id header")

    redis = app.state.redis
    if await is_rate_limited(redis, f"rl:{user_id}", limit=10, window=60):
        raise HTTPException(status_code=429, detail="Too many requests")

    required = {"registration_number", "name", "state_council", "qualification_year"}
    if not required.issubset(payload.keys()):
        raise HTTPException(status_code=400, detail="Missing fields")

    res = await verify_doctor(
        db, user_id,
        payload["registration_number"],
        payload["name"],
        payload["state_council"],
        payload["qualification_year"],
    )
    return res