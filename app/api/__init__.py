from fastapi import APIRouter
from app.api.operations import router as operations_router
from app.api.auth import router as auth_router

router = APIRouter()

router.include_router(operations_router)
router.include_router(auth_router)
