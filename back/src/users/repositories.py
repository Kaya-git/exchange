"""  User repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User
from database.abstract_repo import Repository
from database.engines import async_session_maker


class UserRepo(Repository[User]):
    """
    User repository for CRUD
    and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize User
        repository as for all User
        or only for one
        """
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        email: str,
        hashed_password: str = None,
        first_name: str = None,
        second_name: str = None,
    ) -> None:

        new_user = await self.session.merge(
            User(
                email=email,
                hashed_password=hashed_password,
                first_name=first_name,
                second_name=second_name,
            )
        )
        return new_user

    async def find_by_email(
            self,
            email
    ):
        async with async_session_maker() as session:
            statement = select(User).where(User.email==email)
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    async def get_curr_user(
            self,
            ident: int
    ):
        async with async_session_maker() as session:
            statement = select(User).where(User.id==ident)
            result = await session.execute(statement)
            return result.scalar_one_or_none()
