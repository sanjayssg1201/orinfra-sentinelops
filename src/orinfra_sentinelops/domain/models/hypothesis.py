from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class HypothesisStatus(StrEnum):
    PROPOSED = "proposed"
    TESTING = "testing"
    SUPPORTED = "supported"
    REJECTED = "rejected"


class Hypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str = Field(min_length=1)
    incident_id: str = Field(min_length=1)

    statement: str = Field(min_length=1)

    status: HypothesisStatus = HypothesisStatus.PROPOSED

    confidence: float = Field(ge=0.0, le=1.0)

    supporting_finding_ids: list[str] = Field(default_factory=list)
    contradicting_finding_ids: list[str] = Field(default_factory=list)

    affected_components: list[str] = Field(min_length=1)

    created_at: datetime
    evaluated_at: datetime | None = None

    metadata: dict[str, str] = Field(default_factory=dict)
