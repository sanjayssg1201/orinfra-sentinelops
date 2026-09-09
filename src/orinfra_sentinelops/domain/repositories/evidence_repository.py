from abc import ABC, abstractmethod

from orinfra_sentinelops.domain.models.evidence import Evidence


class EvidenceRepository(ABC):
    """Persistence boundary for evidence."""

    @abstractmethod
    async def save(self, evidence: Evidence) -> Evidence:
        """Persist evidence and return the persisted entity."""
        ...

    @abstractmethod
    async def get_by_id(self, evidence_id: str) -> Evidence | None:
        """Return evidence by ID, or None when it does not exist."""
        ...

    @abstractmethod
    async def delete(self, evidence_id: str) -> None:
        """Delete evidence by ID."""
        ...
