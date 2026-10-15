"""Extend the schema created by the PostgreSQL initialisation scripts.
Revision ID: 0001_community_review
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_community_review"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(length=80), nullable=True))
    op.execute("""
        UPDATE users
        SET name = COALESCE(
            NULLIF(LEFT(SPLIT_PART(TRIM(email), '@', 1), 80), ''),
            'User'
        )
        WHERE name IS NULL
    """)
    op.alter_column(
        "users", "name", existing_type=sa.String(length=80), nullable=False
    )

    op.execute("ALTER TABLE accidents ALTER COLUMN status DROP DEFAULT")
    op.execute(
        "ALTER TYPE public.accident_status RENAME TO accident_status_initial"
    )
    op.execute("""
        CREATE TYPE public.accident_status AS ENUM
        ('pending', 'approved', 'rejected', 'resolved')
    """)
    op.execute("""
        ALTER TABLE accidents
        ALTER COLUMN status TYPE public.accident_status
        USING (
            CASE WHEN status::text = 'in_progress' THEN 'approved'
                 ELSE status::text
            END
        )::public.accident_status
    """)
    op.execute("""
        UPDATE accidents SET status = 'pending'
        WHERE status IS NULL
    """)
    op.execute(
        "ALTER TABLE accidents ALTER COLUMN status SET NOT NULL"
    )
    op.execute("""
        ALTER TABLE accidents ALTER COLUMN status
        SET DEFAULT 'pending'::public.accident_status
    """)
    op.execute("DROP TYPE public.accident_status_initial")

    op.add_column(
        "accidents",
        sa.Column("category", sa.String(length=32), nullable=False,
                  server_default="other"),
    )
    op.add_column(
        "accidents",
        sa.Column("severity", sa.String(length=16), nullable=False,
                  server_default="medium"),
    )
    op.add_column(
        "accidents",
        sa.Column("verification_source", sa.String(length=16), nullable=True),
    )
    op.add_column(
        "accidents",
        sa.Column("reviewed_by", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "accidents",
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "accidents",
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "accidents",
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "accidents_reviewed_by_fk", "accidents", "users", ["reviewed_by"], ["user_id"]
    )
    op.create_check_constraint(
        "valid_incident_category", "accidents",
        "category IN ('accident', 'road_work', 'road_closure', "
        "'pothole', 'traffic_light', 'other')",
    )
    op.create_check_constraint(
        "valid_incident_severity", "accidents",
        "severity IN ('low', 'medium', 'high')",
    )
    op.create_check_constraint(
        "valid_verification_source", "accidents",
        "verification_source IS NULL OR "
        "verification_source IN ('admin', 'community')",
    )
    op.create_index("accidents_status_idx", "accidents", ["status"])
    op.execute("""
        CREATE INDEX accident_geography_idx
        ON accidents USING gist ((location::geography))
    """)

    op.create_table(
        "incident_confirmations",
        sa.Column("confirmation_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "accident_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accidents.accident_id"), nullable=False,
        ),
        sa.Column(
            "user_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.user_id"), nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            nullable=False, server_default=sa.func.now(),
        ),
        sa.UniqueConstraint(
            "accident_id", "user_id", name="one_confirmation_per_user"
        ),
    )
    op.create_table(
        "notification_events",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "accident_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accidents.accident_id"), nullable=False,
        ),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            nullable=False, server_default=sa.func.now(),
        ),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("notification_events")
    op.drop_table("incident_confirmations")
    op.execute("DROP INDEX accident_geography_idx")
    op.drop_index("accidents_status_idx", table_name="accidents")
    for constraint in (
        "valid_verification_source",
        "valid_incident_severity",
        "valid_incident_category",
    ):
        op.drop_constraint(constraint, "accidents", type_="check")
    op.drop_constraint(
        "accidents_reviewed_by_fk", "accidents", type_="foreignkey"
    )
    for column in (
        "ends_at", "starts_at", "reviewed_at", "reviewed_by",
        "verification_source", "severity", "category",
    ):
        op.drop_column("accidents", column)

    op.execute("ALTER TABLE accidents ALTER COLUMN status DROP DEFAULT")
    op.execute("ALTER TYPE public.accident_status RENAME TO accident_status_final")
    op.execute("""
        CREATE TYPE public.accident_status AS ENUM
        ('pending', 'in_progress', 'resolved')
    """)
    op.execute("""
        ALTER TABLE accidents
        ALTER COLUMN status TYPE public.accident_status
        USING (
            CASE WHEN status::text = 'approved' THEN 'in_progress'
                 WHEN status::text = 'rejected' THEN 'pending'
                 ELSE status::text
            END
        )::public.accident_status
    """)
    op.execute("""
        ALTER TABLE accidents ALTER COLUMN status
        SET DEFAULT 'pending'::public.accident_status
    """)
    op.execute("DROP TYPE public.accident_status_final")
    op.alter_column(
        "accidents", "status", existing_type=postgresql.ENUM(
            "pending", "in_progress", "resolved", name="accident_status",
            create_type=False,
        ), nullable=True,
    )
    op.drop_column("users", "name")
