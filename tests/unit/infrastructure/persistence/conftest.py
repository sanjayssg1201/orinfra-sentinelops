from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection

from orinfra_sentinelops.infrastructure.persistence.database import engine
from orinfra_sentinelops.infrastructure.persistence.models import Base


@pytest.fixture
async def database_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield connection

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
