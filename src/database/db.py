from typing import Union

from fastapi import Depends
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import conf
from database.repositories import (
    UserRepo, OrderRepo,
    CurrencyRepo, PaymentOptionRepo,
    CommissionsRepo, PendingOrderRepo,
    ReviewRepo,
)
from typing import AsyncGenerator


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    """
    :param url:
    :return:
    """
    return _create_async_engine(
        url=url, echo=conf.debug,
        pool_pre_ping=True
    )


def create_session_maker(engine: AsyncEngine = None) -> sessionmaker:
    """
    :param url:
    :return:
    """
    return sessionmaker(
        engine or create_async_engine(conf.db.build_connection_str()),
        class_=AsyncSession,
        expire_on_commit=False
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with create_session_maker() as session:
        yield session


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

    commissions: CommissionsRepo
    """ Commissions option repository """

    pending_order: PendingOrderRepo
    """ Pending order option repository """

    review: ReviewRepo

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session()),
        user: UserRepo = None,
        order: OrderRepo = None,
        currency: CurrencyRepo = None,
        payment_option: PaymentOptionRepo = None,
        commissions: CommissionsRepo = None,
        pending_order: PendingOrderRepo = None,
        review: ReviewRepo = None,
    ) -> None:

        self.session = session
        self.user = user or UserRepo(session=session)
        self.order = order or OrderRepo(session=session)
        self.currency = currency or CurrencyRepo(session=session)
        self.payment_option = payment_option or PaymentOptionRepo(
            session=session
        )
        self.commissions = commissions or CommissionsRepo(
            session=session
        )
        self.pending_order = pending_order or PendingOrderRepo(
            session=session
        )
        self.review = review or ReviewRepo(
            session=session
        )
