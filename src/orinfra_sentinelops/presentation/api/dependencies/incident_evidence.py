from collections.abc import AsyncGenerator

from orinfra_sentinelops.application.services.incident_evidence_service import (
    IncidentEvidenceService,
)
from orinfra_sentinelops.infrastructure.persistence.database import get_session
from orinfra_sentinelops.infrastructure.persistence.repositories.incident_evidence import (
    SqlAlchemyIncidentEvidenceRepository,
)


async def get_incident_evidence_service() -> AsyncGenerator[
    IncidentEvidenceService,
    None,
]:
    """Provide an IncidentEvidenceService backed by the configured database."""
    async for session in get_session():
        repository = SqlAlchemyIncidentEvidenceRepository(session)
        yield IncidentEvidenceService(repository)
