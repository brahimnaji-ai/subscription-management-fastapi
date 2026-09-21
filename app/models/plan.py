from decimal import Decimal
from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    billing_period: Mapped[str] = mapped_column(String(20), nullable=False)
    max_api_calls: Mapped[int] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
