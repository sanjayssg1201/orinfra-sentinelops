from fastapi.testclient import TestClient

from orinfra_sentinelops.presentation.api.app import app

client = TestClient(app)


def test_create_incident_returns_created_incident() -> None:
    payload = {
        "title": "Feature pipeline regression",
        "description": "Fraud model performance degraded after a feature pipeline deployment.",
        "severity": "high",
        "affected_components": [
            "feature-pipeline",
            "fraud-model",
        ],
        "environment": "production",
        "service": "fraud-service",
        "trace_ids": [
            "trace-001",
        ],
        "metadata": {
            "scenario": "INC-001",
        },
    }

    response = client.post("/incidents", json=payload)

    assert response.status_code == 201

    body = response.json()

    assert body["incident_id"].startswith("INC-")
    assert body["title"] == payload["title"]
    assert body["description"] == payload["description"]
    assert body["severity"] == "high"
    assert body["status"] == "detected"
    assert body["affected_components"] == payload["affected_components"]
    assert body["environment"] == "production"
    assert body["service"] == "fraud-service"
    assert body["trace_ids"] == ["trace-001"]
    assert body["metadata"] == {"scenario": "INC-001"}
    assert body["detected_at"]
    assert body["resolved_at"] is None
