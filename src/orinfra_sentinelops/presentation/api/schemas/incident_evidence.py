from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class IncidentEvidenceCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=50)
    relevance_score: float = Field(ge=0.0, le=1.0)


class IncidentEvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    incident_id: str
    evidence_id: str
    role: str
    relevance_score: float
    linked_at: datetime
