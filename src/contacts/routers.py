from fastapi import APIRouter, Depends
import sqlalchemy as sa
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


contact_router = APIRouter(
    prefix="/contact",
    tags=["Роутер контактов"]
)

@contact_router.get("/")
async def contact_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    contact_list = await db.contact.get_all()
    return contact_list

@contact_router.get("/{id}")
async def contact(
    id: int,
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    contact = await db.contact.get(ident=id)
    return contact
