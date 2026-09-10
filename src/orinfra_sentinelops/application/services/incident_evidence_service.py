from orinfra_sentinelops.domain.models.incident_evidence import IncidentEvidenceLink
from orinfra_sentinelops.domain.repositories.incident_evidence_repository import (
    IncidentEvidenceRepository,
)


class IncidentEvidenceService:
    """Application service for managing incident-evidence associations."""

    def __init__(self, repository: IncidentEvidenceRepository) -> None:
        self._repository = repository

    async def link_evidence(
        self,
        link: IncidentEvidenceLink,
    ) -> IncidentEvidenceLink:
        """Associate evidence with an incident."""
        if await self._repository.exists(link.incident_id, link.evidence_id):
            raise ValueError(
                f"Evidence '{link.evidence_id}' is already linked to incident '{link.incident_id}'."
            )

        return await self._repository.save(link)

    async def evidence_exists(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> bool:
        """Check whether evidence is linked to an incident."""
        return await self._repository.exists(incident_id, evidence_id)

    async def list_evidence(
        self,
        incident_id: str,
    ) -> list[IncidentEvidenceLink]:
        """List evidence associations for an incident."""
        return await self._repository.list_by_incident(incident_id)

    async def unlink_evidence(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> None:
        """Remove an evidence association."""
        await self._repository.delete(incident_id, evidence_id)
