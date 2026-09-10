from datetime import UTC, datetime

import pytest

from orinfra_sentinelops.application.services.evidence_service import EvidenceService
from orinfra_sentinelops.domain.models.evidence import Evidence


class InMemoryEvidenceRepository:
    """In-memory repository used to test EvidenceService."""

    def __init__(self) -> None:
        self._evidence: dict[str, Evidence] = {}

    async def save(self, evidence: Evidence) -> Evidence:
        self._evidence[evidence.evidence_id] = evidence
        return evidence

    async def get_by_id(self, evidence_id: str) -> Evidence | None:
        return self._evidence.get(evidence_id)

    async def delete(self, evidence_id: str) -> None:
        self._evidence.pop(evidence_id, None)


def build_evidence(evidence_id: str = "EVD-001") -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        source="model-monitor",
        evidence_type="metric",
        observed_at=datetime.now(UTC),
        component="fraud-model",
        summary="Precision dropped significantly.",
        value={"precision": 0.71},
        trace_id="trace-001",
        request_id="request-001",
        confidence=0.94,
    )


@pytest.mark.asyncio
async def test_create_evidence_persists_and_returns_evidence() -> None:
    repository = InMemoryEvidenceRepository()
    service = EvidenceService(repository)

    evidence = build_evidence()

    result = await service.create_evidence(evidence)

    assert result == evidence
    assert repository._evidence[evidence.evidence_id] == evidence


@pytest.mark.asyncio
async def test_get_evidence_returns_existing_evidence() -> None:
    repository = InMemoryEvidenceRepository()
    service = EvidenceService(repository)

    evidence = build_evidence()
    await repository.save(evidence)

    result = await service.get_evidence(evidence.evidence_id)

    assert result == evidence


@pytest.mark.asyncio
async def test_get_missing_evidence_raises_value_error() -> None:
    repository = InMemoryEvidenceRepository()
    service = EvidenceService(repository)

    with pytest.raises(
        ValueError,
        match="Evidence not found: EVD-MISSING",
    ):
        await service.get_evidence("EVD-MISSING")


@pytest.mark.asyncio
async def test_delete_evidence_removes_evidence() -> None:
    repository = InMemoryEvidenceRepository()
    service = EvidenceService(repository)

    evidence = build_evidence()
    await repository.save(evidence)

    await service.delete_evidence(evidence.evidence_id)

    assert evidence.evidence_id not in repository._evidence


@pytest.mark.asyncio
async def test_delete_missing_evidence_is_noop() -> None:
    repository = InMemoryEvidenceRepository()
    service = EvidenceService(repository)

    await service.delete_evidence("EVD-MISSING")
