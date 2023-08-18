from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database.db import create_session_maker
from database.models import User
from fastapi_users.db import SQLAlchemyUserDatabase
from typing import AsyncGenerator
from database.db import create_session_maker


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with create_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
