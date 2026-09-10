from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orinfra_sentinelops.domain.models.incident_evidence import IncidentEvidenceLink
from orinfra_sentinelops.domain.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)
from orinfra_sentinelops.infrastructure.persistence.models.incident_evidence import (
    IncidentEvidenceLinkORM,
)


class SqlAlchemyIncidentEvidenceRepository(IncidentEvidenceRepository):
    """SQLAlchemy implementation of the incident-evidence repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(
        self,
        link: IncidentEvidenceLink,
    ) -> IncidentEvidenceLink:
        orm = IncidentEvidenceLinkORM(
            incident_id=link.incident_id,
            evidence_id=link.evidence_id,
            role=link.role,
            relevance_score=link.relevance_score,
            linked_at=link.linked_at,
        )

        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)

        return self._to_domain(orm)

    async def exists(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> bool:
        result = await self._session.execute(
            select(IncidentEvidenceLinkORM).where(
                IncidentEvidenceLinkORM.incident_id == incident_id,
                IncidentEvidenceLinkORM.evidence_id == evidence_id,
            )
        )

        return result.scalar_one_or_none() is not None

    async def list_by_incident(
        self,
        incident_id: str,
    ) -> list[IncidentEvidenceLink]:
        result = await self._session.execute(
            select(IncidentEvidenceLinkORM)
            .where(IncidentEvidenceLinkORM.incident_id == incident_id)
            .order_by(IncidentEvidenceLinkORM.linked_at)
        )

        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def delete(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> None:
        result = await self._session.execute(
            select(IncidentEvidenceLinkORM).where(
                IncidentEvidenceLinkORM.incident_id == incident_id,
                IncidentEvidenceLinkORM.evidence_id == evidence_id,
            )
        )

        orm = result.scalar_one_or_none()

        if orm is None:
            return

        await self._session.delete(orm)
        await self._session.commit()

    @staticmethod
    def _to_domain(
        orm: IncidentEvidenceLinkORM,
    ) -> IncidentEvidenceLink:
        return IncidentEvidenceLink(
            incident_id=orm.incident_id,
            evidence_id=orm.evidence_id,
            role=orm.role,
            relevance_score=orm.relevance_score,
            linked_at=orm.linked_at,
        )
