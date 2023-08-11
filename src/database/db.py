from typing import Union

from fastapi import Depends
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import conf
# from db.repositories import AuthorRepo, BookRepo, GenreRepo


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
        engine or create_async_engine(conf.db.build_connection_str),
        class_=AsyncSession,
        expire_on_commit=False
    )


class Database:
    """
    Database class is the highest abstraction level of database
    and can be used in the handlers or any other bot-side functions
    """

    author: AuthorRepo
    """ Author repository """

    book: BookRepo
    """ Book repository """

    genre: GenreRepo
    """ Genre repository """

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession = Depends(create_session_maker()),
        author: AuthorRepo = None,
        book: BookRepo = None,
        genre: GenreRepo = None,
    ) -> None:

        self.session = session
        self.author = author or AuthorRepo(session=session)
        self.book = book or BookRepo(session=session)
        self.genre = genre or GenreRepo(session=session)
