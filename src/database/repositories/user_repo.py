""" User repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Role, User
from .abstract import Repository


class UserRepo(Repository[User]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize User repository as for all Users
        or only for one
        """
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        user_name: str,
        email: str,
        hashed_password: str,
        role: Role = Role.User,
        
    ) -> None:

        new_user = await self.session.merge(
            User(
                user_name=user_name,
                email=email,
                hashed_password=hashed_password,
                role=role
            )
        )
        return new_user
