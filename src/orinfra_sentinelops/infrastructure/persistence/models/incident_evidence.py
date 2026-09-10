from datetime import datetime

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from orinfra_sentinelops.infrastructure.persistence.models.base import Base
from orinfra_sentinelops.infrastructure.persistence.types import UTCDateTime


class IncidentEvidenceLinkORM(Base):
    """Persistence model for an incident-evidence association."""

    __tablename__ = "incident_evidence_links"

    incident_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("incidents.incident_id", ondelete="CASCADE"),
        primary_key=True,
    )

    evidence_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("evidence.evidence_id", ondelete="CASCADE"),
        primary_key=True,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    relevance_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    linked_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
    )
