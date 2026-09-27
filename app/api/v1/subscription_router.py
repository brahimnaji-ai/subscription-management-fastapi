from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.subscription import (
    PlanChangeRequest,
    SubscriptionCreate,
    SubscriptionResponse,
)
from app.service.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscriptions")
service = SubscriptionService()


@router.post(
    "",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def subscribe(
    request: SubscriptionCreate,
    db: Annotated[Session, Depends(get_db)],
) -> SubscriptionResponse:
    subscription = service.subscribe(db, request)
    return SubscriptionResponse.model_validate(subscription)


@router.get(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
)
def find_by_id(
    subscription_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> SubscriptionResponse:
    subscription = service.find_by_id(db, subscription_id)
    return SubscriptionResponse.model_validate(subscription)


@router.put(
    "/{id}/plan",
    response_model=SubscriptionResponse,
)
def change_plan(
    id: int,
    request: PlanChangeRequest,
    db: Annotated[Session, Depends(get_db)],
) -> SubscriptionResponse:
    subscription = service.change_plan(db, id, request)
    return SubscriptionResponse.model_validate(subscription)

