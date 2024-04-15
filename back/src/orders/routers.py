import logging
from typing import TYPE_CHECKING, List

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import current_active_user
from database.db import Database, get_async_session
from sevices import services
from users.routers import lk_router
from enums.models import Status, CurrencyType

from .models import Order
from .shemas import OrderRead
from payment_options.models import PaymentOption
from currencies.models import Currency
from enums.models import CurrencyType
from sevices import services


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

    order_id = await services.redis_values.get_order_id(user_uuid)

    order = await db.order.get(order_id)

    LOGGER.info(f"Заявка: {order.id} Статус заявки: {order.status}")

    if order is not None:

        if (
            order.status is Status.исполнена and
            order.transaction_link is not None
        ):
            # Удаляем заявки из акутальных и ключ в редисе
            await services.redis_values.redis_conn.delete(user_uuid)

            buy_currency = await db.currency.get(order.buy_currency_id)

            if buy_currency.type is CurrencyType.Крипта:
                return {
                    "link": order.transaction_link
                }
            return None

        if order.status is Status.отклонена:
            # Удаляем заявки из акутальных и ключ в редисе
            await services.redis_values.redis_conn.delete(user_uuid)

            return {
                "reason": order.decline_reason
            }

        return {
            "status": order.status
        }

    raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ордера нет в базе"
            )


@orders_router.post("/get_order_info")
async def get_order_info(
    uuid: str,
    session: AsyncSession = Depends(get_async_session)
) -> dict | None:
    db = Database(session=session)
    if services.redis_values.check_existance(user_uuid=uuid):
        return await services.redis_values.decode_values_for_order_info(
            user_uuid=uuid, db=db
        )
    else:
        return False
