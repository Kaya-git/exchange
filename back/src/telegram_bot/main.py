from aiogram import Bot
import asyncio
from dispatcheres import get_redis_storage, get_dispatcher
from src.utils.data_structure import TransferData
from src.cache import Cache
from src.config import conf
from src.database.database import create_session_maker
import logging


async def start_bot():
    """
    This function will start bot with polling mode
    """
    bot = Bot(token=conf.bot.token)
    cache = Cache()
    storage = get_redis_storage(redis=cache.redis_client)
    dp = get_dispatcher(storage=storage)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(pool=create_session_maker(), cache=cache)
    )


if __name__ == "__main__":
    logging.basicConfig(level=conf.logging_level)
    asyncio.run(start_bot())
