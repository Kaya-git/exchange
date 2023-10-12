"""  Currency repository file """
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from ..models import Currency, ServicePaymentOption
from .abstract import Repository
from typing import List


class CurrencyRepo(Repository[Currency]):
    """
    Currency repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize PaymentOption repository as for all PaymentOptions
        or only for one
        """
        super().__init__(type_model=Currency, session=session)

    async def new(
        self,
        tikker_id: int,
        tikker: str,
        name: str,
        max: sa.Numeric,
        min: sa.Numeric,
        icon: str,
        gas: sa.Numeric = 130,
        service_margin: sa.Numeric = 7,
        reserve: sa.Numeric = 0,
        service_payment_option: List[ServicePaymentOption] = [],
    ) -> None:

        new_currency = await self.session.merge(
            Currency(
                tikker_id=tikker_id,
                tikker=tikker,
                name=name,
                max=max,
                min=min,
                icon=icon,
                gas=gas,
                service_margin=service_margin,
                reserve=reserve,
                service_payment_option=service_payment_option,
            )
        )
        return new_currency
