from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import (
    ReturnToMenu,
    Profile,
    OperationType,
    TikkerName,
    DisplayPrice,
    CorrectOrder,
    Payed
)
from handlers import get_crypto
from aiogram.fsm.context import FSMContext


class InlineKeyboards:

    inline_keyboard_builder = InlineKeyboardBuilder()

    async def profile_kb(self):
        self.inline_keyboard_builder.button(
            text='Реферальная система',
            callback_data=Profile(
                action='ref'
            )
        )

        self.inline_keyboard_builder.button(
            text='Промокоды',
            callback_data=Profile(
                action='promo'
            )
        )

        self.inline_keyboard_builder.button(
            text='Скидки',
            callback_data=Profile(
                action='discount'
            )
        )

        self.inline_keyboard_builder.button(
            text='Вывод баланса',
            callback_data=Profile(
                action='withdrawal'
            )
        )

        self.inline_keyboard_builder.adjust(2, 2)
        return self.inline_keyboard_builder.as_markup()

    async def operation_type(self, state: FSMContext):

        self.inline_keyboard_builder.button(
            text='Купить валюту',
            callback_data=OperationType(
                operation_type='buy'
            )
        )

        self.inline_keyboard_builder.button(
            text='Продать валюту',
            callback_data=OperationType(
                operation_type='sell'
            )
        )

        self.inline_keyboard_builder.button(
            text='Главное меню',
            callback_data=ReturnToMenu(
                back=True
            )
        )

        self.inline_keyboard_builder.adjust(2, 1)
        return self.inline_keyboard_builder.as_markup()

    async def get_crypto_tikker(self, state: FSMContext):
        crypto_lst = await get_crypto()
        for i in crypto_lst:
            self.inline_keyboard_builder.button(
                text=f"{i["name"]}{i["tikker"]}",
                callback_data=TikkerName(
                    tikker=f"{i["tikker"]}"
                )
            )
        return self.inline_keyboard_builder.as_markup()

    async def display_price(self, currency_name: str):
        self.inline_keyboard_builder.button(
                text="В Рублях",
                callback_data=DisplayPrice(
                    tikker="RUB"
                )
            )
        self.inline_keyboard_builder.button(
                text=f"В {currency_name}",
                callback_data=DisplayPrice(
                    tikker=f"{currency_name}"
                )
            )
        return self.inline_keyboard_builder.as_markup()

    async def correct_order(self):
        self.inline_keyboard_builder.button(
            text="Да",
            callback_data=CorrectOrder(
                reply=True
            )
        )
        self.inline_keyboard_builder.button(
            text="Нет",
            callback_data=CorrectOrder(
                reply=False
            )
        )
        return self.inline_keyboard_builder.as_markup()

    async def payed(self):
        self.inline_keyboard_builder.button(
            text="Оплатил",
            callback_data=Payed(
                payed=True
            )
        )
        return self.inline_keyboard_builder.as_markup()


inline_kb = InlineKeyboards()
