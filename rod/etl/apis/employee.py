from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rod.core.exceptions import ApplicationError
from rod.etl.models.employee import Employee
from rod.etl.selectors.employee import EmployeeSelector
from rod.etl.services.employee import EmployeeService
from rod.users.serializers import UserSerializer

# Create your api views here.


class MeEmployeeDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.ModelSerializer):
        user = UserSerializer()

        class Meta:
            model = Employee
            fields = [
                "id",
                "phone",
                "address",
                "birth_date",
                "position",
                "department",
                "start_date",
                "user",
            ]

    def get(self, request):
        employee = EmployeeSelector().employee_get(user_id=request.user.id)

        if employee is None:
            raise ApplicationError(message="Employee not found")
        output_serializer = self.OutputSerializer(employee)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class MeEmployeeUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        birth_date = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        user = UserSerializer()

        class Meta:
            model = Employee
            fields = [
                "id",
                "phone",
                "address",
                "birth_date",
                "position",
                "department",
                "start_date",
                "user",
            ]

    def patch(self, request):
        employee = EmployeeSelector().employee_get(user_id=request.user.id)
        if employee is None:
            raise ApplicationError(message="Employee not found")
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        employee = EmployeeService().employee_update(
            data=input_serializer.validated_data,
            employee=employee,
        )
        output_serializer = self.OutputSerializer(employee)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
