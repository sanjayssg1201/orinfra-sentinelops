from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from orinfra_sentinelops.domain.models.hypothesis import (
    Hypothesis,
    HypothesisStatus,
)


def test_hypothesis_accepts_valid_data() -> None:
    hypothesis = Hypothesis(
        hypothesis_id="HYP-001",
        incident_id="INC-001",
        statement="Feature pipeline regression caused fraud model degradation.",
        confidence=0.87,
        supporting_finding_ids=["FND-001", "FND-002"],
        contradicting_finding_ids=["FND-003"],
        affected_components=["feature-pipeline", "fraud-model-v3"],
        created_at=datetime.now(UTC),
    )

    assert hypothesis.hypothesis_id == "HYP-001"
    assert hypothesis.incident_id == "INC-001"
    assert hypothesis.status == HypothesisStatus.PROPOSED
    assert hypothesis.confidence == 0.87
    assert len(hypothesis.supporting_finding_ids) == 2


def test_hypothesis_rejects_confidence_outside_range() -> None:
    with pytest.raises(ValidationError):
        Hypothesis(
            hypothesis_id="HYP-001",
            incident_id="INC-001",
            statement="Feature pipeline regression caused degradation.",
            confidence=1.2,
            affected_components=["feature-pipeline"],
            created_at=datetime.now(UTC),
        )


def test_hypothesis_rejects_empty_affected_components() -> None:
    with pytest.raises(ValidationError):
        Hypothesis(
            hypothesis_id="HYP-001",
            incident_id="INC-001",
            statement="Feature pipeline regression caused degradation.",
            confidence=0.87,
            affected_components=[],
            created_at=datetime.now(UTC),
        )


def test_hypothesis_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Hypothesis(
            hypothesis_id="HYP-001",
            incident_id="INC-001",
            statement="Feature pipeline regression caused degradation.",
            confidence=0.87,
            affected_components=["feature-pipeline"],
            created_at=datetime.now(UTC),
            unexpected_field="should fail",
        )
