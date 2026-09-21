from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.enums import BillingPeriod
from app.schemas.plan import PlanCreate, PlanResponse, PlanUpdate
from app.service.plan_service import PlanService

router = APIRouter(prefix="/plans")

service = PlanService()


@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create(
    request: PlanCreate,
    db: Session = Depends(get_db),
)-> PlanResponse:
    plan = service.create(db, request)
    return PlanResponse.model_validate(plan)


@router.get("", response_model=list[PlanResponse])
def get_all(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[
        int,
        Query(ge=0, le=9_223_372_036_854_775_807),
    ] = 0,
    active: bool | None = Query(default=None),
    billing_period: BillingPeriod | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[PlanResponse]:
    plans = service.find_all(db, limit, offset, active, billing_period)
    return [PlanResponse.model_validate(plan) for plan in plans]


@router.get("/{plan_id}", response_model=PlanResponse)
def find_by_id(
    plan_id: int,
    db: Session = Depends(get_db),
) -> PlanResponse:
    plan = service.find_by_id(db, plan_id)
    return PlanResponse.model_validate(plan)


@router.patch("/{plan_id}", response_model=PlanResponse)
def update_plan(
    plan_id: int,
    request: PlanUpdate,
    db: Session = Depends(get_db),
) -> PlanResponse:
    plan = service.update_plan(db, plan_id, request)
    return PlanResponse.model_validate(plan)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_plan(
    plan_id: int,
    db: Session = Depends(get_db),
) -> None:
    service.deactivate_plan(db, plan_id)
