import uuid

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from rod.accounts.models.customer_model import Customer
from rod.accounts.models.employee_model import Employee

User = get_user_model()


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


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
def make_customer(db, api_client):
    def create_customer(auth: bool = True):  # noqa: FBT001, FBT002
        user = User.objects.create_user(
            username=f"fakeuser_{uuid.uuid4()}",
            email=f"fakeuser_{uuid.uuid4()}@example.com",
            password="testpass123",  # noqa: S106
        )

        if auth:
            api_client.force_authenticate(user=user)

        group, _ = Group.objects.get_or_create(name="Customer")
        user.groups.add(group)

        customer, _ = Customer.objects.get_or_create(user=user)
        return customer

    return create_customer


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
