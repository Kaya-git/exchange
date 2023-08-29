""" Order repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Order, User, PaymentOption, Status
from .abstract import Repository
import datetime


class OrderRepo(Repository[Order]):
    """
    Order repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize order repository as for all odrders or only for one order
        """
        super().__init__(type_model=Order, session=session)

    async def new(
        self,
        user: User,
        payment_from: PaymentOption,
        payment_to: PaymentOption,
        date: datetime.datetime,
        status: Status,
    ) -> None:

        new_order = await self.session.merge(
            Order(
                user=user,
                payment_from=payment_from,
                payment_to=payment_to,
                date=date,
                status=status,
            )
        )
        return new_order
