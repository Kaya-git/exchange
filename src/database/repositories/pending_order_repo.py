""" PendingOrder repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import PendingOrder, PaymentOption
from .abstract import Repository


class PendingOrderRepo(Repository[PendingOrder]):
    """
    PendingOrder repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize PendingOrder repository
        as for all PendingOrder or only for one
        """
        super().__init__(type_model=PendingOrder, session=session)

    async def new(
        self,
        email: str,
        payment_from: PaymentOption,
        payment_to: PaymentOption,
        user_uuid: str = None
    ) -> None:

        new_pending_order = await self.session.merge(
            PendingOrder(
                email=email,
                payment_from=payment_from,
                payment_to=payment_to,
                user_uuid=user_uuid,
            )
        )
        return new_pending_order
