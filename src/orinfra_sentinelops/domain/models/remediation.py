from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class RemediationStatus(StrEnum):
    PROPOSED = "proposed"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class RemediationRisk(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Remediation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    remediation_id: str = Field(min_length=1)
    incident_id: str = Field(min_length=1)

    action: str = Field(min_length=1)
    description: str = Field(min_length=1)

    status: RemediationStatus = RemediationStatus.PROPOSED
    risk: RemediationRisk

    affected_components: list[str] = Field(min_length=1)

    supporting_hypothesis_ids: list[str] = Field(default_factory=list)
    supporting_evidence_ids: list[str] = Field(default_factory=list)

    requires_approval: bool = True
    approved_by: str | None = None
    approved_at: datetime | None = None

    created_at: datetime
    executed_at: datetime | None = None

    execution_result: str | None = None

    metadata: dict[str, str] = Field(default_factory=dict)
