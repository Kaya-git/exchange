""" Payment Option repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import (
    Currency, PaymentOption,
    PaymentPointer, PaymentBelonging,
    PendingOrder
)
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
        cc_num_x_wallet: str,
        cc_holder: str,
        image_name: str,
        payment_point: PaymentPointer,
        clien_service_belonging: PaymentBelonging,
        currency_id: Currency,
        pending_order_id: PendingOrder = None,
    ) -> None:

        new_payment_opt = await self.session.merge(
            PaymentOption(
                cc_num_x_wallet=cc_num_x_wallet,
                cc_holder=cc_holder,
                image_name=image_name,
                payment_point=payment_point,
                clien_service_belonging=clien_service_belonging,
                currency_id=currency_id,
                pending_order_id=pending_order_id,
            )
        )
        return new_payment_opt
