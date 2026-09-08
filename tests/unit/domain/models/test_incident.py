from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from orinfra_sentinelops.domain.enums.incident import (
    IncidentSeverity,
    IncidentStatus,
)
from orinfra_sentinelops.domain.models.incident import Incident


def test_incident_uses_detected_status_by_default() -> None:
    incident = Incident(
        incident_id="INC-001",
        title="Feature pipeline regression",
        description="Fraud model performance degraded after a pipeline deployment.",
        severity=IncidentSeverity.HIGH,
        detected_at=datetime.now(UTC),
        affected_components=["feature-pipeline", "fraud-model-v3"],
        environment="production",
        service="fraud-service",
    )

    assert incident.status == IncidentStatus.DETECTED


def test_incident_rejects_empty_affected_components() -> None:
    with pytest.raises(ValidationError):
        Incident(
            incident_id="INC-001",
            title="Feature pipeline regression",
            description="Fraud model performance degraded.",
            severity=IncidentSeverity.HIGH,
            detected_at=datetime.now(UTC),
            affected_components=[],
            environment="production",
            service="fraud-service",
        )


def test_incident_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Incident(
            incident_id="INC-001",
            title="Feature pipeline regression",
            description="Fraud model performance degraded.",
            severity=IncidentSeverity.HIGH,
            detected_at=datetime.now(UTC),
            affected_components=["fraud-model-v3"],
            environment="production",
            service="fraud-service",
            unexpected_field="should fail",
        )
