from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    finding_id: str = Field(min_length=1)
    investigator: str = Field(min_length=1)

    summary: str = Field(min_length=1)
    component: str = Field(min_length=1)

    observed_at: datetime

    confidence: float = Field(ge=0.0, le=1.0)

    evidence_ids: list[str] = Field(min_length=1)

    severity: str = Field(min_length=1)
    finding_type: str = Field(min_length=1)

    metadata: dict[str, str] = Field(default_factory=dict)
