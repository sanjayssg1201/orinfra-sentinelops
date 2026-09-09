"""create evidence table

Revision ID: a2cf06d485ad
Revises: 070d819fa14c
Create Date: 2026-09-09 16:30:28.064441

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from orinfra_sentinelops.infrastructure.persistence.types import UTCDateTime

# revision identifiers, used by Alembic.
revision: str = "a2cf06d485ad"
down_revision: str | Sequence[str] | None = "070d819fa14c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "evidence",
        sa.Column("evidence_id", sa.String(length=100), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("evidence_type", sa.String(length=100), nullable=False),
        sa.Column("observed_at", UTCDateTime(), nullable=False),
        sa.Column("component", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("trace_id", sa.String(length=255), nullable=True),
        sa.Column("request_id", sa.String(length=255), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("evidence_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("evidence")
