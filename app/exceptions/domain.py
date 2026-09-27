class DomainException(Exception):
    pass


class PlanAlreadyExistsException(DomainException):
    def __init__(self, name: str):
        super().__init__(f"Plan '{name}' already exists")


class PlanNotFoundException(DomainException):
    def __init__(self, plan_id: int):
        super().__init__(f"Plan '{plan_id}' was not found")


class PlanInactiveException(DomainException):
    def __init__(self, plan_id: int):
        super().__init__(f"Plan '{plan_id}' is inactive")


# =========================== CUSTOMER ==================================

class CustomerNotFoundException(DomainException):
    def __init__(self, customer_id: int):
        super().__init__(f"Customer '{customer_id}' was not found")


class CustomerAlreadyExistsException(DomainException):
    def __init__(self, email: str):
        super().__init__(f"Customer '{email}' already exists")


# =========================== SUBSCRIPTION ===============================

class SubscriptionNotFoundException(DomainException):
    def __init__(self, subscription_id: int):
        super().__init__(f"Subscription '{subscription_id}' was not found")


class CustomerAlreadySubscribedException(DomainException):
    def __init__(self, customer_id: int):
        super().__init__(
            f"Customer '{customer_id}' already has an active subscription"
        )

class InvalidSubscriptionStateException(DomainException):
    def __init__(
        self,
        current_status: object,
        allowed_statuses: object = None,
    ):
        self.current_status = current_status
        self.allowed_statuses = allowed_statuses
        if isinstance(current_status, int) and allowed_statuses is None:
            super().__init__(
                f"Subscription '{current_status}' was not a valid subscription state"
            )
            return

        current_name = (
            current_status.value
            if hasattr(current_status, "value")
            else str(current_status)
        )
        if allowed_statuses:
            allowed_names = [
                s.value if hasattr(s, "value") else str(s)
                for s in allowed_statuses  # type: ignore[union-attr]
            ]
            super().__init__(
                f"Subscription status '{current_name}' is invalid for this operation. Allowed statuses: {', '.join(allowed_names)}"
            )
        else:
            super().__init__(
                f"Subscription status '{current_name}' is invalid for this operation"
            )


class SamePlanChangeException(DomainException):
    def __init__(self, plan_id: int):
        super().__init__(f"Subscription is already on plan '{plan_id}'")


SamePlanException = SamePlanChangeException
SubscriptionAlreadyOnPlanException = SamePlanChangeException

