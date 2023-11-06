from fastapi import APIRouter, Depends, Path
import sqlalchemy as sa
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from .schemas import FAQ 
from typing import List


faq_router = APIRouter(
    prefix="/faq",
    tags=["Роутер FAQ"]
)

@faq_router.get("/")
async def faq(
    async_session: AsyncSession = Depends(get_async_session)
) -> List[FAQ]:
    db = Database(session=async_session)
    faq_list = await db.faq.get_all()
    return faq_list

@faq_router.get("/{id}")
async def faq(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
) -> FAQ:
    db = Database(session=async_session)
    faq = await db.faq.get(ident=id)
    return faq
