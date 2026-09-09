from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from orinfra_sentinelops.application.services.incident_service import IncidentService
from orinfra_sentinelops.domain.enums.incident import IncidentStatus
from orinfra_sentinelops.domain.models.incident import Incident
from orinfra_sentinelops.presentation.api.dependencies.incident import (
    get_incident_service,
)
from orinfra_sentinelops.presentation.api.schemas.incident import (
    IncidentCreateRequest,
    IncidentResolveRequest,
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


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
async def get_incident(
    incident_id: str,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    """Return an incident by ID."""
    try:
        incident = await service.get_incident(incident_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident '{incident_id}' not found.",
        ) from exc

    return IncidentResponse.model_validate(incident)


@router.post(
    "/{incident_id}/investigate",
    response_model=IncidentResponse,
)
async def start_investigation(
    incident_id: str,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    """Start investigation for an incident."""
    try:
        incident = await service.start_investigation(incident_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return IncidentResponse.model_validate(incident)


@router.post(
    "/{incident_id}/resolve",
    response_model=IncidentResponse,
)
async def resolve_incident(
    incident_id: str,
    request: IncidentResolveRequest,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    """Resolve an incident."""
    try:
        incident = await service.resolve_incident(
            incident_id,
            request.resolved_at,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return IncidentResponse.model_validate(incident)


@router.post(
    "/{incident_id}/close",
    response_model=IncidentResponse,
)
async def close_incident(
    incident_id: str,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    """Close a resolved incident."""
    try:
        incident = await service.close_incident(incident_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return IncidentResponse.model_validate(incident)
