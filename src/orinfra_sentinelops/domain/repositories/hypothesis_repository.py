from abc import ABC, abstractmethod

from orinfra_sentinelops.domain.models.hypothesis import Hypothesis


class HypothesisRepository(ABC):
    """Persistence boundary for RCA hypotheses."""

    @abstractmethod
    async def save(self, hypothesis: Hypothesis) -> Hypothesis:
        """Persist a hypothesis and return the persisted entity."""
        ...

    @abstractmethod
    async def get_by_id(self, hypothesis_id: str) -> Hypothesis | None:
        """Return a hypothesis by ID, or None when it does not exist."""
        ...

    @abstractmethod
    async def delete(self, hypothesis_id: str) -> None:
        """Delete a hypothesis by ID."""
        ...
