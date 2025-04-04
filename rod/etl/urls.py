from django.urls import include
from django.urls import path

from rod.etl.apis.customer import AdminCustomerDetailApi
from rod.etl.apis.customer import AdminCustomerListApi
from rod.etl.apis.customer import MeCustomerDetailApi
from rod.etl.apis.customer import MeCustomerUpdateApi
from rod.etl.apis.employee import MeEmployeeDetailApi
from rod.etl.apis.employee import MeEmployeeUpdateApi
from rod.etl.apis.plan import PlanCreateApi
from rod.etl.apis.plan import PlanDeleteApi
from rod.etl.apis.plan import PlanDetailApi
from rod.etl.apis.plan import PlanFeatureCreateApi
from rod.etl.apis.plan import PlanFeatureDeleteApi
from rod.etl.apis.plan import PlanFeatureDetailApi
from rod.etl.apis.plan import PlanFeatureListApi
from rod.etl.apis.plan import PlanFeatureUpdateApi
from rod.etl.apis.plan import PlanListApi
from rod.etl.apis.plan import PlanUpdateApi
from rod.etl.apis.subscription import SubscriptionCancelAPI
from rod.etl.apis.subscription import SubscriptionCreateAPI
from rod.etl.apis.subscription import SubscriptionDetailAPI
from rod.etl.apis.subscription import SubscriptionListAPI

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

# Plan
plan_patterns = [
    path("", PlanListApi.as_view(), name="list"),
    path("create/", PlanCreateApi.as_view(), name="create"),
    path("<int:pk>/", PlanDetailApi.as_view(), name="detail"),
    path("<int:pk>/update/", PlanUpdateApi.as_view(), name="update"),
    path("<int:pk>/delete/", PlanDeleteApi.as_view(), name="delete"),
    path("<int:pk>/features/", PlanFeatureListApi.as_view(), name="feature-list"),
    path(
        "<int:pk>/features/create/",
        PlanFeatureCreateApi.as_view(),
        name="feature-create",
    ),
]

# Plan Feature
plan_feature_patterns = [
    path("<int:pk>/", PlanFeatureDetailApi.as_view(), name="detail"),
    path("<int:pk>/update/", PlanFeatureUpdateApi.as_view(), name="update"),
    path("<int:pk>/delete/", PlanFeatureDeleteApi.as_view(), name="delete"),
]

# Subscription
subscription_patterns = [
    path("", SubscriptionListAPI.as_view(), name="list"),
    path("create/", SubscriptionCreateAPI.as_view(), name="create"),
    path("<uuid:pk>/", SubscriptionDetailAPI.as_view(), name="detail"),
    path("me/", SubscriptionDetailAPI.as_view(), name="me"),
    path("me/cancel/", SubscriptionCancelAPI.as_view(), name="cancel"),
]

urlpatterns = [
    path("customers/", include((customer_patterns, "customers"))),
    path("employees/", include((employee_patterns, "employees"))),
    path("plans/", include((plan_patterns, "plans"))),
    path("plan-features/", include((plan_feature_patterns, "plan-features"))),
    path("subscriptions/", include((subscription_patterns, "subscriptions"))),
]
