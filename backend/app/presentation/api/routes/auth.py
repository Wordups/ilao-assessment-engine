from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.core.security import CurrentUser, get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def read_me(current_user: CurrentUser = Depends(get_current_user), settings: Settings = Depends(get_settings)) -> dict:
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "auth_mode": settings.auth_mode,
    }
