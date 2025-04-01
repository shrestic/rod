from unittest.mock import patch

import pytest
from model_bakery import baker
from rest_framework import status

from rod.common.utils import make_mock_object
from rod.etl.models import Customer


@pytest.mark.django_db
class TestCustomer:
    def test_if_customer_is_created_when_user_is_created_return_201(self, user):
        assert Customer.objects.filter(user=user).exists()

    def test_if_customer_is_updated_return_200(self, authenticate, api_client):
        # Arrange: Set up the test data and mocks
        authenticate()  # Authenticate the user to make API calls

        # Create a mock customer with initial data
        mock_customer = make_mock_object(
            id=1,
            phone="0987654321",
            address="Old Address",
            birth_date="1990-01-01",
        )

        # Create a mock customer with updated data to return from customer_update
        updated_mock_customer = make_mock_object(
            id=1,
            phone="1234567890",
            address="1234567890",
            birth_date="2021-01-01",
        )

        # Mock CustomerSelector and CustomerService
        with (
            patch(
                "rod.etl.selectors.CustomerSelector.customer_get",
                return_value=mock_customer,
            ),
            patch(
                "rod.etl.services.CustomerService.customer_update",
                return_value=updated_mock_customer,
            ),
        ):
            # Prepare the data to send in the request
            update_data = {
                "phone": "1234567890",
                "address": "1234567890",
                "birth_date": "2021-01-01",
            }

            # Act: Call the API to update the customer
            response = api_client.put(
                "/etl/customers/me/update/",
                data=update_data,
                format="json",
            )

            # Assert: Verify the results
            assert response.status_code == status.HTTP_200_OK
            assert response.data["id"] == "1"
            assert response.data["phone"] == "1234567890"
            assert response.data["address"] == "1234567890"
            assert response.data["birth_date"] == "2021-01-01"

    def test_if_user_is_admin_can_get_customer_list_return_200(
        self,
        authenticate,
        api_client,
    ):
        authenticate(is_staff=True)

        response = api_client.get("/etl/customers/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_not_admin_can_get_customer_list_return_403(
        self,
        authenticate,
        api_client,
    ):
        authenticate()
        response = api_client.get("/etl/customers/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_can_get_customer_list_with_filter_return_200(
        self,
        authenticate,
        api_client,
    ):
        authenticate(is_staff=True)

        baker.make(
            "users.BaseUser",
            is_staff=False,
            first_name="Jane",
            last_name="Smith",
        )

        response = api_client.get("/etl/customers/?is_staff=False")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["user"]["first_name"] == "Jane"
        assert response.data["results"][0]["user"]["last_name"] == "Smith"
