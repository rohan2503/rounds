from fastapi import FastAPI
from app.core.config import settings
from app.core.rate_limiter import init_redis
from app.api.v1.router import api_router

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis()

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Doctor Verification API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}