from datetime import datetime

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from orinfra_sentinelops.infrastructure.persistence.models.base import Base
from orinfra_sentinelops.infrastructure.persistence.types import UTCDateTime


class IncidentORM(Base):
    """SQLAlchemy persistence model for incidents."""

    __tablename__ = "incidents"

    incident_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    detected_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        UTCDateTime(),
        nullable=True,
    )

    affected_components: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    environment: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    service: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    trace_ids: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    metadata_: Mapped[dict[str, str]] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
    )
