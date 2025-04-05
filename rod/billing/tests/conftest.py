import pytest
from model_bakery import baker

from rod.billing.models.subscription_model import Subscription
from rod.plan.models.plan_model import Plan


@pytest.fixture
def make_subscription(db, make_customer):
    def create_subscription(auth: bool = True):  # noqa: FBT001, FBT002
        customer = make_customer(auth=auth)
        plan = baker.make(Plan)
        subscription = baker.make(Subscription, customer=customer, plan=plan)
        subscription.save()
        return subscription

    return create_subscription
