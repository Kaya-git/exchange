from fastapi import APIRouter, Depends, Path
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from .schemas import CurrencyRead
from binance_parser import find_price
from enums import CryptoType


currency_router = APIRouter(
    prefix="/currency",
    tags=["Роутер валют"]
)


@currency_router.get("/list", response_model=List[CurrencyRead])
async def currency_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    currency_list = await db.currency.get_all()
    return currency_list


@currency_router.get("/currency/{id}", response_model=CurrencyRead)
async def currency_id(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    currency = await db.currency.get(ident=id)
    return currency

@currency_router.get("/tariffs")
async def tariffs(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)

    all_currencies = await db.currency.get_all()
    currency_list =[]
    for currency in all_currencies:
        if currency.type is CryptoType.Crypto:
            show_currency = {}

            solo_tikker = currency.tikker.split('_')[0]
            parsing_tikker = f"{solo_tikker}RUB"

            coin_price = await find_price(parsing_tikker)
            show_currency["name"] = currency.name
            show_currency["tikker"] = solo_tikker
            show_currency["icon"] = currency.icon
            show_currency["reserve"] = currency.reserve
            show_currency["max"] = currency.max
            show_currency["min"] = currency.min
            show_currency["coin_price"] = coin_price
            currency_list.append(show_currency)
        else:
            pass

    return currency_list
