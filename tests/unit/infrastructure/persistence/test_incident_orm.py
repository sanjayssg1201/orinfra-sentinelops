from datetime import UTC, datetime

from sqlalchemy import inspect

from orinfra_sentinelops.infrastructure.persistence.models import (
    Base,
    IncidentORM,
)


def test_incident_orm_table_metadata() -> None:
    assert IncidentORM.__tablename__ == "incidents"

    mapper = inspect(IncidentORM)

    column_names = {column.name for column in mapper.columns}

    assert column_names == {
        "incident_id",
        "title",
        "description",
        "severity",
        "status",
        "detected_at",
        "resolved_at",
        "affected_components",
        "environment",
        "service",
        "trace_ids",
        "metadata",
    }


def test_incident_orm_primary_key() -> None:
    mapper = inspect(IncidentORM)

    primary_keys = [column.name for column in mapper.primary_key]

    assert primary_keys == ["incident_id"]


def test_incident_orm_can_be_constructed() -> None:
    incident = IncidentORM(
        incident_id="INC-001",
        title="Feature pipeline regression",
        description="Synthetic feature transformation regression.",
        severity="high",
        status="detected",
        detected_at=datetime.now(UTC),
        environment="test",
        service="fraud-service",
    )

    assert incident.incident_id == "INC-001"
    assert incident.severity == "high"
    assert incident.status == "detected"


def test_incident_orm_registered_with_base() -> None:
    assert "incidents" in Base.metadata.tables
