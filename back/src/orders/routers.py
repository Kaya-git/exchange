from typing import TYPE_CHECKING, List

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import current_active_user
from database.db import Database, get_async_session
from sevices import services
from users.routers import lk_router

from .models import Order
from .shemas import OrderRead
import logging

if TYPE_CHECKING:
    from users.models import User


LOGGER = logging.getLogger(__name__)

orders_router = APIRouter(
    prefix="/api/orders",
    tags=["Роутер заявок"]
)


@orders_router.post("/decline_order")
async def decline_order(
    user_uuid: str | None = Form(),
    async_session: AsyncSession = Depends(get_async_session)
):
    db = Database(session=async_session)

    # Проверяем существование ключа в редисе
    await services.redis_values.check_existance(
        user_uuid=user_uuid
    )

    order_id = await services.redis_values.get_order_id(
        user_uuid=user_uuid
    )
    if order_id is not None:
        await db.order.delete(Order.id == order_id)
        await db.session.commit()
    await services.redis_values.redis_conn.delete(user_uuid)


@lk_router.get("/orders", response_model=List[OrderRead])
async def order_list(
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_user)
):

    completed_orders = await Database(
        async_session
        ).order.select_orders_with_joined_currensies(
        Order.user_email == user.email
    )

    return completed_orders


@orders_router.get("/get_order_status")
async def get_order_status(
    user_uuid: str,
    session: AsyncSession = Depends(get_async_session)
) -> dict | None:
    db = Database(session=session)

    order = await db.order.get_last_order(
        user_uuid=user_uuid
    )

    LOGGER.info(f"Заявка:{order}")

    if order is not None:
        return {
            "status": order.status
        }
    raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ордера нет в базе"
            )
