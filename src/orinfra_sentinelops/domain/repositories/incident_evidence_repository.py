from abc import ABC, abstractmethod

from orinfra_sentinelops.domain.models.incident_evidence import IncidentEvidenceLink


class IncidentEvidenceRepository(ABC):
    """Persistence contract for incident-evidence associations."""

    @abstractmethod
    async def save(
        self,
        link: IncidentEvidenceLink,
    ) -> IncidentEvidenceLink: ...

    @abstractmethod
    async def exists(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> bool: ...

    @abstractmethod
    async def list_by_incident(
        self,
        incident_id: str,
    ) -> list[IncidentEvidenceLink]: ...

    @abstractmethod
    async def delete(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> None: ...
