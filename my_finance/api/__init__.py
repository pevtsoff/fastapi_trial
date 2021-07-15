from fastapi import APIRouter
from my_finance.api.operations import router as operations_router
from my_finance.api.auth import router as auth_router

router = APIRouter()

router.include_router(operations_router)
router.include_router(auth_router)
