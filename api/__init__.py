from fastapi import APIRouter

from api.user import router as user_router
from api.registration.auth import router as login_router


router = APIRouter()
router.include_router(user_router, prefix="/api/users", tags=["Users"])
router.include_router(login_router, prefix="/api/registration", tags=["Registration"])


__all__ = ["router"]
