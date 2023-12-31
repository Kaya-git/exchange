from decimal import Decimal
import httpx
from fastapi import HTTPException, status
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from currencies.routers import CoingekkoParamsDTO


Price = Decimal


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
    ) -> Price:
        url = self._base + self._path

        param = {
            'ids': f'{parse_params.ids}',
            'vs_currencies': f'{parse_params.vs_currencies}'
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=url, params=param)
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
) -> Price:
    """Parse the Price"""
    return await parser.find_price(parse_params=parse_params)
