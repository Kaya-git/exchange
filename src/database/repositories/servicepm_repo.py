""" Service Option repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Currency, ServicePM
from .abstract import Repository


class ServicePMRepo(Repository[ServicePM]):
    """
    PaymentOption repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize PaymentOption repository as for all PaymentOptions
        or only for one
        """
        super().__init__(type_model=ServicePM, session=session)

    async def new(
        self,
        currency: Currency,
        cc_num_x_wallet: str,
        cc_holder: str,
    ) -> None:

        new_service_pm = await self.session.merge(
            ServicePM(
                currency=currency,
                cc_num_x_wallet=cc_num_x_wallet,
                cc_holder=cc_holder,
            )
        )
        return new_service_pm
