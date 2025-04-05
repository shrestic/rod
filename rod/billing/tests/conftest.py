import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

from rod.billing.models.subscription_model import Subscription
from rod.plan.models.plan_model import Plan

User = get_user_model()


@pytest.fixture
def make_subscription(db, make_customer_user):
    def create_subscription(auth: bool = True):  # noqa: FBT001, FBT002
        customer = make_customer_user(auth=auth)
        plan = baker.make(Plan)
        subscription = baker.make(Subscription, customer=customer, plan=plan)
        subscription.save()
        return subscription

    return create_subscription
