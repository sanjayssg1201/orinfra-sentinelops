from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class IncidentEvidenceLink(BaseModel):
    """Association between an incident and investigation evidence."""

    model_config = ConfigDict(extra="forbid")

    incident_id: str = Field(min_length=1, max_length=100)
    evidence_id: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=50)
    relevance_score: float = Field(ge=0.0, le=1.0)
    linked_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
