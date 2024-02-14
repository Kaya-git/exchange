from asyncio import sleep as async_sleep

from database.db import Database
from enums.models import Status
from pendings.models import PendingAdmin
from redis_ttl.routers import get_ttl
from sevices import services
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from currencies.routers import CoingekkoParamsDTO
from enums import CurrencyType
import logging
from price_parser import parse_the_price, CoinGekkoParser
from fastapi import HTTPException, status
import httpx


LOGGER = logging.getLogger(__name__)


async def cache_rates(
    db: Database = Database
):
    while True:

        LOGGER.info("Получаю актульные курсы")
        try:
            all_currencies = await db.currency.get_all()

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
                ids.append(currency)
            if currency.type is CurrencyType.Фиат:
                vs_currencies.append(ids)

        coingekko_params = CoingekkoParamsDTO(
            ids=ids,
            vs_currencies=vs_currencies
        )

        rates = await parse_the_price(
            parse_params=coingekko_params,
            parser=CoinGekkoParser()
        )

        if rates is not None:
            try:
                await services.redis_values.redis_conn.delete("rates")

            except httpx.RequestError as exc:
                LOGGER.error(f"Проблема c удалением монет из редиса{exc.request.url!r}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Проблема c удалением монет из редиса {exc.request.url!r}"
                )

            LOGGER.info(rates)

            await services.redis_values.add_rates(
                rates
            )

        await async_sleep(600)


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
