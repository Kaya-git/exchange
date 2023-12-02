from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import current_active_verified_user
from database.db import Database, get_async_session
from payment_options.models import PaymentOption

if TYPE_CHECKING:
    from users.models import User


user_lk_router = APIRouter(
    prefix="/api/lk",
    tags=["Роутер информации в лк"]
)


@user_lk_router.get("/user")
async def user_info(
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_verified_user)
):
    db = Database(session=async_session)

    verified_po = await db.payment_option.get_many(
        whereclause=(PaymentOption.user_id == user.id))

    return {
        'buy_volume': user.buy_volume,
        'email': user.email,
        'first_name': user.first_name,
        'second_name': user.second_name,
        'reg_date': user.registered_on,
        'verified_po': verified_po
    }
