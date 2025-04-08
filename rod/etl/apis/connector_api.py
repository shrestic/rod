from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rod.core.exceptions import ApplicationError
from rod.core.permissions import IsETLTeam
from rod.etl.models.connector_model import Connector
from rod.etl.selectors.connector_selector import ConnectorSelector
from rod.etl.services.connector_service import ConnectorService


class ConnectorListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Connector
            fields = "__all__"

    def get(self, request):
        connector_list = ConnectorSelector().connector_list()
        serializer = self.OutputSerializer(connector_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConnectorDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Connector
            fields = "__all__"

    def get(self, request, code):
        connector = ConnectorSelector().connector_get(code=code)
        serializer = self.OutputSerializer(connector)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConnectorCreateApi(APIView):
    permission_classes = [IsETLTeam]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Connector
            fields = "__all__"

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ConnectorService().connector_create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class ConnectorUpdateApi(APIView):
    permission_classes = [IsETLTeam]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Connector
            fields = [
                "label",
                "input_type",
                "config_form",
            ]

    def patch(self, request, code):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        connector = ConnectorSelector().connector_get(code=code)
        if connector is None:
            return ApplicationError(
                message="Connector not found",
            )
        ConnectorService().connector_update(
            connector=connector,
            data=serializer.validated_data,
        )
        return Response(status=status.HTTP_200_OK)


class ConnectorDeleteApi(APIView):
    permission_classes = [IsETLTeam]

    def delete(self, request, code):
        connector = ConnectorSelector().connector_get(code=code)
        if connector is None:
            return ApplicationError(
                message="Connector not found",
            )
        ConnectorService().connector_delete(connector=connector)
        return Response(status=status.HTTP_204_NO_CONTENT)
