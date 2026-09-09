from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orinfra_sentinelops.domain.enums.incident import (
    IncidentSeverity,
    IncidentStatus,
)
from orinfra_sentinelops.domain.models.incident import Incident
from orinfra_sentinelops.domain.repositories.incident_repository import (
    IncidentRepository,
)
from orinfra_sentinelops.infrastructure.persistence.models.incident import (
    IncidentORM,
)


class SqlAlchemyIncidentRepository(IncidentRepository):
    """SQLAlchemy implementation of the incident repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, incident: Incident) -> Incident:
        orm = IncidentORM(
            incident_id=incident.incident_id,
            title=incident.title,
            description=incident.description,
            severity=incident.severity.value,
            status=incident.status.value,
            detected_at=incident.detected_at,
            resolved_at=incident.resolved_at,
            environment=incident.environment,
            service=incident.service,
            affected_components=incident.affected_components,
            trace_ids=incident.trace_ids,
            metadata_=incident.metadata,
        )

        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)

        return self._to_domain(orm)

    async def get_by_id(self, incident_id: str) -> Incident | None:
        result = await self._session.execute(
            select(IncidentORM).where(
                IncidentORM.incident_id == incident_id,
            )
        )

        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return self._to_domain(orm)

    async def update(self, incident: Incident) -> Incident:
        orm = await self._get_orm(incident.incident_id)

        if orm is None:
            raise ValueError(f"Incident not found: {incident.incident_id}")

        orm.title = incident.title
        orm.description = incident.description
        orm.severity = incident.severity.value
        orm.status = incident.status.value
        orm.detected_at = incident.detected_at
        orm.resolved_at = incident.resolved_at
        orm.environment = incident.environment
        orm.service = incident.service
        orm.affected_components = incident.affected_components
        orm.trace_ids = incident.trace_ids
        orm.metadata_ = incident.metadata

        await self._session.commit()
        await self._session.refresh(orm)

        return self._to_domain(orm)

    async def delete(self, incident_id: str) -> None:
        orm = await self._get_orm(incident_id)

        if orm is None:
            return

        await self._session.delete(orm)
        await self._session.commit()

    async def _get_orm(self, incident_id: str) -> IncidentORM | None:
        result = await self._session.execute(
            select(IncidentORM).where(
                IncidentORM.incident_id == incident_id,
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    def _to_domain(orm: IncidentORM) -> Incident:
        return Incident(
            incident_id=orm.incident_id,
            title=orm.title,
            description=orm.description,
            severity=IncidentSeverity(orm.severity),
            status=IncidentStatus(orm.status),
            detected_at=orm.detected_at,
            resolved_at=orm.resolved_at,
            affected_components=orm.affected_components,
            trace_ids=orm.trace_ids,
            metadata=orm.metadata_,
            environment=orm.environment,
            service=orm.service,
        )
