from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from orinfra_sentinelops.application.services.evidence_service import EvidenceService
from orinfra_sentinelops.domain.models.evidence import Evidence
from orinfra_sentinelops.presentation.api.dependencies.evidence import (
    get_evidence_service,
)
from orinfra_sentinelops.presentation.api.schemas.evidence import (
    EvidenceCreateRequest,
    EvidenceResponse,
)

router = APIRouter(
    prefix="/evidence",
    tags=["evidence"],
)


@router.post(
    "",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_evidence(
    request: EvidenceCreateRequest,
    service: EvidenceService = Depends(get_evidence_service),
) -> EvidenceResponse:
    """Create investigation evidence."""
    evidence = Evidence(
        evidence_id=f"EVD-{uuid4().hex[:12].upper()}",
        source=request.source,
        evidence_type=request.evidence_type,
        observed_at=request.observed_at,
        component=request.component,
        summary=request.summary,
        value=request.value,
        trace_id=request.trace_id,
        request_id=request.request_id,
        confidence=request.confidence,
    )

    created = await service.create_evidence(evidence)

    return EvidenceResponse.model_validate(created)


@router.get(
    "/{evidence_id}",
    response_model=EvidenceResponse,
)
async def get_evidence(
    evidence_id: str,
    service: EvidenceService = Depends(get_evidence_service),
) -> EvidenceResponse:
    """Return evidence by identifier."""
    try:
        evidence = await service.get_evidence(evidence_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence '{evidence_id}' not found.",
        ) from exc

    return EvidenceResponse.model_validate(evidence)


@router.delete(
    "/{evidence_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_evidence(
    evidence_id: str,
    service: EvidenceService = Depends(get_evidence_service),
) -> None:
    """Delete evidence by identifier."""
    try:
        await service.get_evidence(evidence_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence '{evidence_id}' not found.",
        ) from exc

    await service.delete_evidence(evidence_id)
