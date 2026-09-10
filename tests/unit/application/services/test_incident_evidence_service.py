import pytest

from orinfra_sentinelops.application.services.incident_evidence_service import (
    IncidentEvidenceService,
)
from orinfra_sentinelops.domain.models.incident_evidence import IncidentEvidenceLink


class InMemoryIncidentEvidenceRepository:
    def __init__(self) -> None:
        self._links: dict[tuple[str, str], IncidentEvidenceLink] = {}

    async def save(self, link: IncidentEvidenceLink) -> IncidentEvidenceLink:
        self._links[(link.incident_id, link.evidence_id)] = link
        return link

    async def exists(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> bool:
        return (incident_id, evidence_id) in self._links

    async def list_by_incident(
        self,
        incident_id: str,
    ) -> list[IncidentEvidenceLink]:
        return [link for link in self._links.values() if link.incident_id == incident_id]

    async def delete(
        self,
        incident_id: str,
        evidence_id: str,
    ) -> None:
        self._links.pop((incident_id, evidence_id), None)


def build_link(
    incident_id: str = "INC-001",
    evidence_id: str = "EVD-001",
) -> IncidentEvidenceLink:
    return IncidentEvidenceLink(
        incident_id=incident_id,
        evidence_id=evidence_id,
        role="supporting",
        relevance_score=0.92,
    )


@pytest.mark.asyncio
async def test_link_evidence_persists_association() -> None:
    repository = InMemoryIncidentEvidenceRepository()
    service = IncidentEvidenceService(repository)
    link = build_link()

    result = await service.link_evidence(link)

    assert result == link
    assert await repository.exists("INC-001", "EVD-001") is True


@pytest.mark.asyncio
async def test_link_evidence_rejects_duplicate() -> None:
    repository = InMemoryIncidentEvidenceRepository()
    service = IncidentEvidenceService(repository)
    link = build_link()

    await service.link_evidence(link)

    with pytest.raises(ValueError, match="already linked"):
        await service.link_evidence(link)


@pytest.mark.asyncio
async def test_evidence_exists_delegates_to_repository() -> None:
    repository = InMemoryIncidentEvidenceRepository()
    service = IncidentEvidenceService(repository)

    await repository.save(build_link())

    assert await service.evidence_exists("INC-001", "EVD-001") is True
    assert await service.evidence_exists("INC-001", "EVD-999") is False


@pytest.mark.asyncio
async def test_list_evidence_returns_incident_links() -> None:
    repository = InMemoryIncidentEvidenceRepository()
    service = IncidentEvidenceService(repository)

    first = build_link("INC-001", "EVD-001")
    second = build_link("INC-001", "EVD-002")
    unrelated = build_link("INC-002", "EVD-003")

    await repository.save(first)
    await repository.save(second)
    await repository.save(unrelated)

    results = await service.list_evidence("INC-001")

    assert results == [first, second]


@pytest.mark.asyncio
async def test_unlink_evidence_removes_association() -> None:
    repository = InMemoryIncidentEvidenceRepository()
    service = IncidentEvidenceService(repository)

    await repository.save(build_link())

    await service.unlink_evidence("INC-001", "EVD-001")

    assert await service.evidence_exists("INC-001", "EVD-001") is False
