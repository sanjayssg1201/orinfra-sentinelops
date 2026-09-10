from orinfra_sentinelops.domain.models.evidence import Evidence
from orinfra_sentinelops.domain.repositories.evidence_repository import (
    EvidenceRepository,
)


class EvidenceService:
    """Application service for managing investigation evidence."""

    def __init__(self, repository: EvidenceRepository) -> None:
        self._repository = repository

    async def create_evidence(self, evidence: Evidence) -> Evidence:
        """Persist investigation evidence."""
        return await self._repository.save(evidence)

    async def get_evidence(self, evidence_id: str) -> Evidence:
        """Retrieve evidence by identifier."""
        evidence = await self._repository.get_by_id(evidence_id)

        if evidence is None:
            raise ValueError(f"Evidence not found: {evidence_id}")

        return evidence

    async def delete_evidence(self, evidence_id: str) -> None:
        """Delete evidence by identifier."""
        await self._repository.delete(evidence_id)
