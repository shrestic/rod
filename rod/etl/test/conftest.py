import uuid

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from model_bakery import baker
from rest_framework.test import APIClient

from rod.etl.models.customer import Customer
from rod.etl.models.employee import Employee
from rod.etl.models.plan import Plan
from rod.etl.models.subscription import Subscription

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False, is_superuser=False):  # noqa: FBT002
        user = User(
            username=f"fakeuser_{uuid.uuid4()}",
            email=f"fakeuser_{uuid.uuid4()}@example.com",
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        api_client.force_authenticate(user=user)
        return user

    return do_authenticate


@pytest.fixture
def make_employee_is_support_agent(db, authenticate):
    def create_employee():
        user = authenticate(is_staff=True)
        user.save()

        group, _ = Group.objects.get_or_create(name="Support Agent")
        user.groups.add(group)

        if not hasattr(user, "employee"):
            Employee.objects.create(user=user)

    return create_employee


@pytest.fixture
def make_employee_is_product_admin(db, authenticate):
    def create_employee():
        user = authenticate(is_staff=True)
        user.save()

        group, _ = Group.objects.get_or_create(name="Product Admin")
        user.groups.add(group)

        if not hasattr(user, "employee"):
            Employee.objects.create(user=user)

    return create_employee


@pytest.fixture
def make_customer_user(db, api_client):
    def create_customer(auth: bool = True):  # noqa: FBT001, FBT002
        user = User.objects.create_user(
            username=f"fakeuser_{uuid.uuid4()}",
            email=f"fakeuser_{uuid.uuid4()}@example.com",
            is_staff=False,
            is_superuser=False,
        )

        if auth:
            api_client.force_authenticate(user=user)

        group, _ = Group.objects.get_or_create(name="Customer")
        user.groups.add(group)

        customer, _ = Customer.objects.get_or_create(user=user)
        return customer

    return create_customer


@pytest.fixture
def make_subscription(db, make_customer_user):
    def create_subscription(auth: bool = True):  # noqa: FBT001, FBT002
        customer = make_customer_user(auth=auth)
        plan = baker.make(Plan)
        subscription = baker.make(Subscription, customer=customer, plan=plan)
        subscription.save()
        return subscription

    return create_subscription
