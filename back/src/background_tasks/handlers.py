import json
import logging
from asyncio import sleep as async_sleep

import httpx
from fastapi import HTTPException, status

from database.db import Database
from enums import CurrencyType
from enums.models import Status
from pendings.models import PendingAdmin
from price_parser.parser import parse_the_price
from redis_ttl.routers import get_ttl
from sevices import services


LOGGER = logging.getLogger(__name__)


async def cache_rates():
    first = True
    while True:

        LOGGER.info("Получаю актульные курсы")
        try:
            all_currencies = await Database().currency.get_all()
            print(all_currencies)
        except httpx.RequestError as exc:

            LOGGER.error(f"Проблема с поиском монет в бд {exc.request.url!r}")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Проблема с поиском монет в бд {exc.request.url!r}"
            )

        vs_currencies = []
        ids = []

        for currency in all_currencies:
            if currency.type is CurrencyType.Крипта:
                LOGGER.info(f"Крипта:{currency}")
                ids.append(currency.coingecko_tik)
            if currency.type is CurrencyType.Фиат:
                LOGGER.info(f"Фиат:{currency}")
                vs_currencies.append(currency.coingecko_tik)

        LOGGER.info(f"Фиат:{vs_currencies}")
        LOGGER.info(f"Крипта:{ids}")

        rates = await parse_the_price(ids, vs_currencies,)

        LOGGER.info(f"ответ:{rates}")

        if rates is not None and first is False:
            try:
                LOGGER.info("Удаляем валюты из редиса")
                await services.redis_values.redis_conn.delete("rates")

            except httpx.RequestError as exc:
                LOGGER.error(
                    f"Проблема c удалением монет из редиса{exc.request.url!r}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"""Проблема c удалением монет из редиса
                    {exc.request.url!r}
                    """
                )

        LOGGER.info(f"Курсы: {rates}, тип: {type(rates)}")

        rval = json.dumps(rates)
        await services.redis_values.redis_conn.set("rates", rval)

        LOGGER.info("Парсинг спит 10 мин")
        await async_sleep(60)


async def controll_order(
    user_uuid: str | None,
    db: Database
):

    # Получаем оставшееся время жизни ключа
    order_ttl = await get_ttl(
        user_uuid=user_uuid
    )

    # Если ключ -1 то не назначено время
    if order_ttl == -1:
        return None

    # Запускаем цикл, пока жив ключ
    while order_ttl != -2:

        # Актуальный номер роутера
        router_num = await services.redis_values.get_router_num(
            user_uuid=user_uuid
        )

        # Если номер роутера от 3, то можно получить номер заявки
        if router_num >= 3:
            order_id = await services.redis_values.get_order_id(
                user_uuid=user_uuid
            )
            user_id = await services.redis_values.get_user_id(
                user_uuid
            )
            if order_id:
                await services.db_paralell.payed_button_db(
                    db=db,
                    user_uuid=user_uuid,
                    order_id=order_id,
                    user_id=user_id
                )
        # Отдаем контроль на 10 сек
        await async_sleep(10)

        order_ttl = await get_ttl(
            user_uuid=user_uuid
        )

    # C 4 по 5 и с 7 по 8 заявка находиться актуальных
    if (
        4 <= router_num >= 5 or
        7 <= router_num >= 8
    ):
        # Удаляем заявку из актуальных
        await db.pending_admin.delete(
            PendingAdmin.order_id == order_id
        )
        await db.session.commit()

    if router_num >= 3:
        order = await db.order.get(order_id)
        if order.status != Status.исполнена:
            # Меняем статус заявки на истекло время
            await db.order.order_status_timout(
                order_id
            )
        return None
    else:
        return None
