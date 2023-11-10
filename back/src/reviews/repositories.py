"""  Review repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from enums import Mark
from reviews.models import Review
from database.abstract_repo import Repository
from datetime import datetime


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
        rating: Mark,
        user_id: int,
        moderated: bool,
        data: datetime = datetime.utcnow(),
    ) -> None:

        new_review = await self.session.merge(
            Review(
                user_id=user_id,
                text=text,
                rating=rating,
                data=data,
                moderated=moderated
            )
        )
        return new_review
