"""  FAQ repository file """
from sqlalchemy.ext.asyncio import AsyncSession

from database.abstract_repo import Repository

from .models import FAQ


class FAQRepo(Repository[FAQ]):
    """
    FAQ repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize FAQ repository as for all FAQ
        or only for one
        """
        super().__init__(type_model=FAQ, session=session)

    async def new(
        self,
        question: str,
        answer: str
    ) -> None:

        new_faq = await self.session.merge(
            FAQ(
                question=question,
                answer=answer
            )
        )
        return new_faq
