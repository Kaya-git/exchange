from aiogram.types import Message
from aiogram import F
from aiogram.filters import Text
from telegram_bot.logic.keyboards.inline import inline_kb
from ..fsm.finite_st_buyback import ExchangeStates
from aiogram import Router
from ..keyboards.reply import kb_main_menu, cancel_button
from aiogram.fsm.context import FSMContext
import logging
from database import Database
from src.exchange.routers import fill_order_form
from src.middlewares import DatabaseMiddleware
from aiogram.types import CallbackQuery
from src.telegram_bot.utils.callbackdata import (
    OperationType,
    TikkerName,
    DisplayPrice,
    Verification,
    CreditCard,
    CryptoWallet
)


buyback_router = Router(name="buyback")
buyback_router.message.middleware(DatabaseMiddleware())


@buyback_router.message(F.text == 'Обмен', ignore_case=True)
async def start_buy_back(message: Message, state: FSMContext) -> None:

    await state.set_state(ExchangeStates.user_uuid)
    await state.update_data(user_uuid=message.from_user.id)

    await state.set_state(ExchangeStates.client_email)
    await state.update_data(client_email=None)

    await state.set_state(ExchangeStates.client_buy_value)
    await state.update_data(client_buy_value=0)

    await state.set_state(ExchangeStates.client_sell_value)
    await state.update_data(client_sell_value=0)

    await message.answer(
        text="Выберите, какую операцию хотите совершить",
        reply_markup=await inline_kb.operation_type()
    )


@buyback_router.callback_query(OperationType.filter(F.prefix == "operation"))
async def get_crypto_tikkers(
    query: CallbackQuery,
    state: FSMContext,
    callback: OperationType
):
    await state.set_state(ExchangeStates.operation_type)
    await state.update_data(operation_type=callback.operation_type)
    await query.answer(
        text="Выберите валюту",
        reply_markup=await inline_kb.get_crypto_tikker()
    )


@buyback_router.callback_query(TikkerName.filter(F.prefix == "tikker"))
async def sell_crypto(
    query: CallbackQuery,
    state: FSMContext,
    callback: TikkerName
):
    if state.operation_type == "sell":

        await state.set_state(ExchangeStates.client_sell_tikker)
        await state.update_data(client_sell_tikker=callback.tikker)

        await state.set_state(ExchangeStates.client_buy_tikker)
        await state.update_data(client_buy_tikker="RUB")

    if state.operation_type == "buy":

        await state.set_state(ExchangeStates.client_buy_tikker)
        await state.update_data(client_buy_tikker=callback.tikker)

        await state.set_state(ExchangeStates.client_sell_tikker)
        await state.update_data(client_sell_tikker="RUB")

    await query.answer(
        text="Вы желаете ввести сумму",
        reply_markup=await inline_kb.display_price(
            currency_name=callback.tikker
        )
    )


@buyback_router.callback_query(DisplayPrice.filter(F.prefix == "display"))
async def payment_sell_currency(
    query: CallbackQuery,
    state: FSMContext,
    callback: DisplayPrice
):
    await state.set_state(ExchangeStates.display_price)
    await state.update_data(display_price=callback.tikker)

    await state.set_state(ExchangeStates.money_amount)

    await query.answer(
        text=f"Введите нужную сумму в {callback.tikker}",
    )


@buyback_router.message(ExchangeStates.money_amount)
async def credit_card_num(
    message: Message,
    state: FSMContext,
):

    await state.update_data(money_amount=message.text)

    if state.operation_type == "buy":

        if state.display_price == "RUB":
            await state.set_data(ExchangeStates.client_sell_value)
            await state.update_data(client_sell_value=state.money_amount)

        if state.display_price != "RUB":
            await state.set_data(ExchangeStates.client_sell_value)
            await state.update_data(client_sell_value=state.money_amount)

    if state.operation_type == "sell":

        if state.display_price == "RUB":
            await state.set_data(ExchangeStates.client_buy_value)
            await state.update_data(client_buy_value=state.money_amount)

        if state.display_price != "RUB":
            await state.set_data(ExchangeStates.client_sell_value)
            await state.update_data(client_sell_value=state.money_amount)

    await state.set_data(ExchangeStates.client_credit_card_number)
    await message.reply(
        text="Введите реквизиты вашей банковской карты"
    )


@buyback_router.message(ExchangeStates.client_credit_card_number)
async def credit_card_owner(
    message: Message,
    state: FSMContext,
):
    await state.update_data(client_credit_card_number=message.text)
    await state.set_state(ExchangeStates.client_cc_holder)
    await message.reply(
        text="Введите владельца как указано на карте"
    )


@buyback_router.message(ExchangeStates.client_cc_holder)
async def crypto_wallet(
    message: Message,
    state: FSMContext,
):
    await state.update_data(client_cc_holder=message.text)
    await state.set_state(ExchangeStates.client_crypto_wallet)
    await message.reply(
        text="Введите криптовалютный кошелек"
    )


@buyback_router.message(ExchangeStates.client_crypto_wallet)
async def create_order(
    message: Message,
    state: FSMContext,
):
    await state.update_data(client_crypto_wallet=message.text)
    await state.set_state(ExchangeStates.client_crypto_wallet)
    await fill_order_form(
        client_sell_value=state.client_sell_value,
        client_sell_tikker=state.client_sell_tikker,
        client_buy_value=state.client_buy_value,
        client_buy_tikker=state.client_buy_tikker,
        client_email=state.client_email,
        client_crypto_wallet=state.client_crypto_wallet,
        client_credit_card_number=state.client_credit_card_number,
        client_cc_holder=state.client_cc_holder,
        user_uuid=state.user_uuid
    )
    await state.clear()

    await message.reply(
        text="Создали заявку"
    )







# @buyback_router.callback_query(F.data == "sell")
# async def buy_crypto(callback_query: CallbackQuery):
#     await callback_query.answer(
#         reply_markup=await inline.get_av_crypto()
#     )




# @buyback_router.message(Text(text=['Отмена']))
# async def cancel(message: Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return

#     logging.info("Cancelling state %r", current_state)
#     await state.clear()

#     await message.answer(
#         text='Отмена',
#         reply_markup=kb_main_menu
#     )
#     await message.delete()


# @buyback_router.message(BuyBackStates.key_word)
# async def load_product_link(message: Message, state: FSMContext):
#     await state.update_data(key_word=message.text)
#     await state.set_state(BuyBackStates.product_link)
#     await message.reply(
#         "Скинь ссылку на страницу продукта, для продвижения",
#         reply_markup=in
#     )


# @buyback_router.message(BuyBackStates.product_link)
# async def item_size(message: Message, state: FSMContext):
#     await state.update_data(product_link=message.text)
#     await state.set_state(BuyBackStates.item_size)
#     await message.reply(
#         'Укажи размер товара',
#         reply_markup=cancel_button
#     )


# @buyback_router.message(BuyBackStates.item_size)
# async def buy_back_amount(message: Message, state: FSMContext):
#     await state.update_data(item_size=message.text)
#     await state.set_state(BuyBackStates.bb_amount)
#     await message.reply(
#         'Укажи кол-во требуемых выкупов',
#         reply_markup=cancel_button
#     )


# @buyback_router.message(BuyBackStates.bb_amount)
# async def lets_ride(message: Message, state: FSMContext, db: Database):
#     await state.update_data(bb_amount=message.text)
#     user_data = await state.get_data()

#     await db.buyback.new(
#         key_word=user_data["key_word"],
#         product_link=user_data["product_link"],
#         item_size=user_data["item_size"],
#         bb_amount=int(user_data["bb_amount"]),
#         user_id=message.from_user.id
#     )
#     await db.session.commit()
#     await message.reply(
#         f"Ваш заказ по ключевому слову: {user_data['key_word']}\n"
#         f"ссылка на товар: {user_data['product_link']}\n"
#         f"размер товара: {user_data['item_size']}\n"
#         f"кол-во выкупов: {user_data['bb_amount']}\n",
#         reply_markup=kb_main_menu
#     )

#     await state.clear()
