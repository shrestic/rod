from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rod.common.utils import user_in_group
from rod.core.exceptions import ApplicationError
from rod.etl.models.subscription import Subscription
from rod.etl.permissions import IsCustomer
from rod.etl.permissions import IsProductAdmin
from rod.etl.permissions import IsProductAdminOrCustomer
from rod.etl.selectors.customer import CustomerSelector
from rod.etl.selectors.plan import PlanSelector
from rod.etl.selectors.subscription import SubscriptionSelector
from rod.etl.services.subscription import SubscriptionService


class SubscriptionListAPI(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Subscription
            fields = [
                "id",
                "customer",
                "plan",
                "start_date",
                "end_date",
                "is_active",
                "billing_cycle_day",
                "billing_frequency",
            ]

    def get(self, request):
        subscriptions = SubscriptionSelector().subscription_list()
        serializer = self.OutputSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionDetailAPI(APIView):
    permission_classes = [IsAuthenticated, IsProductAdminOrCustomer]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Subscription
            fields = [
                "id",
                "customer",
                "plan",
                "start_date",
                "end_date",
                "is_active",
                "billing_cycle_day",
                "billing_frequency",
            ]

    def get(self, request, pk=None):
        if user_in_group(request.user, "Product Admin") and pk is not None:
            subscription = SubscriptionSelector().subscription_get_by_id(
                subscription_id=pk,
            )
        elif user_in_group(request.user, "Customer") and pk is None:
            customer_id = CustomerSelector().customer_get(user_id=request.user.id).id
            if customer_id is None:
                raise ApplicationError(message="Customer not found")
            subscription = SubscriptionSelector().subscription_get_by_customer(
                customer_id=customer_id,
            )
            if subscription is None:
                raise ApplicationError(message="Subscription not found")
        else:
            raise ApplicationError(message="Invalid access")
        serializer = self.OutputSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionCreateAPI(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class InputSerializer(serializers.Serializer):
        plan_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = PlanSelector().plan_get(plan_id=serializer.validated_data["plan_id"])
        if plan is None:
            raise ApplicationError(message="Plan not found")
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        if (
            SubscriptionSelector().subscription_get_by_customer(
                customer_id=customer.id,
                is_active=True,
            )
            is not None
        ):
            raise ApplicationError(
                message=(
                    "You already have an active subscription. "
                    "Please cancel the existing subscription before creating a new one."
                ),
            )
        SubscriptionService().subscription_create(
            customer=customer,
            plan=plan,
        )
        return Response(status=status.HTTP_201_CREATED)


class SubscriptionCancelAPI(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def patch(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        subscription = SubscriptionSelector().subscription_get_by_customer(
            customer_id=customer.id,
        )
        if subscription is None:
            raise ApplicationError(message="Subscription not found")
        SubscriptionService().subscription_update(
            subscription=subscription,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
