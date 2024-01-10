from typing import TYPE_CHECKING, List

from auth.routers import current_active_user
from database.db import Database, get_async_session
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from users.routers import lk_router

from .models import Order
from .shemas import OrderRead

if TYPE_CHECKING:
    from users.models import User


orders_router = APIRouter(
    prefix="/api/orders",
    tags=["Роутер заявок"]
)


@lk_router.get("/orders", response_model=List[OrderRead])
async def order_list(
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_user)
):
    db = Database(session=async_session)
    completed_orders = await db.order.get_many(
        Order.user_email == user.email
    )
    return completed_orders


@orders_router.get("/get_order_status")
async def get_order_status(
    user_uuid: str | None = Form(),
    session: AsyncSession = Depends(get_async_session)
) -> str:
    db = Database(session=session)

    order = await db.order.get_by_where(
        Order.user_cookie == user_uuid
    )
    return {
        "status": order.status
    }
