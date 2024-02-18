import logging
from asyncio import sleep as asyncsleep
from decimal import Decimal
from typing import TYPE_CHECKING, List, Protocol

import httpx
from fastapi import HTTPException, status

if TYPE_CHECKING:
    from currencies.routers import CoingekkoParamsDTO

LOGGER = logging.getLogger(__name__)

Price = Decimal
Prices = dict


class PriceParser(Protocol):
    """Interface for any price parser"""
    async def find_price(
            self,
            parse_params: "CoingekkoParamsDTO"
    ):
        raise NotImplementedError


class CoinGekkoParser:
    """Coingekko parser"""
    def __init__(
            self,
            base='https://api.coingecko.com',
            path='/api/v3/simple/price'
    ) -> None:
        self._base = base
        self._path = path

    async def find_price(
            self,
            ids,
            vs_currencies
    ) -> Prices:
        url = self._base + self._path

        ids_str = ','.join(ids)
        vs_currencies_str = ','.join(vs_currencies)

        param = {
            'ids': ids_str,
            'vs_currencies': vs_currencies_str
        }
        count = 0
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=url, params=param)

                LOGGER.info(f"Parser status: {response.status_code}")
                LOGGER.info(f"response: {response.json()}")

                if response.status_code == 429:
                    LOGGER.error(
                        "Слишком много запросов к серверу. Парсер перегружен"
                    )

                if response.status_code != 200:
                    count = 5
                    while response.status_code != 200 or count != 0:
                        LOGGER.info("Ждем 5 секунд и отправляем новый запрос")
                        await asyncsleep(5)
                        response = await client.get(url=url, params=param)
                        count -= 1

                if count == 0:
                    return response.json()

            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Произошла ошибка при запросе {exc.request.url!r}."
                )


async def parse_the_price(
        ids:  List | str,
        vs_currencies: List | str
) -> Price | Prices:
    """Parse the Price"""
    return await CoinGekkoParser().find_price(ids, vs_currencies)
