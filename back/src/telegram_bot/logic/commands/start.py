from aiogram.types import Message
from src.logic.keyboards.reply import kb_main_menu
from aiogram import Router
from aiogram.filters import Command
from database import Database
from middlewares import DatabaseMiddleware


start_router = Router(name="start")
start_router.message.middleware(DatabaseMiddleware())


@start_router.message(Command(commands=['start']))
async def start(message: Message, db: Database) -> None:
    """
    Хендлер на команду старта
    """

    await db.user.new(
        user_id=message.from_user.id,
        user_name=message.from_user.username,
    )

    await db.session.commit()
    await message.answer('Главное меню', reply_markup=kb_main_menu)
    await message.delete()
