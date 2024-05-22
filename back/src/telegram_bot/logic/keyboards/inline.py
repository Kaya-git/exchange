from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import (
    ReturnToMenu,
    Profile,
    OperationType,
    TikkerName,
    DisplayPrice,
)
from handlers import get_crypto
from fsm.fsm_states import ExchangeStates
from aiogram.fsm.context import FSMContext


class InlineKeyboards:

    async def profile_kb():
        inline_keyboard_builder = InlineKeyboardBuilder()

        inline_keyboard_builder.button(
            text='Реферальная система',
            callback_data=Profile(
                action='ref'
            )
        )

        inline_keyboard_builder.button(
            text='Промокоды',
            callback_data=Profile(
                action='promo'
            )
        )

        inline_keyboard_builder.button(
            text='Скидки',
            callback_data=Profile(
                action='discount'
            )
        )

        inline_keyboard_builder.button(
            text='Вывод баланса',
            callback_data=Profile(
                action='withdrawal'
            )
        )

        inline_keyboard_builder.adjust(2, 2)
        return inline_keyboard_builder.as_markup()

    async def operation_type(state: FSMContext):
        inline_keyboard_builder = InlineKeyboardBuilder()
        inline_keyboard_builder.button(
            text='Купить валюту',
            callback_data=OperationType(
                operation_type='buy'
            )
        )

        inline_keyboard_builder.button(
            text='Продать валюту',
            callback_data=OperationType(
                operation_type='sell'
            )
        )

        inline_keyboard_builder.button(
            text='Главное меню',
            callback_data=ReturnToMenu(
                back=True
            )
        )

        inline_keyboard_builder.adjust(2, 1)
        return inline_keyboard_builder.as_markup()

    async def get_crypto_tikker(state: FSMContext):
        inline_keyboard_builder = InlineKeyboardBuilder()
        crypto_lst = await get_crypto()
        for i in crypto_lst:
            inline_keyboard_builder.button(
                text=f"{i["name"]}{i["tikker"]}",
                callback_data=TikkerName(
                    tikker=f"{i["tikker"]}"
                )
            )
        return inline_keyboard_builder.as_markup()

    async def display_price(currency_name: str):
        inline_keyboard_builder = InlineKeyboardBuilder()
        inline_keyboard_builder.button(
                text="В Рублях",
                callback_data=DisplayPrice(
                    tikker="RUB"
                )
            )
        inline_keyboard_builder.button(
                text=f"В {currency_name}",
                callback_data=DisplayPrice(
                    tikker=f"{currency_name}"
                )
            )
        return inline_keyboard_builder.as_markup()






inline_kb = InlineKeyboards()
