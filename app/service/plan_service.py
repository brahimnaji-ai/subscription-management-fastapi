from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.domain import PlanAlreadyExistsException, PlanNotFoundException
from app.models.plan import Plan
from app.repository.plan_repository import PlanRepository
from app.schemas.plan import PlanCreate, PlanUpdate


class PlanService:
    def __init__(self):
        self.repository = PlanRepository()

    def create(self, db: Session, request: PlanCreate) -> Plan:
        if self.repository.find_by_name(db, request.name):
            raise PlanAlreadyExistsException(request.name)

        plan = Plan(**request.model_dump())
        try:
            self.repository.save(db, plan)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise PlanAlreadyExistsException(request.name) from None
        return plan

    def find_all(self, db: Session) -> list[Plan]:
        return self.repository.find_all(db)

    def find_by_id(self, db: Session, plan_id: int) -> Plan:
        plan = self.repository.find_by_id(db, plan_id)

        if plan is None:
            raise PlanNotFoundException(plan_id)

        return plan

    def update_plan(self, db: Session, plan_id: int, request: PlanUpdate) -> Plan:
        plan = self.find_by_id(db, plan_id)
        updates = request.model_dump(exclude_unset=True)

        new_name = updates.get("name")
        if new_name is not None and new_name != plan.name:
            existing_plan = self.repository.find_by_name(db, new_name)
            if existing_plan is not None:
                raise PlanAlreadyExistsException(new_name)

        for field, value in updates.items():
            setattr(plan, field, value)

        try:
            self.repository.save(db, plan)
            db.commit()
        except IntegrityError:
            db.rollback()
            if new_name is not None:
                raise PlanAlreadyExistsException(new_name) from None
            raise

        return plan

    def deactivate_plan(self, db: Session, plan_id: int) -> None:
        plan = self.find_by_id(db, plan_id)
        plan.active = False
        self.repository.save(db, plan)
        db.commit()
