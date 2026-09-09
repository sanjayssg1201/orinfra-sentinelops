from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from orinfra_sentinelops.domain.enums.incident import (
    IncidentSeverity,
    IncidentStatus,
)


class IncidentCreateRequest(BaseModel):
    """Request payload for creating an incident."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    severity: IncidentSeverity
    affected_components: list[str] = Field(default_factory=list)
    environment: str = Field(min_length=1, max_length=100)
    service: str = Field(min_length=1, max_length=100)
    trace_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)


class IncidentResponse(BaseModel):
    """API representation of an incident."""

    model_config = ConfigDict(from_attributes=True)

    incident_id: str
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    detected_at: datetime
    resolved_at: datetime | None
    affected_components: list[str]
    environment: str
    service: str
    trace_ids: list[str]
    metadata: dict[str, object]
