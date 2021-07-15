from datetime import timedelta, datetime

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError

from my_finance import models
from my_finance.database import get_session
from my_finance.models.auth import UserCreate
from my_finance.settings import settings
from my_finance import tables
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.auth.User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, password, password_hash):
        return bcrypt.verify(password, password_hash)

    @classmethod
    def hash_password(cls, password) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> models.auth.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="could not validate credentials in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
            )
            user_data = payload.get("user")
            user = models.auth.User.parse_obj(user_data)

        except (JWTError, ValidationError) as e:
            raise exception from e
        else:
            return user

    @classmethod
    def create_token(cls, user: tables.User) -> models.auth.Token:
        user_data = models.auth.User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=settings.jwt_expiration),
            "sub": user_data.id.__str__(),
            "user": user_data.dict(),
        }
        token = jwt.encode(
            payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
        )

        return models.auth.Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: models.auth.UserCreate) -> models.auth.Token:
        user = tables.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )

        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> models.auth.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username is not found or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user = self.session.query(tables.User).filter_by(username=username).first()

        if not user or not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)
