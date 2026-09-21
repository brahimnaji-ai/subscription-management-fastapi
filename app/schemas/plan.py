from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class PlanCreate(BaseModel):
    name: str = Field(length=1, max_length=100)
    price: Decimal = Field(ge=0)
    billing_period: str
    max_api_calls: int = Field(gt=0)


class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    active: bool


class PlanUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: Decimal | None = Field(default=None, ge=0)
    billing_period: str | None = None
    max_api_calls: int | None = Field(default=None, gt=0)
    active: bool | None = None

    @field_validator("*", mode="before")
    @classmethod
    def reject_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("Field cannot be null")
        return value
