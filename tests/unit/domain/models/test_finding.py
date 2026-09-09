from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from orinfra_sentinelops.domain.models.finding import Finding


def test_finding_accepts_valid_data() -> None:
    finding = Finding(
        finding_id="FND-001",
        investigator="model-investigator",
        summary="Model precision dropped after feature pipeline deployment.",
        component="fraud-model-v3",
        observed_at=datetime.now(UTC),
        confidence=0.94,
        evidence_ids=["metric-18291", "prediction-8821", "deployment-91"],
        severity="high",
        finding_type="model_degradation",
    )

    assert finding.finding_id == "FND-001"
    assert finding.investigator == "model-investigator"
    assert finding.confidence == 0.94
    assert len(finding.evidence_ids) == 3


def test_finding_rejects_confidence_outside_range() -> None:
    with pytest.raises(ValidationError):
        Finding(
            finding_id="FND-001",
            investigator="model-investigator",
            summary="Model degradation detected.",
            component="fraud-model-v3",
            observed_at=datetime.now(UTC),
            confidence=1.5,
            evidence_ids=["metric-18291"],
            severity="high",
            finding_type="model_degradation",
        )


def test_finding_rejects_empty_evidence_ids() -> None:
    with pytest.raises(ValidationError):
        Finding(
            finding_id="FND-001",
            investigator="model-investigator",
            summary="Model degradation detected.",
            component="fraud-model-v3",
            observed_at=datetime.now(UTC),
            confidence=0.94,
            evidence_ids=[],
            severity="high",
            finding_type="model_degradation",
        )


def test_finding_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Finding(
            finding_id="FND-001",
            investigator="model-investigator",
            summary="Model degradation detected.",
            component="fraud-model-v3",
            observed_at=datetime.now(UTC),
            confidence=0.94,
            evidence_ids=["metric-18291"],
            severity="high",
            finding_type="model_degradation",
            unexpected_field="should fail",
        )
