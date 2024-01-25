from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Database, get_async_session

from .schemas import ContactDTO

contact_router = APIRouter(prefix="/api/contact", tags=["Роутер контактов"])


@contact_router.get("/list", response_model=List[ContactDTO])
@cache(expire=300)
async def contact_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    return await db.contact.get_all()


@contact_router.get("/{id}", response_model=ContactDTO)
@cache(expire=300)
async def contact(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    return await db.contact.get(ident=id)
