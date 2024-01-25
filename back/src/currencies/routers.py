from dataclasses import dataclass
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Database, get_async_session
from enums import CurrencyType
from price_parser.parser import CoinGekkoParser, parse_the_price

from .models import Currency
from .schemas import CurrencyDTO, CurrencyTariffsDTO

currency_router = APIRouter(
    prefix="/api/currency",
    tags=["Роутер валют"]
)


@dataclass
class CoingekkoParamsDTO:
    ids: str
    vs_currencies: str


@currency_router.get("/list", response_model=List[CurrencyDTO])
@cache(expire=300)
async def currency_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    return await db.currency.get_all()


@currency_router.get("/currency/{id}", response_model=CurrencyDTO)
@cache(expire=300)
async def currency_id(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    return await db.currency.get(ident=id)


@currency_router.get("/tariffs", response_model=List[CurrencyTariffsDTO])
@cache(expire=300)
async def tariffs(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)

    all_currencies = await db.currency.get_all()
    currency_list = []
    for currency in all_currencies:
        if currency.type is CurrencyType.Крипта:

            show_currency = {}

            coingekko_params = CoingekkoParamsDTO(
                ids=currency.coingecko_tik,
                vs_currencies='rub'
            )

            coin_price = await parse_the_price(
                parse_params=coingekko_params,
                parser=CoinGekkoParser()
            )

            show_currency["id"] = currency.id
            show_currency["name"] = currency.name
            show_currency["tikker"] = currency.tikker
            show_currency["icon"] = currency.icon
            show_currency["reserve"] = currency.reserve
            show_currency["max"] = currency.max
            show_currency["min"] = currency.min
            show_currency["coin_price"] = coin_price
            currency_list.append(show_currency)
        else:
            pass

    return currency_list


@currency_router.get("/wallet_val")
async def get_wallet_val(
    currency_tik: str,
    async_session: AsyncSession = Depends(get_async_session)
) -> dict:
    """ Роутер для валидации крипто-кошельков """

    db = Database(session=async_session)
    currency = await db.currency.get_by_where(
        Currency.tikker == currency_tik
    )
    return {
        "min": currency.symbols_max,
        "max": currency.symbols_min,
        "start": currency.wallet_starts
    }
