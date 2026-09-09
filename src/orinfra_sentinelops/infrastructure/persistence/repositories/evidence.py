from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orinfra_sentinelops.domain.models.evidence import Evidence
from orinfra_sentinelops.domain.repositories.evidence_repository import EvidenceRepository
from orinfra_sentinelops.infrastructure.persistence.models.evidence import EvidenceORM


class SqlAlchemyEvidenceRepository(EvidenceRepository):
    """SQLAlchemy implementation of the evidence repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, evidence: Evidence) -> Evidence:
        """Persist evidence and return the saved domain object."""
        orm = EvidenceORM(
            evidence_id=evidence.evidence_id,
            source=evidence.source,
            evidence_type=evidence.evidence_type,
            observed_at=evidence.observed_at,
            component=evidence.component,
            summary=evidence.summary,
            value=evidence.value,
            trace_id=evidence.trace_id,
            request_id=evidence.request_id,
            confidence=evidence.confidence,
        )

        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)

        return self._to_domain(orm)

    async def get_by_id(self, evidence_id: str) -> Evidence | None:
        """Retrieve evidence by its identifier."""
        result = await self._session.execute(
            select(EvidenceORM).where(EvidenceORM.evidence_id == evidence_id)
        )
        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return self._to_domain(orm)

    async def delete(self, evidence_id: str) -> None:
        """Delete evidence if it exists."""
        result = await self._session.execute(
            select(EvidenceORM).where(EvidenceORM.evidence_id == evidence_id)
        )
        orm = result.scalar_one_or_none()

        if orm is None:
            return

        await self._session.delete(orm)
        await self._session.commit()

    @staticmethod
    def _to_domain(orm: EvidenceORM) -> Evidence:
        """Convert a persistence model into a domain model."""
        return Evidence(
            evidence_id=orm.evidence_id,
            source=orm.source,
            evidence_type=orm.evidence_type,
            observed_at=orm.observed_at,
            component=orm.component,
            summary=orm.summary,
            value=orm.value,
            trace_id=orm.trace_id,
            request_id=orm.request_id,
            confidence=orm.confidence,
        )
