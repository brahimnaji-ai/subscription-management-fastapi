from datetime import UTC, datetime, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.domain import (
    CustomerAlreadySubscribedException,
    InvalidSubscriptionStateException,
    PlanInactiveException,
    SamePlanChangeException,
    SubscriptionNotFoundException,
)
from app.models.enums import BillingPeriod, SubscriptionStatus
from app.models.subscription import Subscription
from app.repository.subscription_repository import SubscriptionRepository
from app.schemas.subscription import (
    CancellationRequest,
    PlanChangeRequest,
    SubscriptionCreate,
)
from app.service.customer_service import CustomerService
from app.service.plan_service import PlanService


class SubscriptionService:
    def __init__(
        self,
        repository: SubscriptionRepository | None = None,
        customer_service: CustomerService | None = None,
        plan_service: PlanService | None = None,
    ):
        self.repository = repository or SubscriptionRepository()
        self.customer_service = customer_service or CustomerService()
        self.plan_service = plan_service or PlanService()

    def subscribe(self, db: Session, request: SubscriptionCreate) -> Subscription:
        # 1. Verify customer exists
        self.customer_service.find_by_id(db, request.customer_id)

        # 2. Verify plan exists and is active
        plan = self.plan_service.find_by_id(db, request.plan_id)
        if not plan.active:
            raise PlanInactiveException(request.plan_id)

        # 3. Reject if customer already has an active or trialing subscription
        existing_sub = self.repository.find_active_by_customer(db, request.customer_id)
        if existing_sub is not None:
            raise CustomerAlreadySubscribedException(request.customer_id)

        # 4. Compute period dates from billing period
        now = datetime.now(UTC)
        period_days = 30 if plan.billing_period == BillingPeriod.MONTHLY else 365

        if plan.trial_days > 0:
            status = SubscriptionStatus.TRIALING
            current_period_start = now + timedelta(days=plan.trial_days)
            current_period_end = current_period_start + timedelta(days=period_days)
        else:
            status = SubscriptionStatus.ACTIVE
            current_period_start = now
            current_period_end = current_period_start + timedelta(days=period_days)

        subscription = Subscription(
            customer_id=request.customer_id,
            plan_id=request.plan_id,
            status=status,
            started_at=now,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
            cancel_at_period_end=False,
        )

        try:
            self.repository.save(db, subscription)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        return subscription

    def find_by_id(self, db: Session, subscription_id: int) -> Subscription:
        subscription = self.repository.find_by_id(db, subscription_id)
        if subscription is None:
            raise SubscriptionNotFoundException(subscription_id)
        return subscription

    def change_plan(
        self,
        db: Session,
        subscription_id: int,
        request: PlanChangeRequest,
    ) -> Subscription:
        # 1. Fetch the subscription; raise SubscriptionNotFoundException if missing
        subscription = self.find_by_id(db, subscription_id)

        # 2. Assert status is ACTIVE or TRIALING; raise InvalidSubscriptionStateException otherwise
        allowed_statuses = [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]
        if subscription.status not in allowed_statuses:
            raise InvalidSubscriptionStateException(
                subscription.status, allowed_statuses
            )

        # 3. Fetch and validate the new plan
        new_plan = self.plan_service.find_by_id(db, request.new_plan_id)
        if not new_plan.active:
            raise PlanInactiveException(request.new_plan_id)

        # 4. Guard against same-plan change
        if subscription.plan_id == request.new_plan_id:
            raise SamePlanChangeException(request.new_plan_id)

        # 5. Update plan_id, reset period dates, persist
        now = datetime.now(UTC)
        period_days = 30 if new_plan.billing_period == BillingPeriod.MONTHLY else 365
        current_period_start = now
        current_period_end = current_period_start + timedelta(days=period_days)

        subscription.plan_id = new_plan.id
        subscription.plan = new_plan
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.cancel_at_period_end = False
        subscription.current_period_start = current_period_start
        subscription.current_period_end = current_period_end

        try:
            self.repository.save(db, subscription)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        return subscription

    def cancel(
        self,
        db: Session,
        subscription_id: int,
        request: CancellationRequest,
    ) -> Subscription:
        # 1. Fetch the subscription; raise SubscriptionNotFoundException if missing
        subscription = self.find_by_id(db, subscription_id)

        # 2. Assert status is ACTIVE or TRIALING; raise InvalidSubscriptionStateException if already canceled or expired
        allowed_statuses = [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]
        if subscription.status not in allowed_statuses:
            raise InvalidSubscriptionStateException(
                subscription.status, allowed_statuses
            )

        # 3. If immediate=True: set status = CANCELED
        if request.immediate:
            subscription.status = SubscriptionStatus.CANCELED
        else:
            # 4. If immediate=False: set cancel_at_period_end = True (status remains ACTIVE)
            subscription.cancel_at_period_end = True

        # 5. Persist and return
        try:
            self.repository.save(db, subscription)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        return subscription

