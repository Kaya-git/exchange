from dataclasses import dataclass
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Database, get_async_session
from enums import CurrencyType
import pprint
from .models import Currency
from .schemas import CurrencyDTO, CurrencyTariffsDTO
import logging
from exchange.handlers import find_exchange_rate


currency_router = APIRouter(
    prefix="/api/currency",
    tags=["Роутер валют"]
)

LOGGER = logging.getLogger(__name__)


@dataclass
class CoingekkoParamsDTO:
    ids: str
    vs_currencies: str


@currency_router.get("/list", response_model=List[CurrencyDTO])
@cache(expire=1800)
async def currency_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    return await db.currency.get_all()


@currency_router.get("/currency/{id}", response_model=CurrencyDTO)
@cache(expire=1800)
async def currency_id(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    return await db.currency.get(ident=id)


@currency_router.get("/tariffs")
async def tariffs(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)

    crypto_currencies = await db.currency.get_many(
        Currency.type == CurrencyType.Крипта
    )

    fiat_currencies = await db.currency.get_many(
        Currency.type == CurrencyType.Фиат
    )

    tariffs_dict = {}

    for fiat_currency in fiat_currencies:
        pprint.pprint(fiat_currency)
        crypto_dict = {}
        for crypto_currency in crypto_currencies:

            dct = {}

            exchange_rate = await find_exchange_rate(
                fiat_currency, crypto_currency
            )
            LOGGER.info(
                f"десер.значение: {exchange_rate}, тип: {type(exchange_rate)}"
            )

            dct["id"] = crypto_currency.id
            dct["name"] = crypto_currency.name
            dct["tikker"] = crypto_currency.tikker
            dct["icon"] = crypto_currency.icon
            dct["reserve"] = crypto_currency.reserve
            dct["max"] = crypto_currency.max
            dct["min"] = crypto_currency.min
            dct["coin_price"] = exchange_rate

            crypto_dict[f"{crypto_currency.tikker}"] = dct
            pprint.pprint(crypto_dict)

        tariffs_dict[f"{fiat_currency.tikker}"] = crypto_dict

    pprint.pprint(tariffs_dict)
    return tariffs_dict


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
