from config import conf
from contacts.repositories import ContactRepo
from currencies.repositories import CurrencyRepo
from faq.repositories import FAQRepo
from orders.repositories import OrderRepo
from payment_options.repositories import PaymentOptionRepo
from pendings.repositories import PendingAdminRepo
from reviews.repositories import ReviewRepo
from service_payment_options.repositories import ServicePaymentOptionRepo
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from users.repositories import UserRepo

from .base_model import Base

engine = _create_async_engine(
    url=conf.db.build_connection_str(),
    echo=conf.debug,
    pool_pre_ping=True
)


async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()


class Database:
    """
    Database class is the highest abstraction level of database
    and can be used in the handlers or any other bot-side functions
    """

    user: UserRepo
    """ User repository """

    order: OrderRepo
    """ Order repository """

    currency: CurrencyRepo
    """ Currency repository """

    payment_option: PaymentOptionRepo
    """ Payment option repository """

    service_payment_option: ServicePaymentOptionRepo
    """ Service payment option repository """

    review: ReviewRepo
    """ Reviews repository """

    faq: FAQRepo
    """ FAQ repository """

    contact: ContactRepo
    """ Contact repository """

    pending_admin: PendingAdminRepo
    """ Pending Admin repository """

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession = None,
        user: UserRepo = None,
        order: OrderRepo = None,
        currency: CurrencyRepo = None,
        payment_option: PaymentOptionRepo = None,
        service_payment_option: ServicePaymentOptionRepo = None,
        review: ReviewRepo = None,
        faq: FAQRepo = None,
        contact: ContactRepo = None,
        pending_admin: PendingAdminRepo = None
    ) -> None:

        self.session = session
        self.user = user or UserRepo(session=session)
        self.order = order or OrderRepo(session=session)
        self.currency = currency or CurrencyRepo(session=session)
        self.payment_option = payment_option or PaymentOptionRepo(
            session=session
        )
        self.service_payment_option = (
            service_payment_option or ServicePaymentOptionRepo(
                session=session
            )
        )
        self.review = review or ReviewRepo(
            session=session
        )
        self.faq = faq or FAQRepo(
            session=session
        )
        self.contact = contact or ContactRepo(
            session=session
        )
        self.pending_admin = pending_admin or PendingAdminRepo(
            session=session
        )
