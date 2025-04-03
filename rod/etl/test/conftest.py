import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from rod.etl.models.employee import Employee

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False, is_superuser=False):  # noqa: FBT002
        user = User(
            username="fakeadmin",
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
        user.save()
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
        user.save()

        if not hasattr(user, "employee"):
            Employee.objects.create(user=user)

    return create_employee
