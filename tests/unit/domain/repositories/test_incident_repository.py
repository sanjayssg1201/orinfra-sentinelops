from datetime import UTC, datetime

import pytest

from orinfra_sentinelops.domain.models.incident import (
    Incident,
)
from orinfra_sentinelops.domain.repositories.incident_repository import (
    IncidentRepository,
)


class InMemoryIncidentRepository(IncidentRepository):
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


def create_incident() -> Incident:
    return Incident(
        incident_id="INC-001",
        title="Feature pipeline regression",
        description="Feature transformation changed unexpectedly.",
        severity="high",
        detected_at=datetime.now(UTC),
        affected_components=["feature-pipeline", "fraud-model-v3"],
        environment="production",
        service="fraud-service",
    )


@pytest.mark.asyncio
async def test_repository_can_save_and_get_incident() -> None:
    repository = InMemoryIncidentRepository()
    incident = create_incident()

    await repository.save(incident)

    result = await repository.get_by_id("INC-001")

    assert result == incident


@pytest.mark.asyncio
async def test_repository_returns_none_for_unknown_incident() -> None:
    repository = InMemoryIncidentRepository()

    result = await repository.get_by_id("INC-404")

    assert result is None


@pytest.mark.asyncio
async def test_repository_can_update_incident() -> None:
    repository = InMemoryIncidentRepository()
    incident = create_incident()

    await repository.save(incident)

    updated = incident.model_copy(update={"title": "Updated feature pipeline regression"})

    result = await repository.update(updated)

    assert result.title == "Updated feature pipeline regression"
    assert await repository.get_by_id("INC-001") == updated


@pytest.mark.asyncio
async def test_repository_can_delete_incident() -> None:
    repository = InMemoryIncidentRepository()
    incident = create_incident()

    await repository.save(incident)
    await repository.delete("INC-001")

    assert await repository.get_by_id("INC-001") is None
