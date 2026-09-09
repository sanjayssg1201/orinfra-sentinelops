from datetime import UTC, datetime

import pytest

from orinfra_sentinelops.application.services.incident_service import (
    IncidentService,
)
from orinfra_sentinelops.domain.enums.incident import (
    IncidentSeverity,
    IncidentStatus,
)
from orinfra_sentinelops.domain.models.incident import Incident
from orinfra_sentinelops.domain.repositories.incident_repository import (
    IncidentRepository,
)


class InMemoryIncidentRepository(IncidentRepository):
    """In-memory repository used for application-layer tests."""

    def __init__(self) -> None:
        self._incidents: dict[str, Incident] = {}

    async def save(self, incident: Incident) -> Incident:
        self._incidents[incident.incident_id] = incident
        return incident

    async def get_by_id(self, incident_id: str) -> Incident | None:
        return self._incidents.get(incident_id)

    async def update(self, incident: Incident) -> Incident:
        self._incidents[incident.incident_id] = incident
        return incident

    async def delete(self, incident_id: str) -> None:
        self._incidents.pop(incident_id, None)


def build_incident(
    status: IncidentStatus = IncidentStatus.DETECTED,
) -> Incident:
    return Incident(
        incident_id="INC-001",
        title="Feature pipeline regression",
        description="Feature transformation changed unexpectedly.",
        severity=IncidentSeverity.HIGH,
        status=status,
        detected_at=datetime(2026, 9, 9, 10, 0, tzinfo=UTC),
        affected_components=["feature-pipeline", "fraud-model"],
        environment="test",
        service="fraud-service",
    )


@pytest.mark.asyncio
async def test_create_and_get_incident() -> None:
    repository = InMemoryIncidentRepository()
    service = IncidentService(repository)

    incident = build_incident()

    created = await service.create_incident(incident)
    retrieved = await service.get_incident("INC-001")

    assert created == incident
    assert retrieved == incident


@pytest.mark.asyncio
async def test_duplicate_incident_is_rejected() -> None:
    repository = InMemoryIncidentRepository()
    service = IncidentService(repository)

    incident = build_incident()

    await service.create_incident(incident)

    with pytest.raises(ValueError, match="Incident already exists"):
        await service.create_incident(incident)


@pytest.mark.asyncio
async def test_incident_lifecycle() -> None:
    repository = InMemoryIncidentRepository()
    service = IncidentService(repository)

    await service.create_incident(build_incident())

    investigating = await service.start_investigation("INC-001")

    assert investigating.status == IncidentStatus.INVESTIGATING

    resolved_at = datetime(2026, 9, 9, 11, 0, tzinfo=UTC)

    resolved = await service.resolve_incident(
        "INC-001",
        resolved_at,
    )

    assert resolved.status == IncidentStatus.RESOLVED
    assert resolved.resolved_at == resolved_at

    closed = await service.close_incident("INC-001")

    assert closed.status == IncidentStatus.CLOSED


@pytest.mark.asyncio
async def test_invalid_status_transition_is_rejected() -> None:
    repository = InMemoryIncidentRepository()
    service = IncidentService(repository)

    await service.create_incident(build_incident())

    with pytest.raises(
        ValueError,
        match="Incident cannot be resolved",
    ):
        await service.resolve_incident(
            "INC-001",
            datetime(2026, 9, 9, 11, 0, tzinfo=UTC),
        )


@pytest.mark.asyncio
async def test_resolution_before_detection_is_rejected() -> None:
    repository = InMemoryIncidentRepository()
    service = IncidentService(repository)

    await service.create_incident(build_incident())
    await service.start_investigation("INC-001")

    with pytest.raises(
        ValueError,
        match="resolved_at cannot be earlier",
    ):
        await service.resolve_incident(
            "INC-001",
            datetime(2026, 9, 9, 9, 0, tzinfo=UTC),
        )
