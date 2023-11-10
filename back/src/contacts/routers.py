from fastapi import APIRouter, Depends, Path
import sqlalchemy as sa
from database.db import Database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ContactRead
from typing import List, Annotated


contact_router = APIRouter(
    prefix="/contact",
    tags=["Роутер контактов"]
)

@contact_router.get("/list", response_model=List[ContactRead])
async def contact_list(
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    contact_list = await db.contact.get_all()
    return contact_list

@contact_router.get("/{id}", response_model=ContactRead)
async def contact(
    id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)
    contact = await db.contact.get(ident=id)
    return contact
