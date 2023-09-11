from fastapi import APIRouter, Cookie, Response, Depends
from fastapi.responses import RedirectResponse
from .sevices import services
from database.models.router_enum import Tikker
from database.db import Database, get_async_session
from binance_parser import find_price
from database.models import (
    Currency, Review,
    PendingOrder, Status,
    PaymentBelonging, PaymentOption
)
import time
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy import select
from pprint import pprint


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
    user_id: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=session)
    does_exist = await services.redis_values.redis_conn.exists(user_id)
    # Проверяем есть ли ключи в реддисе
    if does_exist != 1:
        return "Время вышло"

    (
        client_crypto_wallet,
        client_cc_holder_name,
        client_cc_num,
        get_tikker_id,
        client_get_value,
        send_tikker_id,
        client_send_value,
        client_email
    ) = await services.redis_values.redis_conn.lrange(user_id, 0, -1)

    client_crypto_wallet = str(client_crypto_wallet, 'UTF-8')
    client_cc_holder_name = str(client_cc_holder_name, 'UTF-8')
    client_cc_num = str(client_cc_num, 'UTF-8')
    get_tikker_id = int(get_tikker_id)
    client_get_value = float(client_get_value)
    send_tikker_id = int(send_tikker_id)
    client_send_value = float(client_send_value)
    client_email = str(client_email, 'UTF-8')
    bart_for_one = (client_send_value) / client_get_value

    get_tikker_name = await db.currency.get_by_where(
        Currency.tikker_id == get_tikker_id
    )
    send_tikker_name = await db.currency.get_by_where(
        Currency.tikker_id == send_tikker_id
    )

    return {
        "client_crypto_wallet": client_crypto_wallet,
        "bart_for_one": bart_for_one,
        "client_cc_holder_name": client_cc_holder_name,
        "client_cc_num": client_cc_num,
        "client_get_tikker_name": get_tikker_name.name,
        "client_get_value": client_get_value,
        "client_send_tikker_name": send_tikker_name.name,
        "client_send_value": client_send_value,
        "client_email": client_email
    }


@exhange_router.get("/await")
async def conformation_await(
    user_id: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
) -> RedirectResponse:
    db = Database(session=async_session)
    paralel_waiting = asyncio.create_task(
        services.db_paralell.db_pooling(db, user_id)
    )
    await paralel_waiting


@exhange_router.get("/order/{order_id}")
async def requisites(
    async_session: AsyncSession = Depends(get_async_session),
    user_id: str | None = Cookie(default=None),
):
    client_give_currency_id = await services.redis_values.redis_conn.get(
        user_id
    )
    pprint(client_give_currency_id)
    client_give_currency_id = int(client_give_currency_id)
    db = Database(session=async_session)
    statement = select(
        PaymentOption
    ).where(
        PaymentOption.currency_id == client_give_currency_id
    ).where(
        PaymentOption.clien_service_belonging == PaymentBelonging.Service
    ).join(PaymentOption.currency)
    service_payment_option = await db.session.execute(statement=statement)
    service_payment_option = service_payment_option.scalar_one_or_none()
    return {
        "requisites_num": service_payment_option.cc_num_x_wallet,
        "holder": service_payment_option.cc_holder
    }


@exhange_router.get("/payed")
async def payed_button(
    order_id: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session),
    user_id: str | None = Cookie(default=None),
):
    db = Database(session=async_session)
    does_exist = await services.redis_values.redis_conn.exists(user_id)
    if not does_exist:
        db.pending_order.delete(PendingOrder.user_uuid == user_id)
        return "Время вышло, по новой"
    
    
    while True:
        await time.sleep(30)
        pending_order = await db.pending_order.get_by_where(
            PendingOrder.id == order_id
        )
        if pending_order.status == Status.Completed:
            completed_order = db.order.new(
                user=pending_order.user_uuid,
                payment_from=pending_order.payment_from,
                payment_to=pending_order.payment_to,
                date=pending_order.date,
                status=Status.Completed
                )
            db.session.add(completed_order)
            db.pending_order.delete(PendingOrder.id == order_id)
            db.session.commit()
            return f"Заявка {order_id} обработана"
        if pending_order.status == Status.Canceled:
            completed_order = db.order.new(
                user=pending_order.user_uuid,
                payment_from=pending_order.payment_from,
                payment_to=pending_order.payment_to,
                date=pending_order.date,
                status=Status.Canceled
                )
            db.session.add(completed_order)
            db.pending_order.delete(PendingOrder.id == order_id)
            db.session.commit()


# -----------------------------------------------------------------------------


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
    except KeyError:
        return ("Ошибка в получении ревью")


@menu_router.get("/contacts")
async def contacts():
    ...


@currency_router.get("/{give_tikker}/{get_tikker}")
async def give_get_tikker(
    give_tikker: Tikker,
    get_tikker: Tikker,
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    try:
        give = await db.currency.get_by_where(
            whereclause=(Currency.tikker == give_tikker)
        )
        give_min = give.min
        give_max = give.max
        if get_tikker == "LTC":
            rate = find_price('LTCRUB')
        if get_tikker == "BTC":
            rate = find_price('BTCRUB')
    except KeyError:
        return ("Ошибка в обменном роутере")
    finally:
        return {
            "rate": rate,
            "give_tikker": give_tikker,
            "get_tikker": get_tikker,
            "give_min": give_min,
            "give_max": give_max
        }
