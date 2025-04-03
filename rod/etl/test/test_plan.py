import pytest
from model_bakery import baker
from rest_framework import status

from rod.etl.models.plan import Plan
from rod.etl.models.plan import PlanFeature


@pytest.mark.django_db
class TestPlan:
    def test_if_anonymous_user_can_get_plan_list_return_200(self, api_client):
        baker.make(Plan, _quantity=3)
        response = api_client.get("/etl/plans/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_plan_detail_return_200(self, api_client):
        plan = baker.make(Plan)
        response = api_client.get(f"/etl/plans/{plan.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == plan.id

    def test_if_anonymous_user_can_get_plan_feature_list_return_200(self, api_client):
        plan = baker.make(Plan)
        baker.make(PlanFeature, plan=plan, _quantity=3)
        response = api_client.get(f"/etl/plans/{plan.id}/features/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_plan_feature_detail_return_200(self, api_client):
        plan = baker.make(Plan)
        feature = baker.make(PlanFeature, plan=plan)
        response = api_client.get(f"/etl/plan-features/{feature.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == feature.id

    def test_if_anonymous_user_can_not_create_plan_return_403(self, api_client):
        response = api_client.post("/etl/plans/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_plan_return_403(self, api_client):
        plan = baker.make(Plan)
        response = api_client.patch(f"/etl/plans/{plan.id}/update/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_plan_return_403(self, api_client):
        plan = baker.make(Plan)
        response = api_client.delete(f"/etl/plans/{plan.id}/delete/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_create_plan_feature_return_403(
        self,
        api_client,
    ):
        response = api_client.post("/etl/plans/1/features/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_plan_feature_return_403(
        self,
        api_client,
    ):
        response = api_client.patch("/etl/plan-features/1/update/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_plan_feature_return_403(
        self,
        api_client,
    ):
        response = api_client.delete("/etl/plan-features/1/delete/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_create_plan_return_403(
        self,
        api_client,
        authenticate,
    ):
        authenticate()
        response = api_client.post("/etl/plans/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_update_plan_return_403(
        self,
        api_client,
        authenticate,
    ):
        authenticate()
        response = api_client.patch("/etl/plans/1/update/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_delete_plan_return_403(
        self,
        api_client,
        authenticate,
    ):
        authenticate()
        response = api_client.delete("/etl/plans/1/delete/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_create_plan_feature_return_403(
        self,
        api_client,
        authenticate,
    ):
        authenticate()
        response = api_client.post("/etl/plans/1/features/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_update_plan_feature_return_403(
        self,
        api_client,
        authenticate,
    ):
        authenticate()
        response = api_client.patch("/etl/plan-features/1/update/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_can_not_delete_plan_feature_return_403(
        self,
        api_client,
        authenticate,
    ):
        authenticate()
        response = api_client.delete("/etl/plan-features/1/delete/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_support_agent_can_not_create_plan_return_403(
        self,
        api_client,
        make_employee_is_support_agent,
    ):
        make_employee_is_support_agent()
        response = api_client.post("/etl/plans/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_support_agent_can_not_update_plan_return_403(
        self,
        api_client,
        make_employee_is_support_agent,
    ):
        make_employee_is_support_agent()
        response = api_client.patch("/etl/plans/1/update/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_support_agent_can_not_delete_plan_return_403(
        self,
        api_client,
        make_employee_is_support_agent,
    ):
        make_employee_is_support_agent()
        response = api_client.delete("/etl/plans/1/delete/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_support_agent_can_not_create_plan_feature_return_403(
        self,
        api_client,
        make_employee_is_support_agent,
    ):
        make_employee_is_support_agent()
        response = api_client.post("/etl/plans/1/features/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_admin_can_create_plan_return_201(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        make_employee_is_product_admin()
        response = api_client.post(
            "/etl/plans/create/",
            {
                "name": "Test Plan",
                "description": "Test Description",
                "max_rows_processed": 1000000,
                "cost_per_million_rows": 100.00,
                "base_cost": 100.00,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Plan.objects.filter(name="Test Plan").exists()

    def test_if_employee_is_product_admin_can_update_plan_return_200(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        make_employee_is_product_admin()
        plan = baker.make(Plan)
        response = api_client.patch(
            f"/etl/plans/{plan.id}/update/",
            {
                "name": "Updated Plan",
                "description": "Updated Description",
                "max_rows_processed": 2000000,
                "cost_per_million_rows": 200.00,
                "base_cost": 200.00,
            },
        )
        assert response.status_code == status.HTTP_200_OK

    def test_if_employee_is_product_admin_can_delete_plan_return_204(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        make_employee_is_product_admin()
        plan = baker.make(Plan)
        response = api_client.delete(f"/etl/plans/{plan.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Plan.objects.filter(id=plan.id).exists()

    def test_if_employee_is_product_admin_can_create_plan_feature_return_201(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        make_employee_is_product_admin()
        plan = baker.make(Plan)
        response = api_client.post(
            f"/etl/plans/{plan.id}/features/create/",
            {
                "feature_name": "Test Feature",
                "feature_description": "Test Description",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert PlanFeature.objects.filter(feature_name="Test Feature").exists()

    def test_if_employee_is_product_admin_can_update_plan_feature_return_200(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        make_employee_is_product_admin()
        plan = baker.make(Plan)
        feature = baker.make(PlanFeature, plan=plan)
        response = api_client.patch(
            f"/etl/plan-features/{feature.id}/update/",
            {
                "feature_name": "Updated Feature",
                "feature_description": "Updated Description",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert PlanFeature.objects.filter(feature_name="Updated Feature").exists()

    def test_if_employee_is_product_admin_can_delete_plan_feature_return_204(
        self,
        api_client,
        make_employee_is_product_admin,
    ):
        make_employee_is_product_admin()
        plan = baker.make(Plan)
        feature = baker.make(PlanFeature, plan=plan)
        response = api_client.delete(f"/etl/plan-features/{feature.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PlanFeature.objects.filter(id=feature.id).exists()
