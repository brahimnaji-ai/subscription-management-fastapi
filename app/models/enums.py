from enum import StrEnum


class BillingPeriod(StrEnum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

class SubscriptionStatus(StrEnum):
    TRIALING = "TRIALING"
    ACTIVE = "ACTIVE"
    PAST_DUE = "PAST_DUE"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
