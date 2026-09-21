from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import BillingPeriod
from app.models.plan import Plan


class PlanRepository:
    def find_all(
        self,
        db: Session,
        limit: int,
        offset: int,
        active: bool | None = None,
        billing_period: BillingPeriod | None = None,
    ) -> list[Plan]:
        stmt = select(Plan)

        if active is not None:
            stmt = stmt.where(Plan.active == active)

        if billing_period is not None:
            stmt = stmt.where(Plan.billing_period == billing_period)

        stmt = stmt.order_by(Plan.id).limit(limit).offset(offset)

        return list(db.scalars(stmt))

    def find_by_name(self, db: Session, name: str) -> Plan | None:
        return db.scalar(select(Plan).where(Plan.name == name))

    def find_by_id(self, db: Session, plan_id: int) -> Plan | None:
        return db.get(Plan, plan_id)

    def save(self, db: Session, plan: Plan) -> Plan:
        db.add(plan)
        db.flush()
        db.refresh(plan)
        return plan
