import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):  # noqa: FBT002
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return do_authenticate


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")  # noqa: S106
