from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, status

from orinfra_sentinelops.application.services.incident_service import IncidentService
from orinfra_sentinelops.domain.enums.incident import IncidentStatus
from orinfra_sentinelops.domain.models.incident import Incident
from orinfra_sentinelops.presentation.api.dependencies.incident import (
    get_incident_service,
)
from orinfra_sentinelops.presentation.api.schemas.incident import (
    IncidentCreateRequest,
    IncidentResponse,
)

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_incident(
    request: IncidentCreateRequest,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    """Create a new production incident."""
    incident = Incident(
        incident_id=f"INC-{uuid4().hex[:12].upper()}",
        title=request.title,
        description=request.description,
        severity=request.severity,
        status=IncidentStatus.DETECTED,
        detected_at=datetime.now(UTC),
        resolved_at=None,
        affected_components=request.affected_components,
        environment=request.environment,
        service=request.service,
        trace_ids=request.trace_ids,
        metadata={str(key): str(value) for key, value in request.metadata.items()},
    )

    created = await service.create_incident(incident)

    return IncidentResponse.model_validate(created)
