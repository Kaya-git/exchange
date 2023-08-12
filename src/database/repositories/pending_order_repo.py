""" PendingOrder repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import PendingOrder
from .abstract import Repository


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
        get_value: float,
        send_value: float,
        cc_num: int,
        cc_holder: str,
        cc_image_name: str,
    ) -> None:

        new_pending_order = await self.session.merge(
            PendingOrder(
                email=email,
                get_value=get_value,
                send_value=send_value,
                cc_num=cc_num,
                cc_holder=cc_holder,
                cc_image_name=cc_image_name,
            )
        )
        return new_pending_order
