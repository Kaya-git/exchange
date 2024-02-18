"""  Currency repository file """
from typing import List

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from currencies.models import Currency
from database.abstract_repo import Repository
from database.engines import async_session_maker
from service_payment_options.models import ServicePaymentOption


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

    async def get_all(
        self,
        order_by=None,
    ) -> List[Currency]:
        async with async_session_maker() as session:
            statement = select(Currency)
            if order_by:
                statement = statement.order_by(order_by)
            return (await session.scalars(statement)).all()
