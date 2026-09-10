from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from orinfra_sentinelops.domain.models.evidence import Evidence
from orinfra_sentinelops.infrastructure.persistence.models.base import Base
from orinfra_sentinelops.infrastructure.persistence.repositories.evidence import (
    SqlAlchemyEvidenceRepository,
)


@pytest.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session

    await engine.dispose()


def build_evidence(evidence_id: str = "EVD-001") -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        source="model-monitor",
        evidence_type="metric",
        observed_at=datetime.now(UTC),
        component="fraud-model",
        summary="Precision dropped significantly.",
        value={"precision": 0.71},
        trace_id="trace-001",
        request_id="request-001",
        confidence=0.94,
    )


@pytest.mark.asyncio
async def test_save_and_get_evidence(session: AsyncSession) -> None:
    repository = SqlAlchemyEvidenceRepository(session)
    evidence = build_evidence()

    saved = await repository.save(evidence)
    retrieved = await repository.get_by_id(evidence.evidence_id)

    assert saved == evidence
    assert retrieved == evidence


@pytest.mark.asyncio
async def test_get_missing_evidence_returns_none(session: AsyncSession) -> None:
    repository = SqlAlchemyEvidenceRepository(session)

    result = await repository.get_by_id("EVD-MISSING")

    assert result is None


@pytest.mark.asyncio
async def test_delete_evidence(session: AsyncSession) -> None:
    repository = SqlAlchemyEvidenceRepository(session)
    evidence = build_evidence()

    await repository.save(evidence)
    await repository.delete(evidence.evidence_id)

    result = await repository.get_by_id(evidence.evidence_id)

    assert result is None


@pytest.mark.asyncio
async def test_delete_missing_evidence_is_noop(session: AsyncSession) -> None:
    repository = SqlAlchemyEvidenceRepository(session)

    await repository.delete("EVD-MISSING")
