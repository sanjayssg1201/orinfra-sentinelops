from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from orinfra_sentinelops.domain.models.incident_evidence import (
    IncidentEvidenceLink,
)


def build_link() -> IncidentEvidenceLink:
    return IncidentEvidenceLink(
        incident_id="INC-001",
        evidence_id="EVD-001",
        role="supporting",
        relevance_score=0.94,
        linked_at=datetime.now(UTC),
    )


def test_creates_valid_link() -> None:
    link = build_link()

    assert link.incident_id == "INC-001"
    assert link.evidence_id == "EVD-001"
    assert link.role == "supporting"
    assert link.relevance_score == 0.94


@pytest.mark.parametrize("score", [-0.01, 1.01])
def test_rejects_invalid_relevance_score(score: float) -> None:
    with pytest.raises(ValidationError):
        IncidentEvidenceLink(
            incident_id="INC-001",
            evidence_id="EVD-001",
            role="supporting",
            relevance_score=score,
        )


def test_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        IncidentEvidenceLink(
            incident_id="INC-001",
            evidence_id="EVD-001",
            role="supporting",
            relevance_score=0.94,
            unexpected="value",
        )


def test_generates_linked_at_when_not_provided() -> None:
    link = IncidentEvidenceLink(
        incident_id="INC-001",
        evidence_id="EVD-001",
        role="trigger",
        relevance_score=0.90,
    )

    assert link.linked_at.tzinfo is not None
