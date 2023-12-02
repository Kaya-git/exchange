from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Database, get_async_session

from .schemas import FAQRead

faq_router = APIRouter(
    prefix="/api/faq",
    tags=["Роутер FAQ"]
)


@faq_router.get("/", response_model=List[FAQRead])
async def faq_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    faq_list = await db.faq.get_all()
    return faq_list


@faq_router.get("/{id}", response_model=FAQRead)
async def faq(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    faq = await db.faq.get(ident=id)
    return faq
