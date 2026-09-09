from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from orinfra_sentinelops.domain.models.evidence import Evidence


def test_evidence_accepts_valid_data() -> None:
    observed_at = datetime.now(UTC)

    evidence = Evidence(
        evidence_id="EV-001",
        source="prometheus",
        evidence_type="metric",
        observed_at=observed_at,
        component="fraud-model-v3",
        summary="Model precision dropped from 0.91 to 0.73.",
        value={"previous": 0.91, "current": 0.73},
        trace_id="trace-001",
        request_id="request-001",
        confidence=0.96,
    )

    assert evidence.evidence_id == "EV-001"
    assert evidence.source == "prometheus"
    assert evidence.evidence_type == "metric"
    assert evidence.component == "fraud-model-v3"
    assert evidence.confidence == 0.96
    assert evidence.trace_id == "trace-001"


def test_evidence_accepts_optional_fields_as_none() -> None:
    evidence = Evidence(
        evidence_id="EV-002",
        source="application-log",
        evidence_type="log",
        observed_at=datetime.now(UTC),
        component="feature-pipeline",
        summary="Feature transformation completed successfully.",
        confidence=0.82,
    )

    assert evidence.value is None
    assert evidence.trace_id is None
    assert evidence.request_id is None


def test_evidence_rejects_confidence_outside_range() -> None:
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV-003",
            source="prometheus",
            evidence_type="metric",
            observed_at=datetime.now(UTC),
            component="fraud-model-v3",
            summary="Invalid confidence value.",
            confidence=1.5,
        )


def test_evidence_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV-004",
            source="prometheus",
            evidence_type="metric",
            observed_at=datetime.now(UTC),
            component="fraud-model-v3",
            summary="Unexpected field should fail.",
            confidence=0.90,
            unexpected_field="should fail",
        )


def test_evidence_rejects_empty_required_strings() -> None:
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="",
            source="prometheus",
            evidence_type="metric",
            observed_at=datetime.now(UTC),
            component="fraud-model-v3",
            summary="Invalid evidence.",
            confidence=0.90,
        )
