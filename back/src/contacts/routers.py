from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Database, get_async_session
from fastapi_cache.decorator import cache
from .schemas import ContactRead


contact_router = APIRouter(prefix="/api/contact", tags=["Роутер контактов"])


@contact_router.get("/list", response_model=List[ContactRead])
@cache(expire=300)
async def contact_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    contact_list = await db.contact.get_all()
    return contact_list


@contact_router.get("/{id}", response_model=ContactRead)
@cache(expire=300)
async def contact(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    contact = await db.contact.get(ident=id)
    return contact
