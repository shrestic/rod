import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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
