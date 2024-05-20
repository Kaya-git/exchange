from aiogram.types import Message
from aiogram.filters import CommandObject, Command
from .bot_commands import bot_commands
from aiogram import Router


help_router = Router(name="help")


@help_router.message(Command(commands=['help']))
async def help(message: Message, command: CommandObject):
    if command.args:
        for cmd in bot_commands:
            if cmd[0] == command.args:
                return await message.answer(
                    f'{cmd[0]} - {cmd[1]}\n\n{cmd[2]}'
                )
        else:
            return await message.answer('Команда не найдена')

    await message.answer(
        'Помощь и справка о боте\n'
        'Для того, чтобы получить информацию о команде используй /help\n'
    )
