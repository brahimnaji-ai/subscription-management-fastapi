"""create subscriptions table

Revision ID: f89f287147a4
Revises: 5586c022d1a0
Create Date: 2026-09-27 12:43:50.117592

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f89f287147a4"
down_revision: str | Sequence[str] | None = "5586c022d1a0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    subscription_status_enum = postgresql.ENUM(
        "TRIALING",
        "ACTIVE",
        "PAST_DUE",
        "CANCELED",
        "EXPIRED",
        name="subscription_status_enum",
    )
    subscription_status_enum.create(op.get_bind(), checkfirst=True)

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            name VARCHAR(100) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("plan_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "TRIALING",
                "ACTIVE",
                "PAST_DUE",
                "CANCELED",
                "EXPIRED",
                name="subscription_status_enum",
                create_type=False,
            ),
            nullable=False,
            server_default="ACTIVE",
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "cancel_at_period_end",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
        ),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["plans.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_subscriptions_customer_id"),
        "subscriptions",
        ["customer_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_subscriptions_plan_id"),
        "subscriptions",
        ["plan_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_subscriptions_plan_id"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_customer_id"), table_name="subscriptions")
    op.drop_table("subscriptions")
    op.execute("DROP TYPE IF EXISTS subscription_status_enum")
