from typing import TYPE_CHECKING, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.routers import current_active_user
from database.db import Database, get_async_session

from .models import Order
from .shemas import OrderRead
from users.routers import lk_router
if TYPE_CHECKING:
    from users.models import User


orders_router = APIRouter(
    prefix="/api/orders",
    tags=["Роутер списка заказов для верифицированного пользователя"]
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
