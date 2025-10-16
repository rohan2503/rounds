from fastapi import Header, HTTPException

async def get_user_id(x_user_id: str = Header(None)) -> str:
    """Dependency to get user_id from header"""
    if not x_user_id:
        raise HTTPException(status_code=400, detail="Missing X-User-Id header")
    return x_user_id