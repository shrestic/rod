from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rod.common.utils import inline_serializer
from rod.core.exceptions import ApplicationError
from rod.etl.models.plan import Plan
from rod.etl.models.plan import PlanFeature
from rod.etl.permissions import IsProductAdmin
from rod.etl.selectors.plan import PlanSelector
from rod.etl.services.plan import PlanFeatureService
from rod.etl.services.plan import PlanService


class PlanListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Plan
            fields = [
                "id",
                "name",
                "description",
                "max_rows_processed",
                "cost_per_million_rows",
                "base_cost",
            ]

    def get(self, request):
        plans = PlanSelector().plan_list()
        serializer = self.OutputSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        features = inline_serializer(
            many=True,
            fields={
                "id": serializers.UUIDField(),
                "feature_name": serializers.CharField(),
                "feature_description": serializers.CharField(),
            },
        )

        class Meta:
            model = Plan
            fields = [
                "id",
                "name",
                "description",
                "max_rows_processed",
                "cost_per_million_rows",
                "base_cost",
                "features",
            ]

    def get(self, request, pk):
        plan = PlanSelector().plan_get(plan_id=pk)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        serializer = self.OutputSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        max_rows_processed = serializers.IntegerField()
        cost_per_million_rows = serializers.FloatField()
        base_cost = serializers.FloatField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = PlanService().plan_create(
            **serializer.validated_data,
        )
        return Response(plan.id, status=status.HTTP_201_CREATED)


class PlanUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        max_rows_processed = serializers.IntegerField()
        cost_per_million_rows = serializers.FloatField()
        base_cost = serializers.FloatField()

    def put(self, request, pk):
        plan = PlanSelector().plan_get(plan_id=pk)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = PlanService().plan_update(
            plan=plan,
            data=serializer.validated_data,
        )
        return Response(plan.id, status=status.HTTP_200_OK)


class PlanDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    def delete(self, request, pk):
        plan = PlanSelector().plan_get(plan_id=pk)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        PlanService().plan_delete(plan=plan)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanFeatureCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        feature_name = serializers.CharField()
        feature_description = serializers.CharField()

    def post(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = PlanSelector().plan_get(plan_id=pk)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        plan_feature = PlanFeatureService().plan_feature_create(
            plan=plan,
            **serializer.validated_data,
        )
        return Response(plan_feature.id, status=status.HTTP_201_CREATED)


class PlanFeatureUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        feature_name = serializers.CharField()
        feature_description = serializers.CharField()

    def put(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_feature = PlanSelector().plan_feature_get(feature_id=pk)
        if plan_feature is None:
            raise ApplicationError(message="Plan feature not found")
        plan_feature = PlanFeatureService().plan_feature_update(
            plan_feature=plan_feature,
            data=serializer.validated_data,
        )
        return Response(plan_feature.id, status=status.HTTP_200_OK)


class PlanFeatureDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlanFeature
            fields = ["id", "feature_name", "feature_description"]

    def get(self, request, pk):
        plan_feature = PlanSelector().plan_feature_get(feature_id=pk)
        if plan_feature is None:
            raise ApplicationError(message="Plan feature not found")
        serializer = self.OutputSerializer(plan_feature)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanFeatureListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlanFeature
            fields = ["id", "feature_name", "feature_description"]

    def get(self, request, pk):
        plan_features = PlanSelector().plan_features_list(plan_id=pk)
        serializer = self.OutputSerializer(plan_features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanFeatureDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    def delete(self, request, pk):
        plan_feature = PlanSelector().plan_feature_get(feature_id=pk)
        if plan_feature is None:
            raise ApplicationError(message="Plan feature not found")
        PlanFeatureService().plan_feature_delete(plan_feature=plan_feature)
        return Response(status=status.HTTP_204_NO_CONTENT)
