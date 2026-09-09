from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from orinfra_sentinelops.domain.models.remediation import (
    Remediation,
    RemediationRisk,
    RemediationStatus,
)


def test_remediation_accepts_valid_data() -> None:
    remediation = Remediation(
        remediation_id="REM-001",
        incident_id="INC-001",
        action="Rollback feature pipeline to version 1.0.",
        description="Restore the last known-good feature transformation.",
        risk=RemediationRisk.MEDIUM,
        affected_components=["feature-pipeline", "fraud-model-v3"],
        supporting_hypothesis_ids=["HYP-001"],
        supporting_evidence_ids=["EV-001", "EV-002"],
        created_at=datetime.now(UTC),
    )

    assert remediation.remediation_id == "REM-001"
    assert remediation.incident_id == "INC-001"
    assert remediation.status == RemediationStatus.PROPOSED
    assert remediation.requires_approval is True
    assert remediation.risk == RemediationRisk.MEDIUM
    assert len(remediation.supporting_evidence_ids) == 2


def test_remediation_rejects_empty_affected_components() -> None:
    with pytest.raises(ValidationError):
        Remediation(
            remediation_id="REM-001",
            incident_id="INC-001",
            action="Rollback feature pipeline.",
            description="Restore the last known-good version.",
            risk=RemediationRisk.MEDIUM,
            affected_components=[],
            created_at=datetime.now(UTC),
        )


def test_remediation_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Remediation(
            remediation_id="REM-001",
            incident_id="INC-001",
            action="Rollback feature pipeline.",
            description="Restore the last known-good version.",
            risk=RemediationRisk.MEDIUM,
            affected_components=["feature-pipeline"],
            created_at=datetime.now(UTC),
            unexpected_field="should fail",
        )


def test_remediation_supports_approval_metadata() -> None:
    approved_at = datetime.now(UTC)

    remediation = Remediation(
        remediation_id="REM-001",
        incident_id="INC-001",
        action="Rollback feature pipeline.",
        description="Restore the last known-good version.",
        risk=RemediationRisk.MEDIUM,
        affected_components=["feature-pipeline"],
        status=RemediationStatus.APPROVED,
        approved_by="operator-001",
        approved_at=approved_at,
        created_at=datetime.now(UTC),
    )

    assert remediation.status == RemediationStatus.APPROVED
    assert remediation.approved_by == "operator-001"
    assert remediation.approved_at == approved_at
