""" Payment Option repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Currency, PaymentOption
from .abstract import Repository
from typing import Optional


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
        currency: Currency,
        amount: float,
        cc_num_x_wallet: str,
        cc_holder: str = None,
        image_name: str = None,
        user_id: Optional[str] = None,
    ) -> None:

        new_payment_opt = await self.session.merge(
            PaymentOption(
                currency=currency,
                amount=amount,
                cc_num_x_wallet=cc_num_x_wallet,
                cc_holder=cc_holder,
                image_name=image_name,
                user_id=user_id
            )
        )
        return new_payment_opt
