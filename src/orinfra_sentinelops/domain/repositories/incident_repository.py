from abc import ABC, abstractmethod

from orinfra_sentinelops.domain.models.incident import Incident


class IncidentRepository(ABC):
    """Persistence boundary for incident aggregates."""

    @abstractmethod
    async def save(self, incident: Incident) -> Incident:
        """Persist an incident and return the persisted entity."""
        ...

    @abstractmethod
    async def get_by_id(self, incident_id: str) -> Incident | None:
        """Return an incident by ID, or None when it does not exist."""
        ...

    @abstractmethod
    async def update(self, incident: Incident) -> Incident:
        """Update an existing incident and return the persisted entity."""
        ...

    @abstractmethod
    async def delete(self, incident_id: str) -> None:
        """Delete an incident by ID."""
        ...
