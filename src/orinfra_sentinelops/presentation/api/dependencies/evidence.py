from collections.abc import AsyncGenerator

from orinfra_sentinelops.application.services.evidence_service import EvidenceService
from orinfra_sentinelops.infrastructure.persistence.database import get_session
from orinfra_sentinelops.infrastructure.persistence.repositories.evidence import (
    SqlAlchemyEvidenceRepository,
)


async def get_evidence_service() -> AsyncGenerator[EvidenceService, None]:
    """Provide an EvidenceService backed by the configured database."""
    async for session in get_session():
        repository = SqlAlchemyEvidenceRepository(session)
        yield EvidenceService(repository)
