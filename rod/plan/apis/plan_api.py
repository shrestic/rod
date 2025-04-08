from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rod.common.utils import inline_serializer
from rod.core.exceptions import ApplicationError
from rod.core.permissions import IsProductAdmin
from rod.plan.models.plan_model import Plan
from rod.plan.models.plan_model import PlanFeature
from rod.plan.selectors.plan_selector import PlanSelector
from rod.plan.services.plan_service import PlanFeatureService
from rod.plan.services.plan_service import PlanService


class PlanListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Plan
            fields = [
                "name",
                "code",
                "description",
                "cost",
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
                "name": serializers.CharField(),
                "description": serializers.CharField(),
            },
        )

        class Meta:
            model = Plan
            fields = [
                "name",
                "code",
                "description",
                "cost",
                "features",
            ]

    def get(self, request, code):
        plan = PlanSelector().plan_get(code=code)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        serializer = self.OutputSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        code = serializers.CharField()
        description = serializers.CharField()
        cost = serializers.FloatField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if PlanSelector().plan_get(code=serializer.validated_data["code"]):
            raise ApplicationError(message="Plan with given code already exists")
        plan = PlanService().plan_create(
            **serializer.validated_data,
        )
        return Response(plan.code, status=status.HTTP_201_CREATED)


class PlanUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        code = serializers.CharField()
        description = serializers.CharField()
        cost = serializers.FloatField()

    def patch(self, request, code):
        plan = PlanSelector().plan_get(code=code)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = PlanService().plan_update(
            plan=plan,
            data=serializer.validated_data,
        )
        return Response(plan.code, status=status.HTTP_200_OK)


class PlanDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    def delete(self, request, code):
        plan = PlanSelector().plan_get(code=code)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        PlanService().plan_delete(plan=plan)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanFeatureCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        plan_code = serializers.CharField()
        code = serializers.CharField()
        name = serializers.CharField()
        description = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_code = serializer.validated_data["plan_code"]
        code = serializer.validated_data["code"]
        name = serializer.validated_data["name"]
        description = serializer.validated_data["description"]
        plan = PlanSelector().plan_get(code=plan_code)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        plan_feature = PlanFeatureService().plan_feature_create(
            plan=plan,
            code=code,
            name=name,
            description=description,
        )
        return Response(plan_feature.code, status=status.HTTP_201_CREATED)


class PlanFeatureBulkCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        name = serializers.CharField()
        description = serializers.CharField()

    def post(self, request, code):
        if not isinstance(request.data, list):
            raise ApplicationError(
                message="Expected a list of features.",
            )

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        plan = PlanSelector().plan_get(code=code)
        if plan is None:
            raise ApplicationError(message="Plan not found")
        PlanFeatureService().plan_feature_bulk_create(
            plan=plan,
            features_data=serializer.validated_data,
        )

        return Response(status=status.HTTP_201_CREATED)


class PlanFeatureUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        code = serializers.CharField()
        description = serializers.CharField()

    def patch(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_feature = PlanSelector().plan_feature_get(id=pk)
        if plan_feature is None:
            raise ApplicationError(message="Plan feature not found")
        plan_feature = PlanFeatureService().plan_feature_update(
            plan_feature=plan_feature,
            data=serializer.validated_data,
        )
        return Response(plan_feature.code, status=status.HTTP_200_OK)


class PlanFeatureDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlanFeature
            fields = ["name", "description"]

    def get(self, request, pk):
        plan_feature = PlanSelector().plan_feature_get(id=pk)
        if plan_feature is None:
            raise ApplicationError(message="Plan feature not found")
        serializer = self.OutputSerializer(plan_feature)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanFeatureListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlanFeature
            fields = ["name", "description"]

    def get(self, request, code):
        plan = PlanSelector().plan_get(code=code)
        if plan is None:
            raise ApplicationError(message="Plan with given code not found")
        plan_features = PlanSelector().plan_features_list(plan_code=code)
        serializer = self.OutputSerializer(plan_features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanFeatureDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductAdmin]

    def delete(self, request, pk):
        plan_feature = PlanSelector().plan_feature_get(id=pk)
        if plan_feature is None:
            raise ApplicationError(message="Plan feature not found")
        PlanFeatureService().plan_feature_delete(plan_feature=plan_feature)
        return Response(status=status.HTTP_204_NO_CONTENT)
