from abc import ABC, abstractmethod

from orinfra_sentinelops.domain.models.remediation import Remediation


class RemediationRepository(ABC):
    """Persistence boundary for remediation actions."""

    @abstractmethod
    async def save(self, remediation: Remediation) -> Remediation:
        """Persist a remediation and return the persisted entity."""
        ...

    @abstractmethod
    async def get_by_id(self, remediation_id: str) -> Remediation | None:
        """Return a remediation by ID, or None when it does not exist."""
        ...

    @abstractmethod
    async def update(self, remediation: Remediation) -> Remediation:
        """Update a remediation and return the persisted entity."""
        ...

    @abstractmethod
    async def delete(self, remediation_id: str) -> None:
        """Delete a remediation by ID."""
        ...
