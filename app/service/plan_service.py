from sqlalchemy.orm import Session


from app.models.plan import Plan
from app.repository.plan_repository import PlanRepository
from app.schemas.plan import PlanCreate


class PlanService:
    def __init__(self):
        self.repository = PlanRepository()

    def create(self, db: Session, request: PlanCreate) -> Plan:
        if self.repository.find_by_name(db, request.name):
            raise ValueError(
                "Plan with name '{}' already exists".format(request.name)
            )
        plan = Plan(**request.model_dump())
        self.repository.save(db, plan)
        db.commit()
        return plan

    def find_all(self, db: Session) -> list[Plan]:
        return self.repository.find_all(db)
