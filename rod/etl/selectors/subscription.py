import uuid

from django.db.models import QuerySet

from rod.common.utils import get_object
from rod.etl.models.subscription import Subscription


class SubscriptionSelector:
    def __init__(self) -> None:
        pass

    def subscription_list(self) -> QuerySet[Subscription]:
        return Subscription.objects.all()

    def subscription_get_by_id(self, *, subscription_id: int) -> Subscription:
        return get_object(Subscription, id=subscription_id)

    def subscription_get_by_customer(
        self,
        *,
        customer_id: uuid.UUID,
        is_active: bool = True,
    ) -> Subscription:
        return get_object(
            Subscription,
            customer_id=customer_id,
            is_active=is_active,
        )
