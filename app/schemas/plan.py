from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class PlanCreate(BaseModel):
    name: str = Field(length=1, max_length=100)
    price: Decimal = Field(ge=0)
    billing_period: str
    max_api_calls: int = Field(gt=0)


class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    active: bool
