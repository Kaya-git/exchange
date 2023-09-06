""" Currency repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Currency, PaymentOption
from .abstract import Repository


class CurrencyRepo(Repository[Currency]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize user repository as for all users or only for one user
        """
        super().__init__(type_model=Currency, session=session)

    async def new(
        self,
        id: int,
        name: str,
        tikker: str,
        reserve: float = 0,
        min: int = 0,
        max: int = 0,
        payment_option: list[PaymentOption] | PaymentOption = None,
    ) -> None:

        new_currency = await self.session.merge(
            Currency(
                id=id,
                name=name,
                tikker=tikker,
                reserve=reserve,
                min=min,
                max=max,
                payment_option=payment_option,
            )
        )
        return new_currency
