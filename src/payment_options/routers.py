from auth.routers import current_active_verified_user 
from fastapi import Depends, APIRouter, Path
from typing import TYPE_CHECKING, Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_async_session, Database
from .schemas import PaymentOptionRead
from .models import PaymentOption
if TYPE_CHECKING:
    from users.models import User


payment_options = APIRouter(
    prefix="/my_po",
    tags=["роутер личного кабинета"]
)

@payment_options.get("/")
async def po_list(
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_verified_user)
) -> List[PaymentOptionRead]:
    db = Database(session=async_session)
    my_po = await db.payment_option.get_many(
        PaymentOption.id == user.payment_options
    )
    return my_po

@payment_options.get("/{po_id}")
async def po_list(
    po_id: Annotated[int, Path(title="The ID of the item to get")],
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_verified_user),

) -> PaymentOptionRead:
    db = Database(session=async_session)
    po = await db.payment_option.get(ident=po_id)
    return po
