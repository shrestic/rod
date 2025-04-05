import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from rod.plan.models import Plan


@pytest.mark.django_db
class TestSubscription:
    def test_if_user_is_customer_can_create_subscription_return_201(
        self,
        make_customer_user,
        api_client,
    ):
        # Arrange
        make_customer_user()
        plan = baker.make(Plan)
        url = reverse("subscriptions:create")
        data = {"plan_id": plan.id}

        # Act
        response = api_client.post(url, data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_is_customer_can_get_subscription_detail_return_200(
        self,
        make_subscription,
        api_client,
    ):
        # Arrange
        make_subscription(auth=True)
        url = reverse("subscriptions:me")

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_customer_can_cancel_subscription_return_204(
        self,
        make_subscription,
        api_client,
    ):
        # Arrange
        make_subscription(auth=True)
        url = reverse("subscriptions:cancel")

        # Act
        response = api_client.patch(url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_product_admin_can_get_subscription_detail_return_200(
        self,
        make_employee_is_product_admin,
        make_subscription,
        api_client,
    ):
        # Arrange
        make_employee_is_product_admin()
        subscription = make_subscription(auth=False)
        url = reverse("subscriptions:detail", args=[subscription.id])

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_product_admin_can_list_subscription_return_200(
        self,
        make_employee_is_product_admin,
        make_subscription,
        api_client,
    ):
        # Arrange
        make_employee_is_product_admin()
        subscriptions = [make_subscription(auth=False) for _ in range(3)]
        url = reverse("subscriptions:list")

        # Act
        response = api_client.get(url)
        response_ids = {item["id"] for item in response.data}
        expected_ids = {str(sub.id) for sub in subscriptions}

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response_ids == expected_ids

    def test_if_user_is_not_customer_can_not_create_subscription_return_403(
        self,
        api_client,
    ):
        # Arrange
        url = reverse("subscriptions:create")

        # Act
        response = api_client.post(url, format="json")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
