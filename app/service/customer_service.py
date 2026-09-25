from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.domain import (
    CustomerAlreadyExistsException,
    CustomerNotFoundException,
)
from app.models.customer import Customer
from app.repository.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerResponse


class CustomerService:

    def __init__(self):
        self.repository = CustomerRepository()

    def create(
            self,
            db: Session,
            request: CustomerCreate,
    ) -> CustomerResponse:

        if self.repository.find_by_email(db, request.email):
            raise CustomerAlreadyExistsException(request.email)

        customer = Customer(**request.model_dump())

        try:
            self.repository.save(db, customer)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise CustomerAlreadyExistsException(request.email) from None

        return CustomerResponse.model_validate(customer)

    def find_by_id(
            self,
            db: Session,
            customer_id: int,
    ) -> CustomerResponse:

        customer = self.repository.find_by_id(db, customer_id)

        if customer is None:
            raise CustomerNotFoundException(customer_id)

        return CustomerResponse.model_validate(customer)

    def find_all(
            self,
            db: Session,
            limit: int,
            offset: int,
    ) -> list[CustomerResponse]:

        customers = self.repository.find_all(db, limit, offset)

        return [
            CustomerResponse.model_validate(customer)
            for customer in customers
        ]