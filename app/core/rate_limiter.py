try:
    from redis import asyncio as aioredis
except Exception:
    aioredis = None
from app.core.config import settings  # CHANGE: import settings

async def init_redis():
    if aioredis is None:
        print("⚠️ Redis client not installed, rate limiting disabled")
        return None
    try:
        return aioredis.from_url(settings.REDIS_URL)  # CHANGE: use settings
    except Exception as e:
        print("⚠️ Redis not available, rate limiting disabled:", e)
        return None

async def is_rate_limited(redis, key: str, limit: int, window: int) -> bool:
    if not redis:
        return False
    current = await redis.incr(key)
    if int(current) == 1:
        await redis.expire(key, window)
    return current > limit