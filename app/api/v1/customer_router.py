from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.service.customer_service import CustomerService

router = APIRouter(prefix="/customers")

service = CustomerService()


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
        request: CustomerCreate,
        db: Session = Depends(get_db),
) -> CustomerResponse:
    return service.create(db, request)


@router.get("", response_model=list[CustomerResponse])
def get_all(
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
        db: Session = Depends(get_db),
) -> list[CustomerResponse]:
    return service.find_all(db, limit, offset)


@router.get("/{customer_id}", response_model=CustomerResponse)
def find_by_id(
        customer_id: int,
        db: Session = Depends(get_db),
) -> CustomerResponse:
    return service.find_by_id(db, customer_id)