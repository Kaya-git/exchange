from aiogram.types import Message
from aiogram import F
from aiogram.filters import Text
from telegram_bot.logic.keyboards.inline import inline
from ..fsm.finite_st_buyback import ExchangeStates
from aiogram import Router
from ..keyboards.reply import kb_main_menu, cancel_button
from aiogram.fsm.context import FSMContext
import logging
from database import Database
from src.middlewares import DatabaseMiddleware
from aiogram.types import CallbackQuery
from src.telegram_bot.utils.callbackdata import OperationInfo


buyback_router = Router(name="buyback")
buyback_router.message.middleware(DatabaseMiddleware())


@buyback_router.message(F.text == 'Обмен', ignore_case=True)
async def start_buy_back(message: Message, state: FSMContext) -> None:
    await state.set_state(ExchangeStates.user_uuid)
    await state.update_data(user_uuid=message.from_user.id)
    await message.answer(
        text="Выберите, какую операцию хотите совершить",
        reply_markup=await inline.operation_type_kb()
    )


@buyback_router.callback_query(F.action == "buy")
async def buy_crypto(query: CallbackQuery):
    await query.answer(
        reply_markup=await inline.get_buy_crypto()
    )


@buyback_router.callback_query(F.action == "sell")
async def sell_crypto(query: CallbackQuery):
    await query.answer(
        reply_markup=await inline.get_sell_crypto()
    )


@buyback_router.callback_query(F.operation == "buy")
async def payment_buy_currency(
    query: CallbackQuery,
    state: FSMContext,
    callback: OperationInfo
):
    await state.set_state(ExchangeStates.client_buy_tikker)
    await state.update_data(client_buy_tikker=callback.tikker)
    await state.set_state(ExchangeStates.client_buy_currency)
    await query.answer(
        text="Вы желаете ввести сумму",
        reply_markup=await inline.choose_curr_payment_type()
    )


@buyback_router.callback_query(F.operation == "sell")
async def payment_sell_currency(
    query: CallbackQuery,
    state: FSMContext,
    callback: OperationInfo
):
    await state.set_state(ExchangeStates.client_sell_tikker)
    await state.update_data(client_sell_tikker=callback.tikker)
    await state.set_state(ExchangeStates.client_sell_currency)
    await query.answer(
        text="Вы желаете ввести сумму",
        reply_markup=await inline.choose_curr_payment_type()
    )


@buyback_router.callback_query(F.operation == "sell")
















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
