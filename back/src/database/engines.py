from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from config import conf
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
