from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from orinfra_sentinelops.infrastructure.persistence.settings import DatabaseSettings

settings = DatabaseSettings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.echo_sql,
)

session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
