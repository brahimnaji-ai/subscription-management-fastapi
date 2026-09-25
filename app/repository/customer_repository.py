from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    def find_all(
            self,
            db: Session,
            limit: int,
            offset: int,
    ) -> list[Customer]:
        stmt = (
            select(Customer)
            .order_by(Customer.id)
            .limit(limit)
            .offset(offset)
        )
        return list(db.scalars(stmt).all())

    def find_by_id(self, db: Session, customer_id: int) -> Customer | None:
        return db.get(Customer, customer_id)

    def find_by_email(self, db: Session, email: str) -> Customer | None:
        stmt = select(Customer).where(Customer.email == email)
        return db.scalar(stmt)



    def save(self, db: Session, customer: Customer) -> Customer:
        db.add(customer)
        db.flush()
        db.refresh(customer)
        return customer
