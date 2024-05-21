from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Обмен'),
            KeyboardButton(text='Профиль')
        ],
        [
            KeyboardButton(text='Наши ресурсы'),
            KeyboardButton(text='Помощь')
        ]
    ],
    resize_keyboard=True
)


cancel_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)
