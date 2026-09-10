from datetime import UTC, datetime

from fastapi.testclient import TestClient

from orinfra_sentinelops.presentation.api.app import app

client = TestClient(app)


def test_create_evidence_returns_created_evidence() -> None:
    observed_at = datetime.now(UTC)

    response = client.post(
        "/evidence",
        json={
            "source": "model-monitor",
            "evidence_type": "metric",
            "observed_at": observed_at.isoformat(),
            "component": "fraud-model",
            "summary": "Precision dropped significantly.",
            "value": {
                "precision": 0.71,
                "baseline": 0.87,
            },
            "trace_id": "trace-001",
            "request_id": "request-001",
            "confidence": 0.94,
        },
    )

    assert response.status_code == 201

    evidence = response.json()

    assert evidence["evidence_id"].startswith("EVD-")
    assert evidence["source"] == "model-monitor"
    assert evidence["evidence_type"] == "metric"
    assert evidence["component"] == "fraud-model"
    assert evidence["summary"] == "Precision dropped significantly."
    assert evidence["value"]["precision"] == 0.71
    assert evidence["trace_id"] == "trace-001"
    assert evidence["request_id"] == "request-001"
    assert evidence["confidence"] == 0.94


def test_get_evidence_returns_evidence() -> None:
    response = client.post(
        "/evidence",
        json={
            "source": "model-monitor",
            "evidence_type": "metric",
            "observed_at": datetime.now(UTC).isoformat(),
            "component": "fraud-model",
            "summary": "Recall dropped.",
            "value": {
                "recall": 0.68,
            },
            "confidence": 0.91,
        },
    )

    assert response.status_code == 201

    evidence_id = response.json()["evidence_id"]

    get_response = client.get(f"/evidence/{evidence_id}")

    assert get_response.status_code == 200
    assert get_response.json()["evidence_id"] == evidence_id
    assert get_response.json()["summary"] == "Recall dropped."


def test_get_unknown_evidence_returns_not_found() -> None:
    response = client.get("/evidence/EVD-MISSING")

    assert response.status_code == 404
    assert response.json()["detail"] == "Evidence 'EVD-MISSING' not found."


def test_delete_evidence_returns_no_content() -> None:
    response = client.post(
        "/evidence",
        json={
            "source": "telemetry",
            "evidence_type": "latency",
            "observed_at": datetime.now(UTC).isoformat(),
            "component": "fraud-service",
            "summary": "Latency increased.",
            "value": {
                "p95_ms": 850,
            },
            "confidence": 0.89,
        },
    )

    assert response.status_code == 201

    evidence_id = response.json()["evidence_id"]

    delete_response = client.delete(f"/evidence/{evidence_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/evidence/{evidence_id}")

    assert get_response.status_code == 404


def test_delete_unknown_evidence_returns_not_found() -> None:
    response = client.delete("/evidence/EVD-MISSING")

    assert response.status_code == 404
    assert response.json()["detail"] == "Evidence 'EVD-MISSING' not found."
