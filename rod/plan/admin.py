from django.contrib import admin

from rod.plan.models.plan_model import Plan
from rod.plan.models.plan_model import PlanFeature


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "max_rows_processed",
        "cost_per_million_rows",
        "base_cost",
    ]
    list_per_page = 10
    ordering = ["name"]


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = [
        "plan",
        "feature_name",
        "feature_description",
    ]
    list_per_page = 10
    ordering = ["plan__name", "feature_name"]
    list_select_related = ["plan"]
