""" Order repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import CompletedOrder, User, PaymentOption, Status, Currency
from .abstract import Repository
import datetime


class OrderRepo(Repository[CompletedOrder]):
    """
    Order repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize order repository as for all odrders or only for one order
        """
        super().__init__(type_model=CompletedOrder, session=session)

    async def new(
        self,
        email: str,
        give_amount: float,
        give_currency_id: Currency,
        get_amount: float,
        get_currency_id: Currency,
        payment_options: list[PaymentOption],
        status: Status = Status.InProcess,
        user_uuid: str = None,
        user_id: int = None,
    ) -> None:

        completed_order = await self.session.merge(
            CompletedOrder(
                email=email,
                give_amount=give_amount,
                give_currency_id=give_currency_id,
                get_amount=get_amount,
                get_currency_id=get_currency_id,
                payment_options=payment_options,
                status=status,
                user_uuid=user_uuid,
                user_id=user_id,
            )
        )
        return completed_order
