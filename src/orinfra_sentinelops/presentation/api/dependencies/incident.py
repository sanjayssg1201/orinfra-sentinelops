from collections.abc import AsyncGenerator

from orinfra_sentinelops.application.services.incident_service import IncidentService
from orinfra_sentinelops.infrastructure.persistence.database import get_session
from orinfra_sentinelops.infrastructure.persistence.repositories.incident_repository import (
    SqlAlchemyIncidentRepository,
)


async def get_incident_service() -> AsyncGenerator[IncidentService, None]:
    """Provide an IncidentService backed by the configured database."""
    async for session in get_session():
        repository = SqlAlchemyIncidentRepository(session)
        yield IncidentService(repository)
