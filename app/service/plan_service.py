from sqlalchemy.orm import Session

from app.exceptions.domain import PlanAlreadyExistsException, PlanNotFoundException
from app.models.plan import Plan
from app.repository.plan_repository import PlanRepository
from app.schemas.plan import PlanCreate

class PlanService:
    def __init__(self):
        self.repository = PlanRepository()

    def create(self, db: Session, request: PlanCreate) -> Plan:
        if self.repository.find_by_name(db, request.name):
            raise PlanAlreadyExistsException(request.name)

        plan = Plan(**request.model_dump())
        self.repository.save(db, plan)
        db.commit()
        return plan

    def find_all(self, db: Session) -> list[Plan]:
        return self.repository.find_all(db)

    def find_by_id(self, db: Session, plan_id: int) -> Plan:
        plan = self.repository.find_by_id(db, plan_id)

        if plan is None:
            raise PlanNotFoundException(plan_id)

        return plan
