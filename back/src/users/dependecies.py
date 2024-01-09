from datetime import datetime

from config import conf
from database.db import Database
from exceptions import (IncorrectTokenException, TokenAbsentException,
                        TokenExpiredException, UserIsNotPresentException)
from fastapi import Depends, Request
from jose import JWTError, jwt
from users.models import User


def get_token(request: Request):
    token = request.cookies.get("admin_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    db = Database()
    try:
        payload = jwt.decode(token, conf.auth.jwt_token, conf.auth.algorithm)
    except JWTError:
        raise IncorrectTokenException
    # Check token expiration
    expire = payload.get("exp")
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    # Check if the token and user match
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    # Check if user is present in database
    user = await db.user.get_curr_user(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def get_current_admin_user(
        current_user: User = Depends(get_current_user)
):
    return current_user
