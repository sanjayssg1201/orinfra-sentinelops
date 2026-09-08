from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    evidence_type: str = Field(min_length=1)
    observed_at: datetime
    component: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    value: Any | None = None
    trace_id: str | None = None
    request_id: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
