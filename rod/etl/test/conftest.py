import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
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
def employee_with_customer_permission(db, authenticate):
    def make_employee_user():
        user = authenticate(is_staff=True)
        user.save()

        group, _ = Group.objects.get_or_create(name="Customer Support")
        user.groups.add(group)

        permission = Permission.objects.get(codename="view_customer")
        group.permissions.add(permission)

        if not hasattr(user, "employee"):
            Employee.objects.create(user=user)

        return user

    return make_employee_user
