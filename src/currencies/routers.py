from fastapi import APIRouter, Depends, Path
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING, Annotated, List
from .schemas import CurrencyRead

currency_router = APIRouter(
    prefix="/currency",
    tags=["Роутер валют"]
)


@currency_router.get("/list")
async def currency_list(
    async_session: AsyncSession = Depends(get_async_session)
) -> List[CurrencyRead]:
    db = Database(async_session)
    currency_list = await db.currency.get_all()
    return currency_list


@currency_router.get("/currency/{id}")
async def currency_id(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
) -> CurrencyRead:
    db = Database(async_session)
    currency = await db.currency.get(ident=id)
    return currency
