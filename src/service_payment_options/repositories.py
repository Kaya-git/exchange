"""  ServicePaymentOption repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from service_payment_options.models import ServicePaymentOption
from currencies.models import Currency
from enums import BankingType
from database.abstract_repo import Repository


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
        banking_type: BankingType,
        currency_id: Currency,
        number: str,
        holder: str,
    ) -> None:

        new_service_po = await self.session.merge(
            ServicePaymentOption(
                banking_type=banking_type,
                currency_id=currency_id,
                number=number,
                holder=holder,
            )
        )
        return new_service_po
