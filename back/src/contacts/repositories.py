"""  Contact repository file """
from sqlalchemy.ext.asyncio import AsyncSession

from database.abstract_repo import Repository

from .models import Contact


class ContactRepo(Repository[Contact]):
    """
    Contact repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize Contact repository as for all Contacts
        or only for one
        """
        super().__init__(type_model=Contact, session=session)

    async def new(
        self,
        name: str,
        link: str
    ) -> None:

        new_contact = await self.session.merge(
            Contact(
                name=name,
                link=link
            )
        )
        return new_contact
