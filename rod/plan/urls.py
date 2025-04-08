from django.urls import include
from django.urls import path

from rod.plan.apis.plan_api import PlanCreateApi
from rod.plan.apis.plan_api import PlanDeleteApi
from rod.plan.apis.plan_api import PlanDetailApi
from rod.plan.apis.plan_api import PlanFeatureBulkCreateApi
from rod.plan.apis.plan_api import PlanFeatureCreateApi
from rod.plan.apis.plan_api import PlanFeatureDeleteApi
from rod.plan.apis.plan_api import PlanFeatureDetailApi
from rod.plan.apis.plan_api import PlanFeatureListApi
from rod.plan.apis.plan_api import PlanFeatureUpdateApi
from rod.plan.apis.plan_api import PlanListApi
from rod.plan.apis.plan_api import PlanUpdateApi

# Plan
plan_patterns = [
    path("", PlanListApi.as_view(), name="list"),
    path("create/", PlanCreateApi.as_view(), name="create"),
    path("<str:code>/", PlanDetailApi.as_view(), name="detail"),
    path("<str:code>/update/", PlanUpdateApi.as_view(), name="update"),
    path("<str:code>/delete/", PlanDeleteApi.as_view(), name="delete"),
    path("<str:code>/features/", PlanFeatureListApi.as_view(), name="feature-list"),
    path(
        "<str:code>/features/bulk-create/",
        PlanFeatureBulkCreateApi.as_view(),
        name="feature-bulk-create",
    ),
]

# Plan Feature
plan_feature_patterns = [
    path("create/", PlanFeatureCreateApi.as_view(), name="create"),
    path("<int:pk>/", PlanFeatureDetailApi.as_view(), name="detail"),
    path("<int:pk>/update/", PlanFeatureUpdateApi.as_view(), name="update"),
    path("<int:pk>/delete/", PlanFeatureDeleteApi.as_view(), name="delete"),
]


urlpatterns = [
    path("plans/", include((plan_patterns, "plans"))),
    path("plan-features/", include((plan_feature_patterns, "plan-features"))),
]
