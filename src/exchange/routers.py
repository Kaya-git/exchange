from fastapi import APIRouter, Cookie, Response, Depends
from fastapi.responses import RedirectResponse
from .sevices import services
from database.models.router_enum import Tikker
from database.db import Database, get_async_session
from database.models import (
    Currency, Review,
    PendingOrder, PendingStatus,
    ServicePM, Status,
)
import time
from sqlalchemy.ext.asyncio import AsyncSession


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
async def confirm_cc(cookies_id: str | None = Cookie(default=None)):
    does_exist = await services.redis_values.redis_conn.exists(cookies_id)
    # Проверяем есть ли ключи в реддисе
    if does_exist != 1:
        # Меняем статус ордера на время вышло
        return "Время вышло"

    (
        wallet_num,
        cc_holder,
        cc_num,
        get_curr,
        get_value,
        send_curr,
        send_value,
        email
    ) = await services.redis_values.redis_conn.lrange(cookies_id, 0, -1)

    wallet_num = str(wallet_num, 'UTF-8')
    cc_holder = str(cc_holder, 'UTF-8')
    cc_num = str(cc_num, 'UTF-8')
    get_curr = str(get_curr, 'UTF-8')
    get_value = float(get_value)
    send_curr = str(send_curr, 'UTF-8')
    send_value = float(send_value)
    email = str(email, 'UTF-8')
    bart_for_one = (send_curr * 1) / get_curr

    # f"Направление обмена: {send_curr}/{get_curr}\n"
    # f"Обмен по курсу: {bart_for_one}
    # f"Отправляете: {send_value} {send_curr}\n"
    # f"Получаете: {get_value} {get_curr}\n"
    # f" Номер вашей карты: {cc_num}\n"
    # f" Ваш кошелек: {wallet_num}"

    return {
        "wallet_num": wallet_num,
        "bart_for_one": bart_for_one,
        "cc_holder": cc_holder,
        "cc_num": cc_num,
        "get_curr": get_curr,
        "get_value": get_value,
        "send_curr": send_curr,
        "send_value": send_value,
        "email": email
    }


@exhange_router.get("/await")
async def conformation_await(
    user_id: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
) -> RedirectResponse:
    db = Database(session=async_session)
    while True:
        await time.sleep(30)
        order = await db.pending_order.get_by_where(
            PendingOrder.user_uuid == user_id
        )
        if order.status == PendingStatus.Approved:
            return RedirectResponse(f"/exchange/order/{order.id}")
        if order.status == PendingStatus.Canceled:
            return RedirectResponse("/cancel")


@exhange_router.get("/order/{order_id}")
async def requisites(
    order_id: int,
    response: Response,
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    order = await db.pending_order.get_by_where(
        PendingOrder.id == order_id
    )
    service_pm = await db.payment_option.get_by_where(
        ServicePM.currency == order.payment_from.currency
    )

    response.set_cookie(key="order_id", value=order_id)
    return {
        "oder_id": order_id,
        "service_pm": service_pm.cc_num_x_wallet,
        "cc_holder": service_pm.cc_holder
    }


@exhange_router.get("/payed")
async def payed_button(
    order_id: str | None = Cookie(default=None),
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    while True:
        await time.sleep(30)
        pending_order = await db.pending_order.get_by_where(
            PendingOrder.id == order_id
        )
        if pending_order.status == PendingStatus.Completed:
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
        if pending_order.status == PendingStatus.Canceled:
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
        "btc": BTC_RUB_PRICE,
        "ltc": LTC_RUB_PRICE,
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
            rate = LTC_RUB_PRICE
        if get_tikker == "BTC":
            rate = BTC_RUB_PRICE
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
