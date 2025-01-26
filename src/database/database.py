from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.config import get_config
from core.logger import Logger

config = get_config()
logger = Logger.get_logger(__name__)


class Database(object):
    def __init__(self):
        self.engine = create_async_engine(
            url=config.db_url,
            echo=config.DEBUG,
            pool_size=5,
            max_overflow=10,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @asynccontextmanager
    async def session(self):
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except Exception as e:
            logger.info("Session rollback because of exception: %s", e)
            await session.rollback()
        finally:
            await session.close()
