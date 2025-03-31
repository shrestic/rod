# Create your api views here.

from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rod.core.exceptions import ApplicationError
from rod.etl.models import Customer
from rod.etl.selectors import CustomerSelector
from rod.etl.services import CustomerService


class CustomerUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        birth_date = serializers.DateField(required=False)
        image = serializers.ImageField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Customer
            fields = ["id", "phone", "address", "birth_date", "image"]

    def put(self, request, pk):
        customer = CustomerSelector().customer_get(customer_id=pk)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        customer = CustomerService().customer_update(
            data=input_serializer.validated_data,
            customer=customer,
        )
        output_serializer = self.OutputSerializer(customer)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class CustomerListApi(APIView):
    permission_classes = [IsAdminUser]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Customer
            fields = ["id", "phone", "address", "birth_date", "image"]

    def get(self, request):
        customers = CustomerSelector().customer_list()
        output_serializer = self.OutputSerializer(customers, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class CustomerDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Customer
            fields = ["id", "phone", "address", "birth_date", "image"]

    def get(self, request, pk):
        customer = CustomerSelector().customer_get(customer_id=pk)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        output_serializer = self.OutputSerializer(customer)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
