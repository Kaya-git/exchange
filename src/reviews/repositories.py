"""  Review repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from enums import Mark
from users import User
from reviews import Review
from database.abstract_repo import Repository


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
        user_email: User,
        text: str,
        rating: Mark
    ) -> None:

        new_review = await self.session.merge(
            Review(
                user_email=user_email,
                text=text,
                rating=rating,
            )
        )
        return new_review
