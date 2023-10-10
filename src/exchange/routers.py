from fastapi import APIRouter, Cookie, Depends
from fastapi.responses import RedirectResponse
from .sevices import services
from database.db import Database, get_async_session
from binance_parser import find_price
from database.models import (
    Currency, Review,
    ServicePaymentOption,
    Order, Status
)
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy import select, update
from pprint import pprint
from decimal import Decimal

currency_router = APIRouter(
    tags=["валютный роутер"]
)

menu_router = APIRouter(
    tags=["роутер кнопок меню"]
)

exhange_router = APIRouter(
    prefix="/exchange",
    tags=["роутер цепочки обмена"]
)


# -----------------------------------------------------------------------------
@exhange_router.get("/confirm")
async def confirm_order(
    user_uuid: str | None = Cookie(default=None),
    # session: AsyncSession = Depends(get_async_session)
):
    # db = Database(session=session)

    """ Проверяем есть ли ключи в реддисе и забираем значения """
    does_exist = await services.redis_values.redis_conn.exists(user_uuid)
    if does_exist != 1:
        return "Время вышло"

    (
        client_crypto_wallet,
        client_cc_holder,
        client_credit_card_number,
        client_buy_currency_tikker,
        client_buy_value,
        client_sell_currency_tikker,
        client_sell_value,
        client_email
    ) = await services.redis_values.redis_conn.lrange(user_uuid, 0, -1)

    """ Декодируем из бит в пайтоновские значения """
    client_crypto_wallet = str(client_crypto_wallet, 'UTF-8')
    client_cc_holder = str(client_cc_holder, 'UTF-8')
    client_credit_card_number = str(client_credit_card_number, 'UTF-8')
    client_buy_currency_tikker = str(client_buy_currency_tikker, 'UTF-8')
    client_buy_value = str(client_buy_value, 'UTF-8')
    client_sell_currency_tikker = str(client_sell_currency_tikker, 'UTF-8')
    client_sell_value = str(client_sell_value, 'UTF-8')
    client_email = str(client_email, 'UTF-8')
    client_buy_value = Decimal(client_buy_value)
    client_sell_value = Decimal(client_sell_value)

    return {
        "client_crypto_wallet": client_crypto_wallet,
        "client_cc_holder_name": client_cc_holder,
        "client_cc_num": client_credit_card_number,
        "client_get_tikker_name": client_buy_currency_tikker,
        "client_get_value": client_buy_value,
        "client_send_tikker_name": client_sell_currency_tikker,
        "client_send_value": client_sell_value,
        "client_email": client_email
    }


@exhange_router.get("/await")
async def conformation_await(
    user_uuid: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
) -> RedirectResponse:

    db = Database(session=async_session)
    paralel_waiting = asyncio.create_task(
        services.db_paralell.conformation_await(
            db,
            user_uuid
        )
    )
    await paralel_waiting


@exhange_router.get("/order/{order_id}")
async def requisites(
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Cookie(default=None),
):
    db = Database(session=async_session)

    """ Достаем из редиса тикер заказа"""
    order_id = (
        await services.redis_values.redis_conn.lrange(
            user_uuid,
            0,
            -1,
        )
    )
    order_id = int(*order_id)

    pprint(
        f"{order_id}:{type(order_id)}"
    )

    """ Находим в таблице ServicePaymentOption способ оплаты
    с тикером подходящим для продажу клиент"""
    statement = (
        select(
            ServicePaymentOption
            ).join(
            Currency, ServicePaymentOption.currency_tikker == Currency.tikker
            ).join(
                Order, Currency.tikker == Order.sell_currency_tikker
            ).where(
                Order.id == order_id
                )
    )

    service_payment_option = await db.session.execute(statement=statement)
    service_payment_option = service_payment_option.scalar_one_or_none()

    pprint(service_payment_option)

    # try:
    return {
            "requisites_num": service_payment_option.number,
            "holder": service_payment_option.holder
        }
    # except KeyError("Ключ не найден, нужен новый ордер"):
    #     return "Ключ не найден, нужен новый ордер"


@exhange_router.get("/payed")
async def payed_button(
    async_session: AsyncSession = Depends(get_async_session),
    user_uuid: str | None = Cookie(default=None),
):
    db = Database(session=async_session)
    """ Проверяем редис на наличие ключей,
    если исчезли, то ставим статус ордера на просрок"""
    does_exist = await services.redis_values.redis_conn.exists(user_uuid)
    order_id = await services.redis_values.redis_conn.lindex(
        user_uuid,
        0
    )
    order_id = int(order_id)
    if not does_exist:
        statement = (
            update(Order).
            where(Order.id == order_id).
            values(status=Status.Timeout)
        )
        await db.session.execute(statement)
        return "Время вышло, по новой"

    try:
        resp = asyncio.create_task(
            await services.db_paralell.payed_button_db(
                db=db,
                user_uuid=user_uuid,
                order_id=order_id
            )
        )
    except Exception:
        return "Ошибка"
    return resp


# # --------------------------------------------------------------------------


@menu_router.get("/siterules")
async def siterules():
    ...


@menu_router.get("/reserve")
async def reserve(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    currency_list = await db.currency.get_all()
    return_dict = {}
    for currency in currency_list:
        return_dict[currency.name] = (currency.name, currency.reserve)
    return return_dict


@menu_router.get("/tarifs")
async def tarifs():
    return {
        "btc": f"{find_price('BTCRUB')}",
        "ltc": f"{find_price('LTCRUB')}",
    }


@menu_router.get("/faq")
async def faq():
    ...


@menu_router.get("/reviews/list")
async def reviews_all(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    try:
        reviews = await db.review.get_many(limit=10, order_by=Review.data)
        return reviews
    except KeyError("Ошибка в получении ревью"):
        return ("Ошибка в получении ревью")


@menu_router.get("/contacts")
async def contacts():
    ...
