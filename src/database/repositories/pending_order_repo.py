""" PendingOrder repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import PendingOrder, PaymentOption, Currency
from .abstract import Repository
from typing import List, Optional


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
        give_amount: float,
        give_currency_id: Currency,
        get_amount: float,
        get_currency_id: Currency,
        payment_options: Optional[List[PaymentOption]] = [],
        user_uuid: str = None
    ) -> None:

        new_pending_order = await self.session.merge(
            PendingOrder(
                email=email,
                give_amount=give_amount,
                give_currency_id=give_currency_id,
                get_amount=get_amount,
                get_currency_id=get_currency_id,
                payment_options=payment_options,
                user_uuid=user_uuid
            )
        )
        return new_pending_order
