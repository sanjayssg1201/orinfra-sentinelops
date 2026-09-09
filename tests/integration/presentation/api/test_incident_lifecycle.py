from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from orinfra_sentinelops.presentation.api.app import app

client = TestClient(app)


def test_incident_complete_lifecycle() -> None:
    detected_at = datetime.now(UTC)
    resolved_at = detected_at + timedelta(minutes=5)

    create_response = client.post(
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

    assert create_response.status_code == 201
    incident = create_response.json()
    incident_id = incident["incident_id"]

    get_response = client.get(f"/incidents/{incident_id}")

    assert get_response.status_code == 200
    assert get_response.json()["incident_id"] == incident_id
    assert get_response.json()["status"] == "detected"

    investigate_response = client.post(
        f"/incidents/{incident_id}/investigate",
    )

    assert investigate_response.status_code == 200
    assert investigate_response.json()["status"] == "investigating"

    resolve_response = client.post(
        f"/incidents/{incident_id}/resolve",
        json={
            "resolved_at": resolved_at.isoformat(),
        },
    )

    assert resolve_response.status_code == 200
    assert resolve_response.json()["status"] == "resolved"

    close_response = client.post(
        f"/incidents/{incident_id}/close",
    )

    assert close_response.status_code == 200
    assert close_response.json()["status"] == "closed"

    final_response = client.get(f"/incidents/{incident_id}")

    assert final_response.status_code == 200
    assert final_response.json()["status"] == "closed"
