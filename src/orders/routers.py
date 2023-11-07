from auth.routers import current_active_verified_user 
from fastapi import Depends, APIRouter
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_async_session, Database
from .shemas import OrderRead
from .models import Order
if TYPE_CHECKING:
    from users.models import User


orders_router = APIRouter(
    prefix="/orders",
    tags=["Роутер списка заказов для верифицированного пользователя"]
)

@orders_router.get("/list", response_model=List[OrderRead])
async def order_list(
    async_session: AsyncSession = Depends(get_async_session),
    user: "User" = Depends(current_active_verified_user)
):
    db = Database(session=async_session)
    completed_orders = await db.order.get_many(
        Order.user_email == user.email
    )
    return completed_orders
