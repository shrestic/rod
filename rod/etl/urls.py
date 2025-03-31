from django.urls import include
from django.urls import path

from rod.etl.apis import CustomerDetailApi
from rod.etl.apis import CustomerListApi
from rod.etl.apis import CustomerUpdateApi

customer_patterns = [
    path("", CustomerListApi.as_view(), name="list"),
    path("<uuid:pk>/", CustomerDetailApi.as_view(), name="detail"),
    path("<uuid:pk>/update/", CustomerUpdateApi.as_view(), name="update"),
]

urlpatterns = [
    path("customers/", include((customer_patterns, "customers"))),
]
