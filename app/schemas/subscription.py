from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import SubscriptionStatus


class SubscriptionCreate(BaseModel):
    customer_id: int
    plan_id: int


class SubscriptionResponse(BaseModel):
    id: int
    customer_id: int
    plan_id: int
    status: SubscriptionStatus
    started_at: datetime
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlanChangeRequest(BaseModel):
    new_plan_id: int


class CancellationRequest(BaseModel):
    immediate: bool = False