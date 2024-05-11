from fastapi import APIRouter

from api.users import router as users_router

router = APIRouter()

router.include_router(users_router)
