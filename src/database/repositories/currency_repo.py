""" Currency repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Currency
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
        tikker: str
    ) -> None:

        new_currency = await self.session.merge(
            Currency(
                tikker=tikker
            )
        )
        return new_currency
