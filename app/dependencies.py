from fastapi import Request
from datetime import datetime
from . import database
async def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    expires_at = request.session.get("expires_at")
    if expires_at:
        if datetime.now() > datetime.fromisoformat(expires_at):
            request.session.clear()
            return None
    user = await database.fetch_one(
        "SELECT * FROM users WHERE id = ?", 
        (user_id,)
    )
    return user