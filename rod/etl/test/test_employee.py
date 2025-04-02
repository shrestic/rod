from unittest.mock import patch

import pytest
from rest_framework import status

from rod.common.utils import make_mock_object
from rod.etl.models import Employee


@pytest.mark.django_db
class TestEmployee:
    def test_anonymous_user_cannot_create_employee(self, api_client):
        response = api_client.post(
            "/auth/users/",
            {
                "username": "staff",
                "email": "staff@example.com",
                "first_name": "Staff",
                "last_name": "User",
                "password": "testpass123",
                "re_password": "testpass123",
                "is_staff": True,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Only superusers can create staff users." in str(response.data)

    def test_normal_user_cannot_create_employee(self, authenticate, api_client):
        authenticate(is_superuser=False)
        response = api_client.post(
            "/auth/users/",
            {
                "username": "staff",
                "email": "staff@example.com",
                "first_name": "Staff",
                "last_name": "User",
                "password": "testpass123",
                "re_password": "testpass123",
                "is_staff": True,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Only superusers can create staff users." in str(response.data)

    def test_superuser_can_create_employee(self, authenticate, api_client):
        authenticate(is_superuser=True)
        response = api_client.post(
            "/auth/users/",
            {
                "username": "staff",
                "email": "staff@example.com",
                "first_name": "Staff",
                "last_name": "User",
                "password": "testpass123",
                "re_password": "testpass123",
                "is_staff": True,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Employee.objects.filter(user__username="staff").exists()

    def test_if_employee_can_get_own_profile_return_200(
        self,
        authenticate,
        api_client,
    ):
        authenticate()

        mock_user = make_mock_object(
            id="123e4567-e89b-12d3-a456-426614174005",
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
        )

        mock_employee = make_mock_object(
            id="123e4567-e89b-12d3-a456-426614174006",
            phone="0987654321",
            address="Old Address",
            birth_date="1990-01-01",
            user=mock_user,
        )

        with patch(
            "rod.etl.selectors.EmployeeSelector.employee_get",
            return_value=mock_employee,
        ):
            response = api_client.get("/etl/employees/me/")
            assert response.status_code == status.HTTP_200_OK

    def test_if_employee_can_edit_own_profile_return_200(
        self,
        authenticate,
        api_client,
    ):
        authenticate()

        mock_user = make_mock_object(
            id="123e4567-e89b-12d3-a456-426614174007",
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
        )

        mock_employee = make_mock_object(
            id="123e4567-e89b-12d3-a456-426614174007",
            phone="0987654321",
            address="Old Address",
            birth_date="1990-01-01",
            position="Manager",
            department="Sales",
            start_date="2021-01-01",
            user=mock_user,
        )

        updated_mock_employee = make_mock_object(
            id="123e4567-e89b-12d3-a456-426614174007",
            phone="1234567890",
            address="1234567890",
            birth_date="2021-01-01",
            position="Manager",
            department="Sales",
            start_date="2021-01-01",
            user=mock_user,
        )

        with (
            patch(
                "rod.etl.selectors.EmployeeSelector.employee_get",
                return_value=mock_employee,
            ),
            patch(
                "rod.etl.services.EmployeeService.employee_update",
                return_value=updated_mock_employee,
            ),
        ):
            update_data = {
                "phone": "1234567890",
                "address": "1234567890",
                "birth_date": "2021-01-01",
            }
            response = api_client.put(
                "/etl/employees/me/update/",
                data=update_data,
                format="json",
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.data["id"] == "123e4567-e89b-12d3-a456-426614174007"
            assert response.data["phone"] == "1234567890"
            assert response.data["address"] == "1234567890"
            assert response.data["birth_date"] == "2021-01-01"
