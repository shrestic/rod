import pytest
from rest_framework import status

from rod.etl.models import Customer


@pytest.mark.django_db
class TestCustomer:
    def test_if_customer_is_created_when_user_is_created_return_201(self, user):
        assert Customer.objects.filter(user=user).exists()

    def test_if_customer_is_updated_return_200(self, authenticate, api_client, user):
        authenticate()
        customer = Customer.objects.create(user=user)
        response = api_client.put(
            f"/etl/customers/{customer.id}/update/",
            {
                "phone": "1234567890",
                "address": "1234567890",
                "birth_date": "2021-01-01",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["phone"] == "1234567890"
        assert response.data["address"] == "1234567890"
        assert response.data["birth_date"] == "2021-01-01"
