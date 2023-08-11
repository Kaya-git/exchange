""" Order repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Order, User, Currency, PaymentOption, Status
from .abstract import Repository


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
        ammount_get: float,
        get_currency: Currency,
        ammount_give: float,
        give_currency: Currency,
        payment_option: PaymentOption,
        status: Status
    ) -> None:

        new_order = await self.session.merge(
            Order(
                user=user,
                ammount_get=ammount_get,
                get_currency=get_currency,
                ammount_give=ammount_give,
                give_currency=give_currency,
                payment_option=payment_option,
                status=status,
            )
        )
        return new_order
