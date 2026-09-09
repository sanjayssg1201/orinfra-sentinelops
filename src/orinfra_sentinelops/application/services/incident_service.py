from datetime import datetime

from orinfra_sentinelops.domain.enums.incident import IncidentStatus
from orinfra_sentinelops.domain.models.incident import Incident
from orinfra_sentinelops.domain.repositories.incident_repository import (
    IncidentRepository,
)


class IncidentService:
    """Application service for incident lifecycle management."""

    def __init__(self, repository: IncidentRepository) -> None:
        self._repository = repository

    async def create_incident(self, incident: Incident) -> Incident:
        """Create and persist a new incident."""
        existing = await self._repository.get_by_id(incident.incident_id)

        if existing is not None:
            raise ValueError(f"Incident already exists: {incident.incident_id}")

        return await self._repository.save(incident)

    async def get_incident(self, incident_id: str) -> Incident:
        """Retrieve an incident by ID."""
        incident = await self._repository.get_by_id(incident_id)

        if incident is None:
            raise ValueError(f"Incident not found: {incident_id}")

        return incident

    async def start_investigation(
        self,
        incident_id: str,
    ) -> Incident:
        """Transition a detected incident into investigation."""
        incident = await self.get_incident(incident_id)

        if incident.status != IncidentStatus.DETECTED:
            raise ValueError(
                f"Incident cannot start investigation from status '{incident.status}'."
            )

        updated = incident.model_copy(update={"status": IncidentStatus.INVESTIGATING})

        return await self._repository.update(updated)

    async def resolve_incident(
        self,
        incident_id: str,
        resolved_at: datetime,
    ) -> Incident:
        """Transition an investigated incident into resolved."""
        incident = await self.get_incident(incident_id)

        if incident.status != IncidentStatus.INVESTIGATING:
            raise ValueError(f"Incident cannot be resolved from status '{incident.status}'.")

        if resolved_at < incident.detected_at:
            raise ValueError("resolved_at cannot be earlier than detected_at.")

        updated = incident.model_copy(
            update={
                "status": IncidentStatus.RESOLVED,
                "resolved_at": resolved_at,
            }
        )

        return await self._repository.update(updated)

    async def close_incident(self, incident_id: str) -> Incident:
        """Transition a resolved incident into closed."""
        incident = await self.get_incident(incident_id)

        if incident.status != IncidentStatus.RESOLVED:
            raise ValueError(f"Incident cannot be closed from status '{incident.status}'.")

        updated = incident.model_copy(update={"status": IncidentStatus.CLOSED})

        return await self._repository.update(updated)
