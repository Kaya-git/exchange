"""  ServicePaymentOption repository file """
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from currencies.models import Currency
from database.abstract_repo import Repository
from orders.models import Order
from service_payment_options.models import ServicePaymentOption


class ServicePaymentOptionRepo(Repository[ServicePaymentOption]):
    """
    ServicePaymentOption repository for CRUD
    and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize ServicePaymentOption
        repository as for all ServicePaymentOption
        or only for one
        """
        super().__init__(type_model=ServicePaymentOption, session=session)

    async def new(
        self,
        currency_id: Currency,
        number: str,
        holder: str,
    ) -> None:

        new_service_po = await self.session.merge(
            ServicePaymentOption(
                currency_id=currency_id,
                number=number,
                holder=holder,
            )
        )
        return new_service_po

    async def spo_equal_sp(
            self,
            order_id
    ) -> ServicePaymentOption:
        statement = (
            select(
                    ServicePaymentOption
                ).join(
                    Currency, ServicePaymentOption.currency_id == Currency.id
                ).join(
                    Order, Currency.id == Order.sell_currency_id
                ).where(
                    Order.id == order_id
                )
        )

        return (await self.session.execute(statement)).scalar_one_or_none()
