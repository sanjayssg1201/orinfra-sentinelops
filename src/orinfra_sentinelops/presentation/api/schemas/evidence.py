from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EvidenceCreateRequest(BaseModel):
    """Request payload for creating investigation evidence."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1, max_length=100)
    evidence_type: str = Field(min_length=1, max_length=100)
    observed_at: datetime
    component: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1)
    value: object
    trace_id: str | None = None
    request_id: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)


class EvidenceResponse(BaseModel):
    """API response for investigation evidence."""

    model_config = ConfigDict(from_attributes=True)

    evidence_id: str
    source: str
    evidence_type: str
    observed_at: datetime
    component: str
    summary: str
    value: object
    trace_id: str | None
    request_id: str | None
    confidence: float
