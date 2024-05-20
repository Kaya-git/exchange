from aiogram import Bot, Dispatcher, types
import asyncio
from config import conf
import logging
from aiogram.filters import CommandStart
from logic.callback import part_number_router
from logic.smth_else import smth_else_router
from logic.back import back_router
from keyboards.inline import get_inline_keyboard


async def start_bot():
    bot = Bot(token=conf.bot.token)
    cache = Cache()

