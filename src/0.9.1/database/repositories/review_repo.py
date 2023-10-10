""" Review repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Review, User, Mark
from .abstract import Repository


class ReviewRepo(Repository[Review]):
    """
    Review repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize review repository as for all reviews or only for one Review
        """
        super().__init__(type_model=Review, session=session)

    async def new(
        self,
        author: User,
        text: str,
        mark: Mark,
    ) -> None:

        new_review = await self.session.merge(
            Review(
                author=author,
                text=text,
                mark=mark,
            )
        )
        return new_review
