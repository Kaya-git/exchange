from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import AccountInfo, OperationInfo, ValueIn
from handlers import get_crypto


class InlineKeyboards:
    async def profile_kb():
        inline_keyboard_builder = InlineKeyboardBuilder()
        inline_keyboard_builder.button(
            text='Реферальная система',
            callback_data=AccountInfo(
                action='ref'
            )
        )
        inline_keyboard_builder.button(
            text='Промокоды',
            callback_data=AccountInfo(
                action='promo'
            )
        )
        inline_keyboard_builder.button(
            text='Скидки',
            callback_data=AccountInfo(
                action='discount'
            )
        )
        inline_keyboard_builder.button(
            text='Вывод баланса',
            callback_data=AccountInfo(
                action='withdrawal'
            )
        )
        inline_keyboard_builder.adjust(2, 2)
        return inline_keyboard_builder.as_markup()

    async def operation_type_kb():
        inline_keyboard_builder = InlineKeyboardBuilder()
        inline_keyboard_builder.button(
            text='Купить валюту',
            callback_data=AccountInfo(
                action='buy'
            )
        )
        inline_keyboard_builder.button(
            text='Продать валюту',
            callback_data=AccountInfo(
                action='sell'
            )
        )
        inline_keyboard_builder.button(
            text='Главное меню',
            callback_data=AccountInfo(
                action='main_menu'
            )
        )
        inline_keyboard_builder.adjust(2, 1)
        return inline_keyboard_builder.as_markup()

    async def get_buy_crypto():
        inline_keyboard_builder = InlineKeyboardBuilder()
        crypto_lst = await get_crypto()
        for i in crypto_lst:

            inline_keyboard_builder.button(
                text=f"{i["name"]}{i["tikker"]}",
                callback_data=OperationInfo(
                    operation="buy",
                    tikker=f"{i["tikker"]}"
                )
            )
        return inline_keyboard_builder.as_markup()

    async def get_sell_crypto():
        inline_keyboard_builder = InlineKeyboardBuilder()
        crypto_lst = await get_crypto()
        for i in crypto_lst:

            inline_keyboard_builder.button(
                text=f"{i["name"]}{i["tikker"]}",
                callback_data=OperationInfo(
                    operation="sell",
                    tikker=f"{i["tikker"]}"
                )
            )
        return inline_keyboard_builder.as_markup()

    async def choose_curr_payment_type(currency_name: str):
        inline_keyboard_builder = InlineKeyboardBuilder()
        inline_keyboard_builder.button(
                text="В Рублях",
                callback_data=ValueIn(
                    currency="RUB"
                )
            )
        inline_keyboard_builder.button(
                text=f"В {currency_name}",
                callback_data=AccountInfo(
                    action=f"{currency_name}"
                )
            )
        return inline_keyboard_builder.as_markup()


inline = InlineKeyboards()
