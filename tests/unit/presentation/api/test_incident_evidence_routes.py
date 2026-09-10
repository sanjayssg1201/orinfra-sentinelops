from fastapi.testclient import TestClient

from orinfra_sentinelops.presentation.api.app import app

client = TestClient(app)


def create_incident(
    title: str = "Test incident",
    severity: str = "high",
    environment: str = "test",
) -> str:
    response = client.post(
        "/incidents",
        json={
            "title": title,
            "description": "Incident created for API testing.",
            "severity": severity,
            "environment": environment,
            "service": "test-service",
            "affected_components": ["test-service"],
            "trace_ids": [],
            "metadata": {},
        },
    )

    assert response.status_code == 201
    return response.json()["incident_id"]


def create_evidence() -> str:
    response = client.post(
        "/evidence",
        json={
            "source": "test",
            "evidence_type": "metric",
            "observed_at": "2026-09-10T10:00:00Z",
            "component": "test-service",
            "summary": "Latency increased during the incident.",
            "value": {"latency_ms": 850},
            "trace_id": "trace-test-001",
            "request_id": "request-test-001",
            "confidence": 0.95,
        },
    )

    assert response.status_code == 201
    return response.json()["evidence_id"]


def test_link_and_list_incident_evidence() -> None:
    incident_id = create_incident(
        title="Evidence linking incident",
        severity="high",
        environment="production",
    )
    evidence_id = create_evidence()

    response = client.post(
        f"/incidents/{incident_id}/evidence",
        json={
            "evidence_id": evidence_id,
            "role": "root-cause",
            "relevance_score": 0.95,
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["incident_id"] == incident_id
    assert body["evidence_id"] == evidence_id
    assert body["role"] == "root-cause"
    assert body["relevance_score"] == 0.95
    assert "linked_at" in body

    response = client.get(f"/incidents/{incident_id}/evidence")

    assert response.status_code == 200

    body = response.json()
    assert len(body) == 1
    assert body[0]["incident_id"] == incident_id
    assert body[0]["evidence_id"] == evidence_id


def test_duplicate_incident_evidence_link_returns_conflict() -> None:
    incident_id = create_incident(
        title="Duplicate link incident",
        severity="medium",
        environment="test",
    )
    evidence_id = create_evidence()

    payload = {
        "evidence_id": evidence_id,
        "role": "supporting",
        "relevance_score": 0.80,
    }

    response = client.post(
        f"/incidents/{incident_id}/evidence",
        json=payload,
    )

    assert response.status_code == 201

    response = client.post(
        f"/incidents/{incident_id}/evidence",
        json=payload,
    )

    assert response.status_code == 409
    assert "already linked" in response.json()["detail"]


def test_unlink_incident_evidence() -> None:
    incident_id = create_incident(
        title="Unlink evidence incident",
        severity="low",
        environment="test",
    )
    evidence_id = create_evidence()

    response = client.post(
        f"/incidents/{incident_id}/evidence",
        json={
            "evidence_id": evidence_id,
            "role": "supporting",
            "relevance_score": 0.75,
        },
    )

    assert response.status_code == 201

    response = client.delete(
        f"/incidents/{incident_id}/evidence/{evidence_id}",
    )

    assert response.status_code == 204

    response = client.get(
        f"/incidents/{incident_id}/evidence",
    )

    assert response.status_code == 200
    assert response.json() == []
