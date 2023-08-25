from fastapi import APIRouter, Cookie
from .sevices import services
from database.models.router_enum import Tikker
from .constants import LTC_RUB_PRICE, BTC_RUB_PRICE
from database.db import Database as db
from database.models import Currency, Review


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

# -----------------------------------------------------------------------------


@menu_router.get("/siterules")
async def siterules():
    ...


@menu_router.get("/reserve")
async def reserve():
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
async def reviews_all():
    try:
        reviews = await db.review.get_many(limit=10, order_by=Review.data)
        return reviews
    except KeyError:
        return ("Ошибка в получении ревью")


@menu_router.get("/contacts")
async def contacts():
    ...


@currency_router.get("/{give_tikker}/{get_tikker}")
async def give_get_tikker(give_tikker: Tikker, get_tikker: Tikker):
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
