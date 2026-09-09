import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine

from orinfra_sentinelops.infrastructure.persistence.database import engine
from orinfra_sentinelops.infrastructure.persistence.models import Base


@pytest.mark.asyncio
async def test_database_engine_is_async() -> None:
    assert isinstance(engine, AsyncEngine)


@pytest.mark.asyncio
async def test_database_can_create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with engine.connect() as connection:
        table_names = await connection.run_sync(
            lambda sync_connection: inspect(sync_connection).get_table_names()
        )

    assert "incidents" in table_names


@pytest.mark.asyncio
async def test_incidents_table_contains_expected_columns() -> None:
    async with engine.connect() as connection:
        columns = await connection.run_sync(
            lambda sync_connection: inspect(sync_connection).get_columns("incidents")
        )

    column_names = {column["name"] for column in columns}

    assert column_names == {
        "incident_id",
        "title",
        "description",
        "severity",
        "status",
        "detected_at",
        "resolved_at",
        "affected_components",
        "environment",
        "service",
        "trace_ids",
        "metadata",
    }
