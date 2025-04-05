from django.contrib import admin

from rod.billing.models.subscription_model import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "plan",
        "start_date",
        "end_date",
        "is_active",
        "billing_cycle_day",
        "billing_frequency",
    ]
    list_per_page = 10
    ordering = ["customer__user__first_name", "customer__user__last_name"]
