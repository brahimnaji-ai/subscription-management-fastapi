"""add billing period enum

Revision ID: 5586c022d1a0
Revises: c8b447c63995
Create Date: 2026-09-21 19:28:28.331798

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5586c022d1a0"
down_revision: str | Sequence[str] | None = "c8b447c63995"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    billing_period_enum = postgresql.ENUM(
        "MONTHLY",
        "YEARLY",
        name="billing_period_enum",
    )

    billing_period_enum.create(op.get_bind(), checkfirst=True)

    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM plans
                WHERE UPPER(TRIM(billing_period)) NOT IN ('MONTHLY', 'YEARLY')
            ) THEN
                RAISE EXCEPTION
                    'Cannot migrate plans.billing_period: only MONTHLY and YEARLY values are supported';
            END IF;
        END $$;
        """
    )
    op.execute("UPDATE plans SET billing_period = UPPER(TRIM(billing_period))")

    op.alter_column(
        "plans",
        "billing_period",
        existing_type=sa.VARCHAR(length=20),
        type_=billing_period_enum,
        existing_nullable=False,
        postgresql_using="billing_period::billing_period_enum",
    )


def downgrade() -> None:
    op.alter_column(
        "plans",
        "billing_period",
        existing_type=postgresql.ENUM(
            "MONTHLY",
            "YEARLY",
            name="billing_period_enum",
        ),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
    )

    op.execute("DROP TYPE billing_period_enum")
