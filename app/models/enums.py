from enum import StrEnum


class BillingPeriod(StrEnum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

class SubscriptionStatus(StrEnum):
    """Subscription lifecycle states and transitions.

    Valid transitions:
        TRIALING -> ACTIVE | CANCELED | EXPIRED
        ACTIVE   -> PAST_DUE | CANCELED | EXPIRED
        PAST_DUE -> ACTIVE | CANCELED | EXPIRED
        CANCELED -> (terminal)
        EXPIRED  -> (terminal)
    """

    TRIALING = "TRIALING"
    ACTIVE = "ACTIVE"
    PAST_DUE = "PAST_DUE"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"

