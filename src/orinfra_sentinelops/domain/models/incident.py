from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from orinfra_sentinelops.domain.enums.incident import (
    IncidentSeverity,
    IncidentStatus,
)


class Incident(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incident_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.DETECTED

    detected_at: datetime
    resolved_at: datetime | None = None

    affected_components: list[str] = Field(min_length=1)

    environment: str = Field(min_length=1)
    service: str = Field(min_length=1)

    trace_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)
