"""  Order repository file """
import sqlalchemy as sa
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from currencies.models import Currency
from database.abstract_repo import Repository
from database.engines import async_session_maker
from enums import Status, VerifDeclineReason
from orders.models import Order
from payment_options.models import PaymentOption
from service_payment_options.models import ServicePaymentOption
from users.models import User
import logging


LOGGER = logging.getLogger(__name__)


class OrderRepo(Repository[Order]):
    """
    Order repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize Order repository as for all Orders
        or only for one
        """
        super().__init__(type_model=Order, session=session)

    async def new(
        self,
        user_id: User,
        user_email: User,
        user_cookie: str,
        user_buy_sum: sa.Numeric,
        sell_currency_id: Currency,
        user_sell_sum: sa.Numeric,
        buy_currency_id: Currency,
        status: Status,
        buy_payment_option_id: PaymentOption = None,
        sell_payment_option_id: PaymentOption = None,
        decline_reason: VerifDeclineReason = None,
        service_sell_po_id: ServicePaymentOption = None,
        service_buy_po_id: ServicePaymentOption = None,
    ) -> None:

        new_order = await self.session.merge(
            Order(
                user_id=user_id,
                user_email=user_email,
                user_cookie=user_cookie,
                user_buy_sum=user_buy_sum,
                buy_currency_id=buy_currency_id,
                buy_payment_option_id=buy_payment_option_id,
                user_sell_sum=user_sell_sum,
                sell_currency_id=sell_currency_id,
                sell_payment_option_id=sell_payment_option_id,
                status=status,
                decline_reason=decline_reason,
                service_sell_po_id=service_sell_po_id,
                service_buy_po_id=service_buy_po_id,
            )
        )
        return new_order

    async def update_pos(
        self,
        order_id: int,
        po_buy: int,
        po_sell: int
    ):
        async with async_session_maker() as session:

            update_sell_po = (
                update(
                    Order
                ).where(
                    Order.id == order_id
                ).values(
                    sell_payment_option_id=po_sell
                )
            )

            LOGGER.info(f"Апнут селл пеймент {update_sell_po}")

            update_buy_po = (
                update(
                    Order
                ).where(
                    Order.id == order_id
                ).values(
                    buy_payment_option_id=po_buy
                )
            )

            LOGGER.info(f"Апнут бай пеймент {update_buy_po}")            
            await session.execute(update_sell_po)
            await session.execute(update_buy_po)
            await session.commit()

    async def order_status_timout(
            self,
            order_id: int
    ) -> None:
        async with async_session_maker() as session:

            status_update = (
                update(
                    Order
                ).where(
                    Order.id == order_id
                ).values(
                    status=Status.отклонена
                )
            )

            reason_update = (
                update(
                    Order
                ).where(
                    Order.id == order_id
                ).values(
                    decline_reason=VerifDeclineReason.истечение_времени
                )
            )
            await session.execute(status_update)
            await session.execute(reason_update)
            await session.commit()

    async def order_status_update(
            self,
            new_status: Status,
            order_id: int
    ):
        async with async_session_maker() as session:
            statement = (
                update(
                    Order
                ).where(
                    Order.id == order_id
                ).values(
                    status=new_status
                )
            )
            await session.execute(statement)
            await session.commit()

    async def select_orders_with_joined_currensies(
        self,
        whereclause
    ):
        async with async_session_maker() as session:
            statement = (
                select(
                    Order
                ).options(
                    joinedload(Order.buy_currency)
                ).options(
                    joinedload(Order.sell_currency)
                ).where(whereclause)
            )
            return (await session.scalars(statement)).all()
