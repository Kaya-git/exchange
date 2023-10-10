""" Commissions repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Commissions
from .abstract import Repository


class CommissionsRepo(Repository[Commissions]):
    """
    Commissions repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize Commissions repository
        as for all Commissions or only for one
        """
        super().__init__(type_model=Commissions, session=session)

    async def new(
        self,
        margin: float,
        gas: float,
    ) -> None:

        new_commissions = await self.session.merge(
            Commissions(
                margin=margin,
                gas=gas,
            )
        )
        return new_commissions
