""" Payment Option repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Currency, PaymentOption
from .abstract import Repository


class PaymentOptionRepo(Repository[PaymentOption]):
    """
    PaymentOption repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize PaymentOption repository as for all PaymentOptions
        or only for one
        """
        super().__init__(type_model=PaymentOption, session=session)

    async def new(
        self,
        name: str,
        currency: Currency,
        banking_acc_number: str,
    ) -> None:

        new_payment_opt = await self.session.merge(
            PaymentOption(
                name=name,
                currency=currency,
                banking_acc_number=banking_acc_number,
            )
        )
        return new_payment_opt
