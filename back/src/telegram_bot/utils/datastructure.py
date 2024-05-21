from typing import Callable, TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession


from src.cache import Cache
from src.database import Database


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]
    db: Database
    bot: Bot
    cache: Cache
