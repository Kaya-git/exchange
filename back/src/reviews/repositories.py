"""  Review repository file """
from database.abstract_repo import Repository
from reviews.models import Review
from sqlalchemy.ext.asyncio import AsyncSession


class ReviewRepo(Repository[Review]):
    """
    Review repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize Review repository as for all Review
        or only for one
        """
        super().__init__(type_model=Review, session=session)

    async def new(
        self,
        text: str,
        rating: int,
        name: str,
        moderated: bool,
    ) -> None:

        new_review = await self.session.merge(
            Review(
                name=name,
                text=text,
                rating=rating,
                moderated=moderated
            )
        )
        return new_review
