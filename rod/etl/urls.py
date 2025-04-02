from django.urls import include
from django.urls import path

from rod.etl.apis.customer import AdminCustomerDetailApi
from rod.etl.apis.customer import AdminCustomerListApi
from rod.etl.apis.customer import MeCustomerDetailApi
from rod.etl.apis.customer import MeCustomerUpdateApi
from rod.etl.apis.employee import MeEmployeeDetailApi
from rod.etl.apis.employee import MeEmployeeUpdateApi

customer_patterns = [
    path("", AdminCustomerListApi.as_view(), name="list"),
    path("<uuid:pk>/", AdminCustomerDetailApi.as_view(), name="detail"),
    path("me/", MeCustomerDetailApi.as_view(), name="me"),
    path("me/update/", MeCustomerUpdateApi.as_view(), name="update"),
]

employee_patterns = [
    path("me/", MeEmployeeDetailApi.as_view(), name="me"),
    path("me/update/", MeEmployeeUpdateApi.as_view(), name="update"),
]

urlpatterns = [
    path("customers/", include((customer_patterns, "customers"))),
    path("employees/", include((employee_patterns, "employees"))),
]
