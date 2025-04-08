import pytest
from model_bakery import baker
from rest_framework import status

from rod.plan.models.plan_model import Plan
from rod.plan.models.plan_model import PlanFeature


@pytest.mark.django_db
class TestPlan:
    def test_if_anonymous_user_can_get_plan_list_return_200(self, api_client):
        # Arrange
        baker.make(Plan, _quantity=3)

        # Act
        response = api_client.get("/plan/plans/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_plan_detail_return_200(self, api_client):
        # Arrange
        plan = baker.make(Plan)

        # Act
        response = api_client.get(f"/plan/plans/{plan.code}/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == plan.code

    def test_if_anonymous_user_can_get_plan_feature_list_return_200(self, api_client):
        # Arrange
        plan = baker.make(Plan)
        baker.make(PlanFeature, plan=plan, _quantity=3)

        # Act
        response = api_client.get(f"/plan/plans/{plan.code}/features/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_plan_feature_detail_return_200(self, api_client):
        # Arrange
        plan = baker.make(Plan)
        feature = baker.make(PlanFeature, plan=plan)

        # Act
        response = api_client.get(f"/plan/plan-features/{feature.id}/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == feature.name
        assert response.data["description"] == feature.description

    def test_if_anonymous_user_can_not_create_plan_return_403(self, api_client):
        # Act
        response = api_client.post("/plan/plans/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_plan_return_403(self, api_client):
        # Arrange
        plan = baker.make(Plan)

        # Act
        response = api_client.patch(f"/plan/plans/{plan.code}/update/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_plan_return_403(self, api_client):
        # Arrange
        plan = baker.make(Plan)

        # Act
        response = api_client.delete(f"/plan/plans/{plan.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_create_plan_feature_return_403(self, api_client):
        # Act
        response = api_client.post("/plan/plan-features/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_plan_feature_return_403(self, api_client):
        # Act
        response = api_client.patch("/plan/plan-features/1/update/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_plan_feature_return_403(self, api_client):
        # Act
        response = api_client.delete("/plan/plan-features/1/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_create_plan_return_403(
        self,
        api_client,
        authenticate,
    ):
        # Arrange
        authenticate()

        # Act
        response = api_client.post("/plan/plans/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_update_plan_return_403(
        self,
        api_client,
        authenticate,
    ):
        # Arrange
        authenticate()

        # Act
        response = api_client.patch("/plan/plans/1/update/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_delete_plan_return_403(
        self,
        api_client,
        authenticate,
    ):
        # Arrange
        authenticate()

        # Act
        response = api_client.delete("/plan/plans/1/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_create_plan_feature_return_403(
        self,
        api_client,
        authenticate,
    ):
        # Arrange
        authenticate()

        # Act
        response = api_client.post("/plan/plan-features/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_update_plan_feature_return_403(
        self,
        api_client,
        authenticate,
    ):
        # Arrange
        authenticate()

        # Act
        response = api_client.patch("/plan/plan-features/1/update/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_delete_plan_feature_return_403(
        self,
        api_client,
        authenticate,
    ):
        # Arrange
        authenticate()

        # Act
        response = api_client.delete("/plan/plan-features/1/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_support_agent_can_not_create_plan_return_403(
        self,
        api_client,
        make_employee_is_support_agent,
    ):
        # Arrange
        make_employee_is_support_agent()

        # Act
        response = api_client.post("/plan/plans/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_support_agent_can_not_update_plan_return_403(
        self,
        api_client,
        make_employee_is_support_agent,
    ):
        # Arrange
        make_employee_is_support_agent()

        # Act
        response = api_client.patch("/plan/plans/1/update/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_support_agent_can_not_delete_plan_return_403(
        self,
        api_client,
        make_employee_is_support_agent,
    ):
        # Arrange
        make_employee_is_support_agent()

        # Act
        response = api_client.delete("/plan/plans/1/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_support_agent_can_not_create_plan_feature_return_403(
        self,
        api_client,
        make_employee_is_support_agent,
    ):
        # Arrange
        make_employee_is_support_agent()

        # Act
        response = api_client.post("/plan/plan-features/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_admin_can_delete_plan_return_204(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        # Arrange
        make_employee_is_product_admin()
        plan = baker.make(Plan)

        # Act
        response = api_client.delete(f"/plan/plans/{plan.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_employee_is_product_admin_can_create_plan_feature_return_201(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        # Arrange
        make_employee_is_product_admin()
        plan = baker.make(Plan)

        feature_data = {
            "plan_code": plan.code,
            "code": "feature-001",
            "name": "Test Feature",
            "description": "This is a test feature.",
        }

        # Act
        response = api_client.post(
            "/plan/plan-features/create/",
            data=feature_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert PlanFeature.objects.filter(name="Test Feature").exists()

    def test_if_employee_is_product_admin_can_bulk_create_plan_feature_return_201(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        # Arrange
        make_employee_is_product_admin()
        plan = baker.make(Plan)
        data = [
            {
                "name": "Unlimited Connectors",
                "description": "No connector limits",
                "code": "advanced__no-connector-limits",
            },
            {
                "name": "Unlimited Blocks",
                "description": "No transformation limits",
                "code": "advanced__no-transformation-limits",
            },
            {
                "name": "Scheduler & Support",
                "description": "Priority scheduling and help",
                "code": "advanced__priority-scheduling-and-help",
            },
        ]

        # Act
        response = api_client.post(
            f"/plan/plans/{plan.code}/features/bulk-create/",
            data=data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert PlanFeature.objects.filter(name="Scheduler & Support").exists()
        assert PlanFeature.objects.filter(name="Unlimited Blocks").exists()

    def test_if_employee_is_product_admin_can_update_plan_feature_return_200(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        # Arrange
        make_employee_is_product_admin()
        plan = baker.make(Plan)
        feature = baker.make(PlanFeature, plan=plan)
        data = {
            "name": "Connector Limit",
            "description": "Up to 2 connectors",
            "code": "free__up-to-2-connectors",
        }

        # Act
        response = api_client.patch(f"/plan/plan-features/{feature.id}/update/", data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert PlanFeature.objects.filter(name="Connector Limit").exists()

    def test_if_employee_is_product_admin_can_delete_plan_feature_return_204(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        # Arrange
        make_employee_is_product_admin()
        plan = baker.make(Plan)
        feature = baker.make(PlanFeature, plan=plan)

        # Act
        response = api_client.delete(f"/plan/plan-features/{feature.id}/delete/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PlanFeature.objects.filter(id=feature.id).exists()
