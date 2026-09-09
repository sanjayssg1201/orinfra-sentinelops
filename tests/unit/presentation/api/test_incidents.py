from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from orinfra_sentinelops.presentation.api.app import app

client = TestClient(app)


def test_create_incident_returns_created_incident() -> None:
    response = client.post(
        "/incidents",
        json={
            "title": "Feature pipeline regression",
            "description": "Fraud model performance degraded after a pipeline change.",
            "severity": "high",
            "affected_components": [
                "feature-pipeline",
                "fraud-model",
            ],
            "environment": "production",
            "service": "fraud-service",
            "trace_ids": ["trace-001"],
            "metadata": {
                "scenario": "INC-001",
            },
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["incident_id"].startswith("INC-")
    assert body["title"] == "Feature pipeline regression"
    assert body["description"] == (
        "Fraud model performance degraded after a pipeline change."
    )
    assert body["severity"] == "high"
    assert body["status"] == "detected"
    assert body["affected_components"] == [
        "feature-pipeline",
        "fraud-model",
    ]
    assert body["environment"] == "production"
    assert body["service"] == "fraud-service"
    assert body["trace_ids"] == ["trace-001"]
    assert body["metadata"] == {"scenario": "INC-001"}
    assert body["detected_at"] is not None
    assert body["resolved_at"] is None


def test_get_incident_returns_incident() -> None:
    create_response = client.post(
        "/incidents",
        json={
            "title": "Get incident test",
            "description": "Testing incident retrieval.",
            "severity": "medium",
            "affected_components": ["test-service"],
            "environment": "test",
            "service": "test-service",
        },
    )

    assert create_response.status_code == 201

    incident_id = create_response.json()["incident_id"]

    response = client.get(f"/incidents/{incident_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["incident_id"] == incident_id
    assert body["title"] == "Get incident test"
    assert body["description"] == "Testing incident retrieval."
    assert body["severity"] == "medium"
    assert body["status"] == "detected"
    assert body["environment"] == "test"
    assert body["service"] == "test-service"


def test_get_unknown_incident_returns_not_found() -> None:
    response = client.get("/incidents/INC-NOT-FOUND")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Incident 'INC-NOT-FOUND' not found.",
    }


def test_start_investigation_returns_investigating_incident() -> None:
    create_response = client.post(
        "/incidents",
        json={
            "title": "Investigation test",
            "description": "Testing incident investigation.",
            "severity": "high",
            "affected_components": ["test-service"],
            "environment": "test",
            "service": "test-service",
        },
    )

    assert create_response.status_code == 201

    incident_id = create_response.json()["incident_id"]

    response = client.post(
        f"/incidents/{incident_id}/investigate",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["incident_id"] == incident_id
    assert body["status"] == "investigating"


def test_resolve_incident_returns_resolved_incident() -> None:
    response = client.post(
        "/incidents",
        json={
            "title": "Resolution test",
            "description": "Testing incident resolution.",
            "severity": "high",
            "affected_components": ["test-service"],
            "environment": "test",
            "service": "test-service",
        },
    )

    assert response.status_code == 201

    incident = response.json()
    incident_id = incident["incident_id"]

    detected_at = datetime.fromisoformat(
        incident["detected_at"].replace("Z", "+00:00")
    )
    resolved_at = detected_at + timedelta(minutes=5)

    response = client.post(
        f"/incidents/{incident_id}/investigate",
    )

    assert response.status_code == 200

    response = client.post(
        f"/incidents/{incident_id}/resolve",
        json={
            "resolved_at": resolved_at.isoformat(),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["incident_id"] == incident_id
    assert body["status"] == "resolved"
    assert body["resolved_at"] is not None

    actual_resolved_at = datetime.fromisoformat(
        body["resolved_at"].replace("Z", "+00:00")
    )

    assert actual_resolved_at == resolved_at


def test_close_incident_returns_closed_incident() -> None:
    response = client.post(
        "/incidents",
        json={
            "title": "Close incident test",
            "description": "Testing incident closure.",
            "severity": "medium",
            "affected_components": ["test-service"],
            "environment": "test",
            "service": "test-service",
        },
    )

    assert response.status_code == 201

    incident = response.json()
    incident_id = incident["incident_id"]

    detected_at = datetime.fromisoformat(
        incident["detected_at"].replace("Z", "+00:00")
    )
    resolved_at = detected_at + timedelta(minutes=5)

    response = client.post(
        f"/incidents/{incident_id}/investigate",
    )

    assert response.status_code == 200

    response = client.post(
        f"/incidents/{incident_id}/resolve",
        json={
            "resolved_at": resolved_at.isoformat(),
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "resolved"

    response = client.post(
        f"/incidents/{incident_id}/close",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["incident_id"] == incident_id
    assert body["status"] == "closed"
    assert body["resolved_at"] is not None