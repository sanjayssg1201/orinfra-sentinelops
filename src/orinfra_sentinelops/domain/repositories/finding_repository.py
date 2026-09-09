from abc import ABC, abstractmethod

from orinfra_sentinelops.domain.models.finding import Finding


class FindingRepository(ABC):
    """Persistence boundary for investigation findings."""

    @abstractmethod
    async def save(self, finding: Finding) -> Finding:
        """Persist a finding and return the persisted entity."""
        ...

    @abstractmethod
    async def get_by_id(self, finding_id: str) -> Finding | None:
        """Return a finding by ID, or None when it does not exist."""
        ...

    @abstractmethod
    async def delete(self, finding_id: str) -> None:
        """Delete a finding by ID."""
        ...
