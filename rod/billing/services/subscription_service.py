from django.utils import timezone

from rod.accounts.models.customer_model import Customer
from rod.billing.models.subscription_model import Subscription
from rod.common.services import model_update
from rod.plan.models.plan_model import Plan


class SubscriptionService:
    def __init__(self) -> None:
        pass

    def subscription_create(
        self,
        *,
        customer: Customer,
        plan: Plan,
    ) -> Subscription:
        subscription = Subscription(
            customer=customer,
            plan=plan,
            start_date=timezone.now().date(),
            end_date=None,
            is_active=True,
            billing_cycle_day=timezone.now().day,
            billing_frequency="monthly",
        )
        subscription.full_clean()
        subscription.save()
        return subscription

    def subscription_update(
        self,
        *,
        subscription: Subscription,
    ) -> Subscription:
        subscription, has_updated = model_update(
            instance=subscription,
            fields=["is_active", "end_date"],
            data={
                "is_active": False,
                "end_date": timezone.now().date(),
            },
        )
        return subscription
