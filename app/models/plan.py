from decimal import Decimal
from sqlalchemy import Boolean, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import BillingPeriod


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    billing_period: Mapped[BillingPeriod] = mapped_column(
        Enum(
            BillingPeriod,
            name="billing_period_enum",
            values_callable=lambda enum_type: [member.value for member in enum_type],
        ),
        nullable=False,
    )
    max_api_calls: Mapped[int] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
