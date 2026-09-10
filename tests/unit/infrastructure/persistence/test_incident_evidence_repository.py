from datetime import UTC, datetime

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from orinfra_sentinelops.domain.models.incident_evidence import IncidentEvidenceLink
from orinfra_sentinelops.infrastructure.persistence.models.base import Base
from orinfra_sentinelops.infrastructure.persistence.repositories.incident_evidence import (
    SqlAlchemyIncidentEvidenceRepository,
)


@pytest.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    await engine.dispose()


def build_link(
    incident_id: str = "INC-001",
    evidence_id: str = "EVD-001",
    role: str = "supporting",
    relevance_score: float = 0.92,
) -> IncidentEvidenceLink:
    return IncidentEvidenceLink(
        incident_id=incident_id,
        evidence_id=evidence_id,
        role=role,
        relevance_score=relevance_score,
        linked_at=datetime.now(UTC),
    )


@pytest.mark.asyncio
async def test_save_and_get_link(session: AsyncSession) -> None:
    repository = SqlAlchemyIncidentEvidenceRepository(session)
    link = build_link()

    saved = await repository.save(link)
    retrieved = await repository.list_by_incident("INC-001")

    assert saved == link
    assert retrieved == [link]


@pytest.mark.asyncio
async def test_exists_returns_true_for_existing_link(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyIncidentEvidenceRepository(session)

    await repository.save(build_link())

    assert await repository.exists("INC-001", "EVD-001") is True


@pytest.mark.asyncio
async def test_exists_returns_false_for_missing_link(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyIncidentEvidenceRepository(session)

    assert await repository.exists("INC-001", "EVD-999") is False


@pytest.mark.asyncio
async def test_list_by_incident_returns_only_matching_links(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyIncidentEvidenceRepository(session)

    first = build_link("INC-001", "EVD-001")
    second = build_link("INC-001", "EVD-002")
    unrelated = build_link("INC-002", "EVD-003")

    await repository.save(first)
    await repository.save(second)
    await repository.save(unrelated)

    results = await repository.list_by_incident("INC-001")

    assert results == [first, second]


@pytest.mark.asyncio
async def test_delete_removes_link(session: AsyncSession) -> None:
    repository = SqlAlchemyIncidentEvidenceRepository(session)

    await repository.save(build_link())

    await repository.delete("INC-001", "EVD-001")

    assert await repository.exists("INC-001", "EVD-001") is False


@pytest.mark.asyncio
async def test_delete_missing_link_is_noop(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyIncidentEvidenceRepository(session)

    await repository.delete("INC-001", "EVD-999")

    assert await repository.list_by_incident("INC-001") == []


@pytest.mark.asyncio
async def test_composite_key_prevents_duplicate_link(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyIncidentEvidenceRepository(session)

    await repository.save(build_link())

    with pytest.raises(IntegrityError):
        await repository.save(build_link())

    await session.rollback()
