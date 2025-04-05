from django.urls import include
from django.urls import path

from rod.billing.apis.subscription_api import SubscriptionCancelAPI
from rod.billing.apis.subscription_api import SubscriptionCreateAPI
from rod.billing.apis.subscription_api import SubscriptionDetailAPI
from rod.billing.apis.subscription_api import SubscriptionListAPI

# Subscription
subscription_patterns = [
    path("", SubscriptionListAPI.as_view(), name="list"),
    path("create/", SubscriptionCreateAPI.as_view(), name="create"),
    path("<uuid:pk>/", SubscriptionDetailAPI.as_view(), name="detail"),
    path("me/", SubscriptionDetailAPI.as_view(), name="me"),
    path("me/cancel/", SubscriptionCancelAPI.as_view(), name="cancel"),
]

urlpatterns = [
    path("subscriptions/", include((subscription_patterns, "subscriptions"))),
]
