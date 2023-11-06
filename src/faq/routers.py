from fastapi import APIRouter, Depends
import sqlalchemy as sa
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


faq = APIRouter(
    prefix="/faq",
    tags=["Роутер вопрос-ответ"]
)

@faq.get("/")
async def faq(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    faq_list = await db.faq.get_all()
    return faq_list

@faq.get("/{id}")
async def faq(
    id: int,
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    faq = await db.faq.get(ident=id)
    return faq
