from typing import TYPE_CHECKING, Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import current_active_user
from database.db import Database, get_async_session

from .models import PaymentOption
from .schemas import PaymentOptionRead

if TYPE_CHECKING:
    from users.models import User


payment_options_router = APIRouter(
    prefix="/my_pos",
    tags=["Верифицированые опции оплаты пользователя"]
)


@payment_options_router.get("/list", response_model=List[PaymentOptionRead])
async def po_list(
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_user)
):
    db = Database(session=async_session)
    my_po = await db.payment_option.get_many(
        PaymentOption.id == user.payment_options
    )
    return my_po


@payment_options_router.get("/{po_id}", response_model=PaymentOptionRead)
async def po_id(
    po_id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_user),
):
    db = Database(session=async_session)
    po = await db.payment_option.get(ident=po_id)
    return po
