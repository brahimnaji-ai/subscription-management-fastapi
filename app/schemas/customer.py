from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
