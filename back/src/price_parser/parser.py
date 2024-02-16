from decimal import Decimal
from typing import TYPE_CHECKING, Protocol
from asyncio import sleep as asyncsleep
import httpx
from fastapi import HTTPException, status
import logging

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
            parse_params: "CoingekkoParamsDTO"
    ) -> Prices:
        url = self._base + self._path

        param = {
            'ids': f'{parse_params.ids}',
            'vs_currencies': f'{parse_params.vs_currencies}'
        }
        count = 0
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=url, params=param)

                LOGGER.info(f"Parser status: {response.status_code}")

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
                    return None
                price = round(
                    Decimal(
                        response.json()[param['ids']][param['vs_currencies']]
                    ), 2
                )
                return price
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Произошла ошибка при запросе {exc.request.url!r}."
                )


async def parse_the_price(
        parse_params: "CoingekkoParamsDTO",
        parser: CoinGekkoParser
) -> Price | Prices:
    """Parse the Price"""
    return await parser.find_price(parse_params=parse_params)
