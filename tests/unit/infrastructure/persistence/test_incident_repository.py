from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from orinfra_sentinelops.domain.enums.incident import (
    IncidentSeverity,
    IncidentStatus,
)
from orinfra_sentinelops.domain.models.incident import Incident
from orinfra_sentinelops.infrastructure.persistence.models import Base
from orinfra_sentinelops.infrastructure.persistence.repositories.incident_repository import (
    SqlAlchemyIncidentRepository,
)


@pytest.fixture
async def repository() -> SqlAlchemyIncidentRepository:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    session = session_factory()

    try:
        yield SqlAlchemyIncidentRepository(session)
    finally:
        await session.close()
        await engine.dispose()


def build_incident() -> Incident:
    return Incident(
        incident_id="INC-REPO-001",
        title="Feature pipeline regression",
        description="Feature transformation caused model degradation.",
        severity=IncidentSeverity.HIGH,
        status=IncidentStatus.DETECTED,
        detected_at=datetime(2026, 9, 9, 10, 0, tzinfo=UTC),
        affected_components=[
            "feature-pipeline",
            "fraud-model",
        ],
        environment="production",
        service="fraud-service",
        trace_ids=[
            "trace-001",
            "trace-002",
        ],
        metadata={
            "model_version": "fraud-model-v3",
            "feature_version": "1.1",
        },
    )


@pytest.mark.asyncio
async def test_save_and_get_incident(
    repository: SqlAlchemyIncidentRepository,
) -> None:
    incident = build_incident()

    saved = await repository.save(incident)
    retrieved = await repository.get_by_id("INC-REPO-001")

    assert saved == incident
    assert retrieved == incident


@pytest.mark.asyncio
async def test_get_missing_incident_returns_none(
    repository: SqlAlchemyIncidentRepository,
) -> None:
    result = await repository.get_by_id("DOES-NOT-EXIST")

    assert result is None


@pytest.mark.asyncio
async def test_update_incident(
    repository: SqlAlchemyIncidentRepository,
) -> None:
    incident = build_incident()

    await repository.save(incident)

    updated = incident.model_copy(
        update={
            "status": IncidentStatus.INVESTIGATING,
            "description": "Investigation is now in progress.",
        }
    )

    result = await repository.update(updated)

    assert result.status == IncidentStatus.INVESTIGATING
    assert result.description == "Investigation is now in progress."

    retrieved = await repository.get_by_id("INC-REPO-001")

    assert retrieved is not None
    assert retrieved.status == IncidentStatus.INVESTIGATING
    assert retrieved.description == "Investigation is now in progress."


@pytest.mark.asyncio
async def test_update_missing_incident_raises(
    repository: SqlAlchemyIncidentRepository,
) -> None:
    with pytest.raises(ValueError, match="Incident not found"):
        await repository.update(build_incident())


@pytest.mark.asyncio
async def test_delete_incident(
    repository: SqlAlchemyIncidentRepository,
) -> None:
    incident = build_incident()

    await repository.save(incident)
    await repository.delete("INC-REPO-001")

    result = await repository.get_by_id("INC-REPO-001")

    assert result is None


@pytest.mark.asyncio
async def test_delete_missing_incident_is_idempotent(
    repository: SqlAlchemyIncidentRepository,
) -> None:
    await repository.delete("DOES-NOT-EXIST")
