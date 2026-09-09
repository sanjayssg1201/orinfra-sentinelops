from datetime import datetime

from sqlalchemy import Float, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column

from orinfra_sentinelops.infrastructure.persistence.models.base import Base
from orinfra_sentinelops.infrastructure.persistence.types import UTCDateTime


class EvidenceORM(Base):
    """SQLAlchemy persistence model for investigation evidence."""

    __tablename__ = "evidence"

    evidence_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )
    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    evidence_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    observed_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
    )
    component: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    value: Mapped[object] = mapped_column(
        JSON,
        nullable=False,
    )
    trace_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    request_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
