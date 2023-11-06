"""  FAQ repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from .models import FAQ
from database.abstract_repo import Repository
from typing import List


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
        question: str | List[str],
        answer: str | List[str]
    ) -> None:

        new_question_answer = await self.session.merge(
            FAQ(
                question=question,
                answer=answer
            )
        )
        return new_question_answer
