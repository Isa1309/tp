from fastapi import APIRouter

from api.users import router as users_router
from api.animals import router as animals_router
from api.pets import router as pets_router
from api.schedules import router as schedules_router
from api.tasks import router as tasks_router
from api.medical_info import router as medical_info_router

router = APIRouter()

router.include_router(users_router)
router.include_router(animals_router)
router.include_router(pets_router)
router.include_router(schedules_router)
router.include_router(tasks_router)
router.include_router(medical_info_router)
