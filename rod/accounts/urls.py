from django.urls import include
from django.urls import path

from rod.accounts.apis.customer_api import AdminCustomerDetailApi
from rod.accounts.apis.customer_api import AdminCustomerListApi
from rod.accounts.apis.customer_api import MeCustomerDetailApi
from rod.accounts.apis.customer_api import MeCustomerUpdateApi
from rod.accounts.apis.employee_api import MeEmployeeDetailApi
from rod.accounts.apis.employee_api import MeEmployeeUpdateApi

# Customer
customer_patterns = [
    path("", AdminCustomerListApi.as_view(), name="list"),
    path("<uuid:pk>/", AdminCustomerDetailApi.as_view(), name="detail"),
    path("me/", MeCustomerDetailApi.as_view(), name="me"),
    path("me/update/", MeCustomerUpdateApi.as_view(), name="update"),
]

# Employee
employee_patterns = [
    path("me/", MeEmployeeDetailApi.as_view(), name="me"),
    path("me/update/", MeEmployeeUpdateApi.as_view(), name="update"),
]


urlpatterns = [
    path("customers/", include((customer_patterns, "customers"))),
    path("employees/", include((employee_patterns, "employees"))),
]
