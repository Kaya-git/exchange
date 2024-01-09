from datetime import datetime, timedelta
from typing import Union

from config import conf
from database.db import Database
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        data: dict, expires_delta: Union[timedelta, None] = None
        ) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, conf.auth.jwt_token, algorithm=conf.auth.algorithm
    )
    return encoded_jwt


async def authenticate_admin(email: EmailStr, password: str):
    db = Database()
    user = await db.user.find_by_email(email=email)
    if user and verify_password(password, user.hashed_password):
        return user
