from fastapi import APIRouter, Depends
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .scheemas import Currency, CurrencyCreate
from typing import TYPE_CHECKING

currency_router = APIRouter(
    prefix="/currency",
    tags=["роутер валют"]
)


@currency_router.get("/currency/list")
async def currency_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    currency_list = await db.currency.get_all()
    return currency_list


@currency_router.get("/currency/{id}")
async def currency_id(
    id: int,
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(async_session)
    currency = await db.currency.get(ident=id)
    return currency
