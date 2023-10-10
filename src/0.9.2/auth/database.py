from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database.models import User
from fastapi_users.db import SQLAlchemyUserDatabase
from database.db import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
