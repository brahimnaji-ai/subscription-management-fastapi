from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.plan import Plan


class PlanRepository:
    def find_all(self, db: Session) -> list[Plan]:
        return list(db.scalars(select(Plan).order_by(Plan.id)))

    def find_by_name(self, db: Session, name: str) -> Plan | None:
        return db.scalar(select(Plan).where(Plan.name == name))

    def save(self, db: Session, plan: Plan) -> Plan:
        db.add(plan)
        db.flush()
        db.refresh(plan)
        return plan
