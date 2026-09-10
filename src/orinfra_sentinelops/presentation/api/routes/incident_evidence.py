from fastapi import APIRouter, Depends, HTTPException, status

from orinfra_sentinelops.application.services.incident_evidence_service import (
    IncidentEvidenceService,
)
from orinfra_sentinelops.domain.models.incident_evidence import IncidentEvidenceLink
from orinfra_sentinelops.presentation.api.dependencies.incident_evidence import (
    get_incident_evidence_service,
)
from orinfra_sentinelops.presentation.api.schemas.incident_evidence import (
    IncidentEvidenceCreateRequest,
    IncidentEvidenceResponse,
)

router = APIRouter(
    prefix="/incidents/{incident_id}/evidence",
    tags=["incident evidence"],
)


@router.post(
    "",
    response_model=IncidentEvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def link_evidence(
    incident_id: str,
    request: IncidentEvidenceCreateRequest,
    service: IncidentEvidenceService = Depends(get_incident_evidence_service),
) -> IncidentEvidenceResponse:
    """Link evidence to an incident."""
    link = IncidentEvidenceLink(
        incident_id=incident_id,
        evidence_id=request.evidence_id,
        role=request.role,
        relevance_score=request.relevance_score,
    )

    try:
        created = await service.link_evidence(link)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return IncidentEvidenceResponse.model_validate(created)


@router.get(
    "",
    response_model=list[IncidentEvidenceResponse],
)
async def list_incident_evidence(
    incident_id: str,
    service: IncidentEvidenceService = Depends(get_incident_evidence_service),
) -> list[IncidentEvidenceResponse]:
    """Return all evidence linked to an incident."""
    links = await service.list_evidence(incident_id)

    return [IncidentEvidenceResponse.model_validate(link) for link in links]


@router.delete(
    "/{evidence_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unlink_evidence(
    incident_id: str,
    evidence_id: str,
    service: IncidentEvidenceService = Depends(get_incident_evidence_service),
) -> None:
    """Remove evidence from an incident."""
    exists = await service.evidence_exists(incident_id, evidence_id)

    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(f"Evidence '{evidence_id}' is not linked to incident '{incident_id}'."),
        )

    await service.unlink_evidence(incident_id, evidence_id)
