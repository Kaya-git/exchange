"""  PaymentOption repository file """
from sqlalchemy.ext.asyncio import AsyncSession
from enums import BankingType
from currencies import Currency
from payment_options import PaymentOption
from users import User
from database.abstract_repo import Repository


class PaymentOptionRepo(Repository[PaymentOption]):
    """
    PaymentOption repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize PaymentOption repository as for all PaymentOption
        or only for one
        """
        super().__init__(type_model=PaymentOption, session=session)

    async def new(
        self,
        user_id: User,
        banking_type: BankingType,
        currency_id: Currency,
        number: str,
        holder: str,
        is_verified: bool = False,
        image: str = None,
    ) -> None:

        new_payement_option = await self.session.merge(
            PaymentOption(
                banking_type=banking_type,
                currency_id=currency_id,
                number=number,
                holder=holder,
                is_verified=is_verified,
                image=image,
                user_id=user_id,
            )
        )
        return new_payement_option
