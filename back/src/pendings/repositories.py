"""  PendingAdmin repository file """
from sqlalchemy.ext.asyncio import AsyncSession

from database.abstract_repo import Repository
from enums.models import ReqAction
from orders.models import Order
from reviews.models import Review

from .models import PendingAdmin


class PendingAdminRepo(Repository[PendingAdmin]):
    """
    PendingAdmin repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize PendingAdmin repository as for all PendingAdmin
        or only for one
        """
        super().__init__(type_model=PendingAdmin, session=session)

    async def new(
        self,
        req_act: ReqAction,
        order_id: Order = None,
        review_id: Review = None
    ) -> None:

        new_pending = await self.session.merge(
            PendingAdmin(
                req_act=req_act,
                order_id=order_id,
                review_id=review_id
            )
        )
        return new_pending
