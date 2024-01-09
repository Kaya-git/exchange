from typing import Annotated, List

from database.db import Database, get_async_session
from fastapi import APIRouter, Depends, Path
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import FAQDTO

faq_router = APIRouter(
    prefix="/api/faq",
    tags=["Роутер FAQ"]
)


@faq_router.get("/", response_model=List[FAQDTO])
@cache(expire=300)
async def faq_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    return await db.faq.get_all()


@faq_router.get("/{id}", response_model=FAQDTO)
@cache(expire=300)
async def faq(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    return await db.faq.get(ident=id)
