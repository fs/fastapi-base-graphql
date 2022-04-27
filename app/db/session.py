from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base_class import Base


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
        self._session_local = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession, autoflush=False,
                                           autocommit=False)
        self._session = async_scoped_session(self._session_local)

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


session = AsyncDatabaseSession()
