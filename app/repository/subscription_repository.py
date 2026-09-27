from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import SubscriptionStatus
from app.models.subscription import Subscription


class SubscriptionRepository:
    def find_by_id(self, db: Session, subscription_id: int) -> Subscription | None:
        return db.get(Subscription, subscription_id)

    def find_active_by_customer(
        self,
        db: Session,
        customer_id: int,
    ) -> Subscription | None:
        stmt = (
            select(Subscription)
            .where(
                Subscription.customer_id == customer_id,
                Subscription.status.in_(
                    [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]
                ),
            )
            .order_by(Subscription.id.desc())
        )
        return db.scalar(stmt)

    def save(self, db: Session, subscription: Subscription) -> Subscription:
        db.add(subscription)
        db.flush()
        db.refresh(subscription)
        return subscription
