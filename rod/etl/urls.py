from django.urls import include
from django.urls import path

from rod.etl.apis.customer import CustomerDetailApi
from rod.etl.apis.customer import CustomerListApi
from rod.etl.apis.customer import CustomerMeDetailApi
from rod.etl.apis.customer import CustomerMeUpdateApi

customer_patterns = [
    path("", CustomerListApi.as_view(), name="list"),
    path("<uuid:pk>/", CustomerDetailApi.as_view(), name="detail"),
    path("me/", CustomerMeDetailApi.as_view(), name="me"),
    path("me/update/", CustomerMeUpdateApi.as_view(), name="update"),
]

urlpatterns = [
    path("customers/", include((customer_patterns, "customers"))),
]
