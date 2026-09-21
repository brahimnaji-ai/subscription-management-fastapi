from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.plan import Plan


class PlanRepository:
    def find_all(
        self,
        db: Session,
        limit: int,
        offset: int,
    ) -> list[Plan]:
        stmt = (
            select(Plan)
            .order_by(Plan.id)
            .limit(limit)
            .offset(offset)
        )
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
