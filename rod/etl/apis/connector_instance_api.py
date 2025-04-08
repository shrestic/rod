from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rod.accounts.selectors.customer_selector import CustomerSelector
from rod.billing.selectors.subscription_selector import SubscriptionSelector
from rod.core.exceptions import ApplicationError
from rod.core.permissions import IsCustomer
from rod.etl.models.connector_model import ConnectorInstance
from rod.etl.selectors.connector_selector import ConnectorInstanceSelector
from rod.etl.selectors.connector_selector import ConnectorSelector
from rod.etl.services.connector_service import ConnectorInstanceService


class ConnectorInstanceListApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ConnectorInstance
            fields = [
                "id",
                "connector",
                "status",
            ]

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            raise ApplicationError(
                message="Customer not found",
            )
        subscription = SubscriptionSelector().subscription_get_by_customer(
            customer_id=customer.id,
            is_active=True,
        )
        if not subscription:
            raise ApplicationError(
                message="Subscription not found",
            )
        connector_instance_list = ConnectorInstanceSelector().connector_instance_list(
            subscription=subscription,
        )
        serializer = self.OutputSerializer(connector_instance_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConnectorInstanceDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ConnectorInstance
            fields = [
                "id",
                "connector",
                "status",
                "schema_status",
                "schema_snapshot",
            ]

    def get(self, request, pk):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            raise ApplicationError(
                message="Customer not found",
            )
        subscription = SubscriptionSelector().subscription_get_by_customer(
            customer_id=customer.id,
            is_active=True,
        )
        if not subscription:
            raise ApplicationError(
                message="Subscription not found",
            )

        connector_instance = ConnectorInstanceSelector().connector_instance_get(
            connector_instance_id=pk,
            subscription=subscription,
        )
        if not connector_instance:
            raise ApplicationError(
                message="Connector instance not found",
            )
        serializer = self.OutputSerializer(connector_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConnectorInstanceCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class InputSerializer(serializers.ModelSerializer):
        connector_code = serializers.CharField()

        class Meta:
            model = ConnectorInstance
            fields = ["encrypted_config", "connector_code"]

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = CustomerSelector().customer_get(
            user_id=request.user.id,
        )
        if not customer:
            raise ApplicationError(
                message="Customer not found",
            )
        subscription = SubscriptionSelector().subscription_get_by_customer(
            customer_id=customer.id,
            is_active=True,
        )
        if not subscription:
            raise ApplicationError(
                message="Subscription not found",
            )

        connector = ConnectorSelector().connector_get_by_code(
            code=serializer.validated_data["connector_code"],
        )
        if not connector:
            raise ApplicationError(
                message="Connector not found",
            )

        connector_instance = ConnectorInstanceService().connector_instance_create(
            subscription=subscription,
            connector=connector,
            config=serializer.validated_data["encrypted_config"],
        )
        return Response(connector_instance.id, status=status.HTTP_201_CREATED)


class ConnectorInstanceUpdateConfigApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ConnectorInstance
            fields = ["encrypted_config"]

    def patch(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            raise ApplicationError(
                message="Customer not found",
            )
        subscription = SubscriptionSelector().subscription_get_by_customer(
            customer_id=customer.id,
            is_active=True,
        )
        if not subscription:
            raise ApplicationError(
                message="Subscription not found",
            )

        connector_instance = ConnectorInstanceSelector().connector_instance_get(
            connector_instance_id=pk,
            subscription=subscription,
        )
        if not connector_instance:
            raise ApplicationError(
                message="Connector instance not found",
            )

        ConnectorInstanceService().connector_instance_update_config(
            connector_instance=connector_instance,
            new_config=serializer.validated_data["encrypted_config"],
        )

        serializer = self.InputSerializer(connector_instance)
        return Response(status=status.HTTP_200_OK)


class ConnectorInstanceCheckApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ConnectorInstance
            fields = ["id"]

    def post(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            raise ApplicationError(
                message="Customer not found",
            )
        subscription = SubscriptionSelector().subscription_get_by_customer(
            customer_id=customer.id,
            is_active=True,
        )
        if not subscription:
            raise ApplicationError(
                message="Subscription not found",
            )

        connector_instance = ConnectorInstanceSelector().connector_instance_get(
            connector_instance_id=pk,
            subscription=subscription,
        )
        if not connector_instance:
            raise ApplicationError(
                message="Connector instance not found",
            )
        ConnectorInstanceService().connector_instance_check(
            connector_instance=connector_instance,
        )
        return Response(
            {
                "detail": "Check started",
                "current_status": connector_instance.status,
                "next_step": f"Poll GET /etl/connector-instances/{connector_instance.id}/ to retrieve updated status.",  # noqa: E501
            },
            status=status.HTTP_200_OK,
        )


class ConnectorInstanceDiscoverSchemaApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ConnectorInstance
            fields = ["id"]

    def post(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            raise ApplicationError(
                message="Customer not found",
            )
        subscription = SubscriptionSelector().subscription_get_by_customer(
            customer_id=customer.id,
            is_active=True,
        )
        if not subscription:
            raise ApplicationError(
                message="Subscription not found",
            )

        connector_instance = ConnectorInstanceSelector().connector_instance_get(
            connector_instance_id=pk,
            subscription=subscription,
        )
        if not connector_instance:
            raise ApplicationError(
                message="Connector instance not found",
            )
        ConnectorInstanceService().connector_instance_discover_schema(
            connector_instance=connector_instance,
        )
        return Response(
            {
                "detail": "Schema discovery started",
                "schema_status": "DISCOVERING",
                "next_step": (
                    f"Poll GET /etl/connector-instances/{connector_instance.id}/ "
                    "to check progress"
                ),
            },
            status=status.HTTP_200_OK,
        )
