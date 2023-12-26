from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import current_active_user
from database.db import Database, get_async_session
from payment_options.models import PaymentOption
from .scheemas import ChangePassDTO
from auth.manager import UserManager

if TYPE_CHECKING:
    from users.models import User


lk_router = APIRouter(
    prefix="/api/lk",
    tags=["Роутер информации в лк"]
)


@lk_router.get("/user")
async def user_info(
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_user)
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


@lk_router.post("/pass_change")
async def change_pass(
    payload: ChangePassDTO,
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_user)
):
    db = Database(async_session)
    user_manager = UserManager()
    new_pass = payload.new_pass
    old_pass = payload.old_pass
    user_hashed_pass = user.hashed_password
    verif = await user_manager.password_helper.verify_and_update(
        plain_password=old_pass,
        hashed_password=user_hashed_pass
    )
    if verif is True:
        new_hash_pass = user_manager.password_helper.hash(
            new_pass
        )

        await db.user.update(
            whereclause=(User.id == user.id),
            table_name='hashed_pass',
            values=new_hash_pass
        )
        db.session.commit()
        return 'Поменял пасс'
    else:
        return 'Проблемс'
