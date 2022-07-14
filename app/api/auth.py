from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.auth import UserCreate, Token, User
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import AuthService, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up", response_model=Token)
async def sign_up(user_data: UserCreate, service: AuthService = Depends()):
    return await service.register_new_user(user_data)


@router.post("/sign-in", response_model=Token)
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()
):
    return await service.authenticate_user(form_data.username, form_data.password)


@router.get("/user", response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user
